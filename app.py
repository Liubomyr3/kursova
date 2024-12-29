from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Ініціалізація Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Використовуйте current_timestamp

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mark = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

with app.app_context():
    db.create_all()


# Функція для додавання та відображення відгуків
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mark = request.form.get('mark')
        message = request.form.get('message')

        if not name or not email or not mark or not message:
            flash('Заповніть всі поля!', 'danger')
            return redirect(url_for('feedback'))

        new_feedback = Feedback(name=name, email=email, mark=mark, message=message)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Ваш відгук успішно збережений!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')



@app.route('/book_trip', methods=['GET', 'POST'])
def book_trip():
    # Перевірка, чи користувач увійшов у систему
    if 'user_id' not in session:
        flash('Будь ласка, увійдіть у свій акаунт, щоб забронювати поїздку.', 'warning')
        return redirect(url_for('login'))  # Перенаправлення на вхід
    
    # Якщо користувач увійшов
    flash('Поїздка успішно заброньована!', 'success')
    return redirect(url_for('dashboard'))  # Перенаправлення в особистий кабінет

@app.route('/excursion/<name>')
def excursion(name):
    try:
        return render_template(f'{name}.html')
    except:
        return render_template('404.html'), 404

# Функція входу
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Перевірка користувача
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Успішний вхід!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неправильний email або пароль.', 'danger')
    
    return render_template('Login.html')

# Функція реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Паролі не збігаються!', 'danger')
            return render_template('Register.html')

        # Перевірка чи користувач існує
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email вже зареєстровано.', 'danger')
            return render_template('Register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація успішна! Увійдіть у свій акаунт.', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')


# Функція для особистого кабінету
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Будь ласка, увійдіть у свій акаунт.', 'warning')
        return redirect(url_for('login'))
    
    # Замість User.query.get(session['user_id']):
    user = db.session.get(User, session['user_id'])

    if not user:
        flash('Користувач не знайдений.', 'danger')
        return redirect(url_for('login'))

    return render_template('Dashboard.html', user=user)



# Функція для виходу
@app.route('/logout')
def logout():
    # Очищення сесії
    session.clear()
    flash('Ви успішно вийшли з акаунту.', 'success')
    return redirect(url_for('login'))



@app.route('/')
def index():
    return render_template('index.html')

# Обробка помилок 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)


'''
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Ініціалізація Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/excursion/<name>')
def excursion(name):
    try:
        return render_template(f'{name}.html')
    except:
        return render_template('404.html'), 404

# Реєстрація
@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            error_message = 'Паролі не збігаються!'
            return render_template('Register.html', error_message=error_message)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Користувач із таким email вже існує!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація успішна! Тепер увійдіть.', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html', error_message=error_message)

# Авторизація
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Перевірка користувача в базі
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Збереження в сесії
            session['user_id'] = user.id
            flash('Вхід успішний!', 'success')
            return redirect(url_for('dashboard'))  # Перенаправлення до Dashboard
        else:
            flash('Невірний email або пароль!', 'danger')

    return render_template('Login.html')


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('Будь ласка, увійдіть у систему.', 'warning')
        return redirect(url_for('login'))  # Якщо не увійшов, перенаправляємо до login

    # Отримання даних користувача
    user = User.query.get(user_id)
    if not user:
        flash('Користувач не знайдений!', 'danger')
        return redirect(url_for('login'))

    return render_template('Dashboard.html', user=user)


#вихід
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Видаляємо ID із сесії
    flash('Ви вийшли з акаунта.', 'success')
    return redirect(url_for('login'))


# Обробка помилок 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)'''
'''from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
#from data import db, User

# Ініціалізація Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Користувач/OneDrive/Desktop/Kursova/Kursova/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<User {self.name}>'

# Підключення бази даних
#db.init_app(app)

# Створення бази даних
with app.app_context():
    db.create_all()

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/excursion/<name>')
def excursion(name):
    try:
        return render_template(f'{name}.html')
    except:
        return render_template('404.html'), 404

# Сторінка авторизації
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Перевірка користувача
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Невірний email або пароль!', 'danger')
            return redirect(url_for('login'))

        flash(f'Вітаємо, {user.name}!', 'success')
        return redirect(url_for('index'))

    return render_template('Login.html')

# Сторінка реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Перевірка паролів
        if password != confirm_password:
            flash('Паролі не збігаються!', 'danger')
            return redirect(url_for('register'))

        # Перевірка, чи email вже існує
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email вже зареєстровано!', 'danger')
            return redirect(url_for('register'))

        # Хешування паролю
        hashed_password = generate_password_hash(password, method='sha256')

        # Додавання користувача
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Реєстрація успішна!', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')

# Обробка помилок 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)'''
'''from flask import *
from data import db
db.create_all()
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/excursion/<name>')
def excursion(name):
    try:
        return render_template(f'{name}.html')
    except:
        return render_template('404.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Перевірка чи користувач існує
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Невірний email або пароль!', 'danger')
            return redirect(url_for('login'))

        flash(f'Вітаємо, {user.name}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('Login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Перевірка паролів
        if password != confirm_password:
            flash('Паролі не збігаються!', 'danger')
            return redirect(url_for('register'))

        # Перевірка чи email вже існує
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email вже зареєстровано!', 'danger')
            return redirect(url_for('register'))

        # Захешований пароль
        hashed_password = generate_password_hash(password, method='sha256')

        # Додавання нового користувача
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Реєстрація успішна!', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
'''
'''
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Паролі не збігаються!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email уже зареєстровано!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація успішна!', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')

# Маршрут для авторизації
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Невірний email або пароль!', 'danger')
            return redirect(url_for('login'))

        flash(f'Вітаємо, {user.name}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('Login.html')

# Особистий кабінет
@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')

# Обробник помилок 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)'''
'''
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Ініціалізація Flask та SQLAlchemy
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Модель користувача
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка авторизації
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Перевірка користувача
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Невірний email або пароль!', 'danger')
            return redirect(url_for('login'))

        flash(f'Вітаємо, {user.name}!', 'success')
        return redirect(url_for('index'))

    return render_template('Login.html')

# Сторінка реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Перевірка паролів
        if password != confirm_password:
            flash('Паролі не збігаються!', 'danger')
            return redirect(url_for('register'))

        # Перевірка, чи email вже існує
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email вже зареєстровано!', 'danger')
            return redirect(url_for('register'))

        # Хешування паролю
        hashed_password = generate_password_hash(password, method='sha256')

        # Додавання користувача
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Реєстрація успішна!', 'success')
        return redirect(url_for('login'))

    return render_template('Register.html')

# Обробка помилок 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
'''
