from flask import Flask
from flask_login import LoginManager
from app.models.user import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

def create_app():
    app = Flask(__name__)
    login_manager.init_app(app)
    app.config.from_object('app.config.Config')
    login_manager.login_view = 'auth.login'
    
   
    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.admin_routes import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
  
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)
    
    return app
