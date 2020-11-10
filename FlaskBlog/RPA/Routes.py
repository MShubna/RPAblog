from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
from FlaskBlog import db
from FlaskBlog.Model_s import Rpa, Rpaarea, Rpacat, Rpasubcat
from FlaskBlog.RPA.Forms import RpaForm
from FlaskBlog.RPA.utils import send_email

rpa = Blueprint ( 'RPA', __name__ )
static_path = ['Rules/','Input Type/','Input Quality/','Stabilyty/']
file_names = ['1.png','2.png','3.png','4.png','5.png']
d_comments = {0:['Very <br> creative','Pretty <br>creative','A mix between<br> rules and creativity','Pretty <br>rule based','Very <br>rule based'],
              1:['Very much <br>paperbased','Pretty much <br>paperbased','A mix between<br> digital and paperbased','Pretty much <br>digital','Very much <br>digital'],
              2:['Very much <br> unstructured','Pretty much <br>unstructured','A mix between<br>structured and unstructured','Pretty much <br>structured','Very much <br>structured'],
              3:['Major <br> change expected','Several<br> changes expected','Some <br>changes expected','Minor <br> changes expected','No <br>changes expected']}



def ratings(rules,input,indata,chg,b,doc1,doc2,doc3,doc4):
    b_ = rules
    c_ = input
    d_ = indata
    e_ = chg
    d1 =  b+doc1+doc2+doc3+doc4
    suitability = 0 if b_*c_*d_ == 0 else round(((b_+c_+d_)*20)/3,0)
    readiness =0 if e_*d1 == 0 else (e_+d1)*10
    score = 14 if suitability*readiness == 0 else (b_+c_+d_+e_+d1)*4
    scores = {'score': score,'suitability': suitability ,'readiness': readiness}
    return scores

@rpa.route ( '/rpa/<int:post_id>' )
def rpa_post(post_id) :
    post = Rpa.query.get_or_404 ( post_id )
    area = Rpaarea.query.get_or_404 ( post.rpaarea )
    return render_template ( 'Rpa_post1.html', title=post.title, post=post, area=area )


@rpa.route ( '/rpa/<int:post_id>/update', methods=['GET', 'POST'] )
@login_required
def update_rpa_post(post_id) :
    post = Rpa.query.get_or_404 ( post_id )
    if post.author != current_user :
        abort ( 403 )
    form = RpaForm ()
    form.area.choices = [(g.id, g.title) for g in Rpaarea.query.all()]
    if form.area.data == None:
        form.cat.choices = [(c.id, c.title) for c in Rpacat.query.filter( Rpacat.id_rpa == post.rpaarea)]
    else:
        form.cat.choices = [(c.id,c.title) for c in Rpacat.query.filter( Rpacat.id_rpa == form.area.data)]

    #form.cat1.query = Rpacat.query.filter ( Rpacat.id_rpa == post.rpaarea )
    if form.cat.data == None:
        form.subcat.choices = [(b.id, b.title) for b in Rpasubcat.query.filter ( Rpasubcat.id_rpacat == post.rpacat)]
    else:
        form.subcat.choices = [(b.id,b.title) for b in Rpasubcat.query.filter( Rpasubcat.id_rpacat == form.cat.data )]
    #form.subcat.choices = [(b.id,b.title) for b in Rpasubcat.query.all()]

    if form.validate_on_submit() :
        post.title = form.title.data
        post.content = form.content.data
        post.rpaarea = form.area.data
        post.rpacat = form.cat.data
        post.rpasubcat = form.subcat.data
        post.rulebasedrate = int(form.rulebaserate.data)
        post.indatarate = int( form.indatarate.data )
        post.indatastructrate = int( form.indatastructrate.data )
        post.changesrate  = int(form.changesrate.data)
        post.b = form.b.data
        post.doc1 = 0 if form.b.data ==0 else form.doc1.data
        post.doc2 = 0 if form.b.data ==0 else form.doc2.data
        post.doc3 = 0 if form.b.data ==0 else  form.doc3.data
        post.doc4 = 0 if form.b.data ==0 else  form.doc4.data
        post.docrate = post.b +post.doc1 +post.doc2 +post.doc3+post.doc4
        post.email = form.email.data
        db.session.commit()
        #scores = ratings( post.rulebasedrate, post.indatarate,post.indatastructrate,post.changesrate,post.b,post.doc1,post.doc2, post.doc3, post.doc4)
        #scores = {'score' : score,'suitability' : suitability,'readiness' : readiness}
        #render_template( 'demo1.html',title='resultat',egend='Update your RPA idea',score=scores['score'], suitability=scores['suitability'],readiness= scores['readiness'] )

        flash( 'Your RPA idea  has been updated!','success' )
        return redirect ( url_for ( 'RPA.rpa_post', post_id=post.id ) )
    elif request.method == 'GET' :
        form.title.data = post.title
        form.content.data = post.content
        form.area.data = post.rpaarea
        form.cat.data = post.rpacat
        form.subcat.data = post.rpasubcat
        form.rulebaserate.data = post.rulebasedrate
        form.indatarate.data = post.indatarate
        form.indatastructrate.data = post.indatastructrate
        form.changesrate.data = post.changesrate
        form.b.data = post.b
        form.doc1.data = post.doc1
        form.doc2.data = post.doc2
        form.doc3.data = post.doc3
        form.doc4.data = post.doc4
        form.email.data = post.email
    return render_template ( 'Create_Rpa.html', title='Update RPA idea!', form=form, legend='Update your RPA idea',
                             post_id = post.id, filelist = file_names, dir_ectory = static_path, comments = d_comments,
                             score = None,suitability = '0', readiness = '30' )


@rpa.route ( '/rpa/new', methods=['GET', 'POST'] )
@login_required
def new_rpa() :
    form = RpaForm ()
    form.area.choices = [(g.id, g.title) for g in Rpaarea.query.all ()]
    form.cat.choices = [(c.id, c.title) for c in Rpacat.query.all ()]
    form.subcat.choices = [(c.id, c.title) for c in Rpasubcat.query.all ()]
    form.email.data = current_user.email
    if form.validate_on_submit () :
        #print (form.subcat.data)

        doc_1 = 0 if form.b.data == 0 else form.doc1.data
        doc_2 = 0 if form.b.data == 0 else form.doc2.data
        doc_3 = 0 if form.b.data == 0 else form.doc3.data
        doc_4 = 0 if form.b.data == 0 else form.doc4.data
        doc_rate = form.b.data + doc_1 + doc_2 + doc_3 +doc_4
        post = Rpa ( title=form.title.data, content=form.content.data, rpaarea=form.area.data, author=current_user,
                     email=form.email.data, rpacat=form.cat.data, rpasubcat=form.subcat.data,
                     changesrate = int(form.changesrate.data), indatarate=int(form.indatarate.data),
                     rulebasedrate=int(form.rulebaserate.data), indatastructrate = int( form.indatastructrate.data ), b = form.b.data, doc1 = doc_1, doc2 = doc_2,
                     doc3 = doc_3, doc4 = doc_4 , docrate = doc_rate)
        db.session.add ( post )
        db.session.commit ()
        flash ( 'Your post has been created! ', 'success' )
        return redirect ( url_for ( 'main.RPA_j' ) )
    return render_template ( 'Create_Rpa_multisteps.html', title='New RPA Idea ',
                             form=form, legend='New RPA Idea' , filelist = file_names, dir_ectory = static_path, comments = d_comments)



@rpa.route ( "/email" )
def email() :
    send_email( current_user.email )
    #flash( 'An email has been send  with BLABLA','info' )
    return (''),204


@rpa.route ( "/rpa/<int:post_id>/delete", methods=['POST'] )
@login_required
def delete_rpa(post_id) :
    post = Rpa.query.get_or_404 ( post_id )
    if post.author != current_user :
        abort ( 403 )
    db.session.delete ( post )
    db.session.commit ()
    flash ( 'Your RPA Idea has been deleted!', 'success' )
    return redirect ( url_for ( 'main.RPA_j' ) )

@rpa.route ( "/cat/<area>" )
def category(area):
    cats = Rpacat.query.filter( Rpacat.id_rpa == area ).all()
    cat_array = []
    for cat in cats:
        catObj = {'id' : cat.id,'title' : cat.title}
        cat_array.append(catObj)
    return jsonify({'r_cat':cat_array})

@rpa.route ( "/subcat/<cat>" )
def subcategory(cat):
    subcats = Rpasubcat.query.filter( Rpasubcat.id_rpacat == cat).all()
    subcat_array = []
    for scat in subcats:
        scatObj = {'id' : scat.id,'title' : scat.title}
        subcat_array.append(scatObj)
    return jsonify({'r_subcat':subcat_array})


def calc_doc(b,doc1,doc2,doc3,doc4):
    if b=='false':
        docrate = 0
    else:
        b_doc = 0 if b =='false'else 1
        d1_doc = 0 if doc1 == 'false' else 1
        d2_doc = 0 if doc2 == 'false' else 1
        d3_doc = 0 if doc3 == 'false' else 1
        d4_doc = 0 if doc4 =='false' else 1
        docrate = b_doc+d1_doc+d2_doc+d3_doc+d4_doc
    return docrate






@rpa.route ( "/<rules>/<input>/<indata>/<chg>/<b>/<doc1>/<doc2>/<doc3>/<doc4>")
def totalrating(rules,input,indata,chg,b,doc1,doc2,doc3,doc4):
    b_ = int(rules[0])
    c_ = int(input[0])
    d_ = int(indata[0])
    e_ = int( chg[0] )
    d1 = calc_doc(b,doc1,doc2,doc3,doc4)
    suitability = 0 if b_*c_*d_ == 0 else round(((b_+c_+d_)*20)/3,0)
    readiness =0 if e_*d1 == 0 else (e_+d1)*10
    score = 14 if suitability*readiness == 0 else (b_+c_+d_+e_+d1)*4
    scores = {'score': score,'suitability': suitability ,'readiness': readiness}
    print(scores)
    return jsonify({'scores':scores})



