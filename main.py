from app.config import app, db, login_manager
from app.models import User

from app.handlers import home
from app.handlers import auth
from app.handlers import ad


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()  # Создание таблиц при первом запуске


app.register_blueprint(home.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(ad.bp)



if __name__ == "__main__":
    app.run(debug=True, port=8000)
    