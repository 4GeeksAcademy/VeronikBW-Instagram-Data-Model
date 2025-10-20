import os
from flask_admin import Admin
from models import db, User, Post, Media, Comment
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    class User_admin(ModelView):
        column_list = ('id', 'first_name', 'last_name', 'email', 'posts', 'comments')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(User_admin(User, db.session))
    admin.add_view(User_admin(Post, db.session))
    admin.add_view(User_admin(Media, db.session))
    admin.add_view(User_admin(Comment, db.session)) 

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))