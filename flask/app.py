# app.py
from flask import Flask

# Criar a aplicação Flask
app = Flask(__name__)

# Importar configurações
from config import Config
app.config.from_object(Config)

# Importar e inicializar extensões
from extensions import db
db.init_app(app)

# Importar modelos (isso agora funcionará sem problemas)
from models.models import Usuario

# Importar e registrar blueprints
from routes.main import main_bp
app.register_blueprint(main_bp)

# Criar tabelas do banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)