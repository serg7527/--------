import re
from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.config import db
from app.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

def has_invalid_characters(username, password):
    # Определяем запрещенные символы
    pattern = re.compile(r'[^a-zA-Z0-9]')
    # Проверяем имя пользователя и пароль на наличие запрещенных символов
    if pattern.search(username) or pattern.search(password):
        return True
    return False

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Проверка на наличие запрещенных символов
        if has_invalid_characters(username, password):
            flash("Имя пользователя и пароль могут содержать только буквы и цифры.", "danger")
            return redirect(url_for("auth.register"))

        # Проверка на существующего пользователя
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(
                "Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.",
                "danger",
            )
            return redirect(url_for("auth.register"))

        # Хеширование пароля
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Регистрация успешна! Теперь вы можете войти.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home.index"))
        else:
            flash("Неверные учетные данные. Пожалуйста, попробуйте снова.", "danger")
    return render_template("login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.index"))
