from flask import render_template, request, Blueprint
from FlaskBlog.Model_s import Post, Rpa

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    q = request.args.get('q')
    page = request.args.get ( 'page', 1, type=int )

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.content.contains(q)).order_by(Post.date_posted.desc())
    else:
        posts = Post.query.order_by(Post.date_posted.desc())
    posts1 = posts.paginate ( page=page, per_page=3 )
    return render_template('Home_page.html', title = "Blog posts",posts=posts1, q=q)



@main.route('/1')
def step_1():
    return render_template('Toggle_sw.html', title="******")

@main.route('/2')
def step_2():
    return render_template('Cicle_progress_bar.html', title="CPB")


@main.route('/3')
def step_3():
    return render_template( 'demo.html',title="demo circle", procent = '78',procent2 = '14' , procent3 = '96')


@main.route('/RPA_journey')
def RPA_j():
    page = request.args.get('page', 1, type=int)
    rpas = Rpa.query.order_by(Rpa.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('RPA.html', title="List of Rpa ideas", posts=rpas)
