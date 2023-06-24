from flask import Flask, render_template, flash, redirect, url_for, session, request
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'secret'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Article %r>' & self.id


class RegistrationForm(FlaskForm):
    username = StringField(validators=[validators.DataRequired(), validators.Length(min=4, max=50)])
    email = StringField(validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField(validators={validators.DataRequired(),
                                         validators.EqualTo('confirm_password',
                                                            message='Пароли не совпадают')})
    confirm_password = PasswordField()


class LoginForm(FlaskForm):
    username = StringField(validators=[validators.DataRequired(), validators.Length(min=4, max=50)])
    password = PasswordField(validators=[validators.DataRequired()])


@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index']
    if request.endpoint not in allowed_routes and 'logged_in' not in session:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Вы можете сейчас зарегистрироваться и авторизоваться', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['logged_in'] = True
            session['username'] = user.username
            flash('Вы авторизовались', 'success')
            return redirect(url_for('index'))
        else:
            error = 'Неправильное имя пользователя или пароль'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('index'))


@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    api_key = 'b41f842f9800a4d28dbe5d5bbea18a3e'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = round(data['main']['temp'] - 273.15, 1)
    wind_speed = data['wind']['speed']
    return render_template('get_weather.html', city=city, weather=weather_description,
                           temperature=temperature, wind_speed=wind_speed)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        return redirect(url_for('get_weather'))
    return render_template('weather.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/map')
def map():
    url = f'https://openweathermap.org/weathermap?basemap=map' \
          f'&cities=true&layer=temperature&lat=64.5340&lon=40.5631&zoom=5'
    return render_template('map.html', url=url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5006')
