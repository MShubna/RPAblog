from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from FlaskBlog import db
from FlaskBlog.Model_s import Post , Tag
from FlaskBlog.posts.Forms import PostForm

posts = Blueprint('posts',__name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit () :
        post = Post ( title=form.title.data,content=form.content.data,author=current_user )
        db.session.add ( post )
        db.session.commit ()
        flash ( 'Your post has been created! ','success' )

        return redirect(url_for('main.home'))

    return render_template('Create_post.html', title='New post',
                           form=form, legend='New Post')



@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template('Post.html', title=post.title, post=post, tags=tags)

@posts.route('/post/tag/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts.all()
    return render_template('Tag_detail.html', title=tag.name, tag=tag, posts=posts)



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        '''alternative      
        form = PostForm ( formdata = request.form, obj=post )
        form.populate_obj ( post )
        '''
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('Create_post.html', title='Update Post',form=form, legend='Update Post', post_id=post.id)

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

