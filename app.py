from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from settings import settings


from Server.database import db, Role, User, StateOrder
from Server.Models import UserSession

from Server.Repository import UserRepository
from Server.Models import GetUser

from Server.Forms import LoginForm
from Server.Service import LoginService
from Server.AdminView import admin

from Server.Blueprints.manager.manager import manager_router
from Server.Blueprints.worker.worker import worker_router


app = Flask(__name__)
app.config['SECRET_KEY'] = '2wae3tgv'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:' \
                                        f'{settings.pg_port}/{settings.pg_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = '/Files'


app.register_blueprint(manager_router, name="manager_blueprint", url_prefix="/manager")
app.register_blueprint(worker_router, name="worker_blueprint", url_prefix="/worker")


db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

admin.init_app(app)

migrate = Migrate(app, db, render_as_batch=True)


route = {
    "worker": "worker_blueprint.index",
    "manager": "manager_blueprint.index",
    "admin": "/admin",
    "user": "/"
}


@login_manager.user_loader
def load_user(id_user) -> UserSession:
    repo = UserRepository(db.session)
    try:
        return UserSession(GetUser.model_validate(repo.get_user(int(id_user)), from_attributes=True))
    except:
        return UserSession(None)


@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        user_roles = current_user.user.role.name
        if "worker" in user_roles:
            return redirect(url_for(route["worker"]))
        elif "manager" in user_roles:
            return redirect(url_for(route["manager"]))
        elif "admin" in user_roles:
            return redirect(route["admin"])
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "GET":
        return render_template("index.html", title="Авторизация", form=form, user=current_user)
    if request.method == "POST":
        if form.validate_on_submit():
            login_service = LoginService()
            user = login_service.login_user(form.email.data, form.password.data)
            if user is None:
                return redirect(url_for("login"))
            login_user(UserSession(user))
            return redirect(url_for("index"))
        return redirect(url_for("login"))


@app.route("/init_app/<password>", methods=["GET"])
def create_user_admin(password):
    if request.method == "GET":
        if password == "SkripnikVlad1":
            roles = [
                Role(
                    name="worker",
                    description="worker"
                ),
                Role(
                    name="manager",
                    description="manager"
                ),
                Role(
                    name="admin",
                    description="admin"
                ),
                Role(
                    name="user",
                    description="user"
                ),
            ]

            state_order = [
                StateOrder(
                    name="Принято",
                ),
                StateOrder(
                    name="Делаеться",
                ),
                StateOrder(
                    name="Закончено",
                ),
                StateOrder(
                    name="Отменено",
                )
            ]

            db.session.add_all(roles)
            db.session.add_all(state_order)
            db.session.commit()

            admin_user = User(
                name="Владислав",
                surname="Скрипник",
                patronymics="Викторович",

                phone="9053626466",
                email="admin@admin.ru",

                role=roles[2]
            )
            admin_user.password = "admin"

            db.session.add(admin_user)
            db.session.commit()

            return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
