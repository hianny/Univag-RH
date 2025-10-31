from flask_login import LoginManager

from tests.models import Usuario

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Faça login para acessar o sistema'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

def init_app(app):
    login_manager.init_app(app)