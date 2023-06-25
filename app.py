from forms import *

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
