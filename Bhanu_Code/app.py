# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '3d6f45a5fc12445dbac2f59c3b6c7cb1'  # Replace with a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///constitution_app.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    progress = db.Column(db.Text, default='{}')  # Stores progress as JSON

    def get_progress(self):
        return json.loads(self.progress)

    def set_progress(self, progress):
        self.progress = json.dumps(progress)

# Lesson model
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    is_quiz = db.Column(db.Boolean, default=False)

# Question model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    choices = db.Column(db.Text, nullable=False)  # Stored as JSON
    correct_answer = db.Column(db.String(200), nullable=False)

@app.template_filter('json_loads')
def json_loads_filter(s):
    return json.loads(s)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    lessons = Lesson.query.order_by(Lesson.group_id, Lesson.order).all()
    progress = current_user.get_progress()
    return render_template('index.html', lessons=lessons, progress=progress)

@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson.html', lesson=lesson)

@app.route('/complete_lesson/<int:lesson_id>')
@login_required
def complete_lesson(lesson_id):
    progress = current_user.get_progress()
    progress[str(lesson_id)] = True
    current_user.set_progress(progress)
    db.session.commit()
    return redirect(url_for('quiz', lesson_id=lesson_id))

@app.route('/quiz/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def quiz(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    questions = Question.query.filter_by(lesson_id=lesson_id).all()
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer == question.correct_answer:
                score += 1
        
        total_questions = len(questions)
        percentage = (score / total_questions) * 100
        
        if percentage >= 70:  # Pass threshold
            progress = current_user.get_progress()
            progress[str(lesson_id)] = True
            current_user.set_progress(progress)
            db.session.commit()
            flash(f'Congratulations! You passed the quiz with {percentage:.2f}%', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'You scored {percentage:.2f}%. Please try again to pass the quiz.', 'error')
            return redirect(url_for('quiz', lesson_id=lesson_id))
    
    return render_template('quiz.html', lesson=lesson, questions=questions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        flash('Username already exists', 'error')
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# templates/index.html

# templates/lesson.html

# templates/quiz.html

# templates/login.html

# templates/register.html

# static/style.css
