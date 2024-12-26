from flask import Flask, render_template
from routes.project_routes import project_blueprint
from routes.column_routes import column_blueprint
from routes.task_routes import task_blueprint
from routes.log_routes import log_blueprint
from routes.user_routes import user_blueprint
from database import Base, engine

# Создание всех таблиц в базе данных
Base.metadata.create_all(engine)

app = Flask(__name__, template_folder='templates')

# Регистрация Blueprints
app.register_blueprint(project_blueprint, url_prefix='/project')
app.register_blueprint(column_blueprint, url_prefix='/column')
app.register_blueprint(task_blueprint, url_prefix='/task')
app.register_blueprint(log_blueprint, url_prefix='/log')
app.register_blueprint(user_blueprint, url_prefix='/user')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)