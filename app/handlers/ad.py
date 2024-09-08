import os
from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.config import app, db
from app.models import Ad

bp = Blueprint("ad", __name__, url_prefix="/ad")


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_ad():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        image = request.files.get("image")  # Используем get() для безопасного доступа

        # Сохранение изображения на сервере
        image_filename = None
        if image:
            image_filename = secure_filename(image.filename)  # Безопасное имя файла
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        new_ad = Ad(title=title, description=description, image_filename=image_filename)
        db.session.add(new_ad)
        db.session.commit()

        flash("Объявление успешно добавлено!", "success")
        return redirect(url_for("home.index"))

    return render_template("add_ad.html")


@bp.route("/edit/<int:ad_id>", methods=["GET", "POST"])
@login_required
def edit_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        image = request.files.get("image")

        old_image_filename = ad.image_filename  # Сохраним имя старого изображения
        image_filename = old_image_filename  # Предполагаем, что новое изображение не загружено

        if image:
            # Если новое изображение загружено, сохраняем его
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

            # Удаляем старое изображение, если оно существует
            if old_image_filename:
                old_image_path = os.path.join(app.config["UPLOAD_FOLDER"], old_image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        # Обновляем поля объявления
        ad.title = title
        ad.description = description
        ad.image_filename = image_filename

        db.session.commit()
        flash("Объявление успешно обновлено!", "success")
        return redirect(url_for("home.index"))

    return render_template("edit_ad.html", ad=ad)


@bp.route("/delete/<int:ad_id>", methods=["POST"])
@login_required
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    
    # Если у объявления есть изображение, удаляем его с сервера
    if ad.image_filename:
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], ad.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(ad)
    db.session.commit()
    
    flash("Объявление успешно удалено!", "success")
    return redirect(url_for("home.index"))