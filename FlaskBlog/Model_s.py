from datetime import datetime
from flask_login import UserMixin
from FlaskBlog import db, login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id) :
    return User.query.get ( int ( user_id ) )


class User ( db.Model, UserMixin ) :
    id = db.Column ( db.Integer, primary_key=True )
    username = db.Column ( db.String ( 20 ), unique=True, nullable=False )
    email = db.Column ( db.String ( 120 ), unique=True, nullable=False )
    image_file = db.Column ( db.String ( 20 ), nullable=False, default='default.jpg' )
    password = db.Column ( db.String ( 60 ), nullable=False )
    posts = db.relationship ( 'Post', backref='author', lazy=True )
    rpa = db.relationship ( 'Rpa', backref='author', lazy=True )

    def get_reset_token(self, expires_sec=1800) :
        s = Serializer ( current_app.config['SECRET_KEY'], expires_sec )
        return s.dumps ( {'user_id' : self.id} ).decode ( 'utf-8' )

    @staticmethod
    def verify_reset_token(token) :
        s = Serializer ( current_app.config['SECRET_KEY'] )
        try :
            user_id = s.loads ( token )['user_id']
        except :
            return None
        return User.query.get ( user_id )

    def __repr__(self) :
        return f"User('{self.username}','{self.email}','{self.image_file}')"


posts_tag = db.Table ( 'posts_tag',
                       db.Column ( 'post_id', db.Integer, db.ForeignKey ( 'post.id' ) ),
                       db.Column ( 'tag_id', db.Integer, db.ForeignKey ( 'tag.id' ) )
                       )

"""rpa_tag = db.Table('rpa_tag',
                    db.Column('rpa_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )
"""


class Post ( db.Model ) :
    id = db.Column ( db.Integer, primary_key=True )
    title = db.Column ( db.String ( 100 ), nullable=False )
    date_posted = db.Column ( db.DateTime, nullable=False, default=datetime.utcnow )
    content = db.Column ( db.Text, nullable=False )
    user_id = db.Column ( db.Integer, db.ForeignKey ( 'user.id' ), nullable=False )
    tags = db.relationship ( 'Tag', secondary=posts_tag, backref=db.backref ( 'posts', lazy='dynamic' ) )

    def __init__(self, *args, **kwargs) :
        super ( Post, self ).__init__ ( *args, **kwargs )

    def __repr__(self) :
        return f"Post('{self.title}','{self.date_posted}')"


class Rpaarea ( db.Model ) :
    id = db.Column ( db.Integer, primary_key=True )
    title = db.Column ( db.String ( 100 ), nullable=False )
    r_cat = db.relationship ( 'Rpacat', backref='Category', lazy=True )


class Rpacat ( db.Model ) :
    id = db.Column ( db.Integer, primary_key=True )
    title = db.Column ( db.String ( 100 ), nullable=False )
    id_rpa = db.Column ( db.Integer, db.ForeignKey ( 'rpaarea.id' ), nullable=False )
    cat = db.relationship ( 'Rpa', backref='Category', lazy=True )
    cat1 = db.relationship ( 'Rpa', backref='cat1', lazy=True )
    r_subcat = db.relationship ( 'Rpasubcat', backref='Category', lazy=True )

    def __repr__(self) :
        return f"{self.title}"


class Rpasubcat ( db.Model ) :
    id = db.Column ( db.Integer, primary_key=True )
    title = db.Column ( db.String ( 100 ), nullable=False )
    id_rpacat = db.Column ( db.Integer, db.ForeignKey ( 'rpacat.id' ), nullable=False )
    subcat = db.relationship ( 'Rpa', backref='Subcategory', lazy=True )

    def __repr__(self) :
        return f"{self.title}"


class Rpa ( db.Model ) :
    id = db.Column ( db.Integer, primary_key=True )
    title = db.Column ( db.String ( 100 ), nullable=False )
    content = db.Column ( db.Text, nullable=False )
    date_posted = db.Column ( db.DateTime, nullable=False, default=datetime.utcnow )
    user_id = db.Column ( db.Integer, db.ForeignKey ( 'user.id' ), nullable=False )
    rpaarea = db.Column ( db.Integer, db.ForeignKey ( 'rpaarea.id' ), nullable=False )
    rpacat = db.Column ( db.Integer, db.ForeignKey ( 'rpacat.id' ), nullable=False )
    rpasubcat = db.Column ( db.Integer, db.ForeignKey ( 'rpasubcat.id' ), nullable=False )
    email = db.Column ( db.String ( 120 ), nullable=False )
    docrate = db.Column ( db.Integer, nullable=False )
    # docrate1 = db.Column( db.Integer,nullable=False )
    # docrate2 = db.Column( db.Integer,nullable=False )
    # docrate3 = db.Column( db.Integer,nullable=False )
    # docrate4 = db.Column( db.Integer,nullable=False )
    indatastructrate = db.Column ( db.Integer, nullable=False )
    changesrate = db.Column ( db.Integer, nullable=False )
    indatarate = db.Column ( db.Integer, nullable=False )
    rulebasedrate = db.Column ( db.Integer, nullable=False )
    b = db.Column( db.Boolean(),nullable=False)
    doc1 = db.Column( db.Boolean(),nullable=False )
    doc2 = db.Column( db.Boolean(),nullable=False )
    doc3 = db.Column( db.Boolean(),nullable=False )
    doc4 = db.Column( db.Boolean(),nullable=False )
    def __repr__(self) :
        return f"RPA ideas ('{self.title}','{self.date_posted}')"


class Tag ( db.Model ) :
    id = db.Column ( db.Integer, primary_key=True )
    name = db.Column ( db.String ( 80 ), nullable=False )

    def __repr__(self) :
        return f"{self.name}"
