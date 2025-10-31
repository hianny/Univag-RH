from datetime import datetime
from tests.blueprints import auth_bp, funcionario_bp, rh_bp
from .database import init_app as db_init
from .login_manager import login_manager

def configure_all(app):
    configure_db(app)
    configure_routes(app)
    configure_template_filters(app)
    configure_login_manager(app)

def configure_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(funcionario_bp)
    app.register_blueprint(rh_bp)

def configure_db(app):
    db_init(app)

def configure_template_filters(app):
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%d/%m/%Y'):
        if None or value == '':
            return "N/A"
        try:
            # Tenta converter de string para datetime antes de formatar
            if isinstance(value, str):
                # Tenta formatos comuns, ajuste conforme a origem dos seus dados
                try:
                    value = datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    try:
                        value = datetime.strptime(value, '%d/%m/%Y')
                    except ValueError:
                        return value  # Retorna o valor original se não conseguir parsear
            return value.strftime(format)
        except Exception:
            return value

    @app.template_filter('currencyformat')
    def currencyformat(value):
        try:
            return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return value

def configure_login_manager(app):
    login_manager.init_app(app)
