from flask import Flask, render_template, request, redirect, url_for, flash, session


from models import db, User, Subject, Chapter, Quiz, Questions, Scores
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sarvn.sqlite'
app.config['SECRET_KEY'] = 'key'
db.init_app(app)

def setup_admin():
    if not User.query.first():
        admin_password = "admin123"
        hashed_password = generate_password_hash(admin_password)
        new_admin = User(Username="admin", Password=hashed_password, Role="admin", Name="Admin", Qualification="Admin", dob=datetime.now())
        db.session.add(new_admin)
        db.session.commit()


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        name = request.form['fullname']
        qualification = request.form['qualification']
        dob = request.form['dob']
        
        dob1 = datetime.strptime(dob, '%Y-%m-%d').date()

        user = User(Username=username, Password=password, Name=name, Qualification=qualification, dob=dob1)
        db.session.add(user)
        db.session.commit()
        flash('User Registered Successfully')
        return render_template('user_login.html')
    return render_template('user_register.html')  


@app.route('/adminlogin', methods = ['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin_user = User.query.filter_by(Username=username, Role='admin').first()

        if admin_user and check_password_hash(admin_user.Password, password):
            session['user_id'] = admin_user.Id
            session['role'] = admin_user.Role  
            flash('Admin login successful!')
            return redirect(url_for('admin_dashboard'))  
        else:
            flash('Admin ONLY')
            return redirect(url_for('/'))

    return render_template('adminlogin.html')


@app.route('/login', methods = ['GET','POST'])


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(Username = username, Role = 'user').first()

        if user and check_password_hash(user.Password, password):
            session['user_id'] = user.Id
            session['role'] = user.Role  
            flash('Login Successfull!')
            return redirect(url_for('user_dashboard'))  
        else:
            flash('Incorrect or Invaild Credentials')
            return redirect(url_for('/'))
        
    return render_template('user_login.html')


@app.route('/admin_dashboard', methods = ['GET','POST'])
def admin_dashboard():

    if 'user_id' in session and session.get('role') == 'admin':
        subjects = Subject.query.all()
        chapters = Chapter.query.all()

        return render_template('admindashboard.html', subjects = subjects, chapters = chapters)

    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))


@app.route('/createsubject', methods = ['GET','POST'])
def createsubject():

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        subject = Subject(Name=name, Description=description)
        db.session.add(subject)
        db.session.commit()
        flash("Subject Created Successfully")
        return redirect(url_for('admin_dashboard'))
    return render_template('create_subject.html')


@app.route('/editsubject/<int:subject_id>', methods = ['GET','POST'])
def editsubject(subject_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    subject = Subject.query.get_or_404(subject_id)
    if request.method == 'POST':
        subjectname= request.form['name']
        subjectdescription = request.form['description']
        subject.Name = subjectname
        subject.Description = subjectdescription
        db.session.commit()
        flash("Subject Updated Successfully")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_subject.html', subject=subject)


@app.route('/deletesubject/<int:subject_id>', methods = ['GET','POST'])
def deletesubject(subject_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))

    subject=Subject.query.get_or_404(subject_id)
    chapter = Chapter.query.filter_by(Subject_id=subject_id).all()
    quiz = Quiz.query.filter_by(Chapter_id=Chapter.Id).all()
    questions = Questions.query.filter_by(Quiz_id=Quiz.Id).all()
    scores = Scores.query.filter_by(Quiz_id=Quiz.Id).all()
    for chap in chapter:
        db.session.delete(chap)
    for q in quiz:
        db.session.delete(q)
    for ques in questions:
        db.session.delete(ques)
    for score in scores:
        db.session.delete(score)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted Successfully")
    return redirect(url_for('admin_dashboard'))


@app.route('/createchapter/<int:subject_id>', methods = ['GET','POST'])
def createchapter(subject_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        subject_id = subject_id

        chapter = Chapter(Name=name, Description=description, Subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        flash("Chapter Created Successfully")
        return redirect(url_for('admin_dashboard'))
    return render_template('create_chapter.html')


@app.route('/editchapter/<int:chapter_id>', methods = ['GET','POST'])
def editchapter(chapter_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == 'POST':
        chaptername= request.form['name']
        chapterdescription = request.form['description']
        chapter.Name = chaptername
        chapter.Description = chapterdescription
        db.session.commit()
        flash("Subject Updated Successfully")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_chap.html', chapter=chapter)


@app.route('/deletechapter/<int:chapter_id>', methods = ['GET','POST'])
def deletechapter(chapter_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))

    chapter=Chapter.query.get_or_404(chapter_id)
    quiz = Quiz.query.filter_by(Chapter_id=Chapter.Id).all()
    questions = Questions.query.filter_by(Quiz_id=Quiz.Id).all()
    scores = Scores.query.filter_by(Quiz_id=Quiz.Id).all()
    for q in quiz:
        db.session.delete(q)
    for ques in questions:
        db.session.delete(ques)
    for score in scores:
        db.session.delete(score)
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted Successfully")
    return redirect(url_for('admin_dashboard'))


@app.route('/quizdashboard', methods = ['GET','POST'])
def quizdashboard():

    if 'user_id' in session and session.get('role') == 'admin':
        quiz = Quiz.query.all()
        chapter = Chapter.query.all()
        return render_template('quizdashboard.html', quiz = quiz, chapter = chapter)

    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))


@app.route('/createquiz', methods =["GET", "POST"])
def createquiz():

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        chapterid = request.form['chapterid']
        date = request.form['date']
        duration = request.form['duration']
        remarks = request.form['remarks']

        date1 = datetime.strptime(date, '%Y-%m-%d').date()
        hours, minutes = map(int, duration.split(':'))
        duration1 = time(hours, minutes)

        quiz = Quiz(Chapter_id = chapterid, dateofquiz = date1, timeduration = duration1, remarks = remarks)
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz Created Successfully")
        return redirect(url_for('quizdashboard'))
    return render_template('create_quiz.html')


@app.route('/editquiz/<int:quiz_id>', methods = ['GET','POST'])
def editquiz(quiz_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        dateofquiz = request.form['date']
        timeduration = request.form['duration']
        remarks = request.form['remarks']

        date1 = datetime.strptime(dateofquiz, '%Y-%m-%d').date()
        hours, minutes = map(int, timeduration.split(':'))
        duration1 = time(hours, minutes)

        quiz.dateofquiz = date1
        quiz.timeduration = duration1
        quiz.remarks = remarks

        db.session.commit()
        flash("Quiz Created Successfully")
        return redirect(url_for('quizdashboard'))
    return render_template('editingquiz.html')


@app.route('/deletequiz/<int:quiz_id>', methods = ['GET','POST'])

def deletequiz(quiz_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        return redirect(url_for('login'))

    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Questions.query.filter_by(Quiz_id=Quiz.Id).all()
    scores = Scores.query.filter_by(Quiz_id=Quiz.Id).all()
    for ques in questions:
        db.session.delete(ques)
    for score in scores:
        db.session.delete(score)
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted Successfully")
    return redirect(url_for('quizdashboard'))


@app.route('/quiz/<int:quiz_id>', methods = ['GET','POST'])

def quiz(quiz_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        redirect(url_for('login'))

    else:
        questions = Questions.query.filter_by(Quiz_id=quiz_id).all()   
        return render_template('questions.html', quiz_id = quiz_id, questions = questions)


@app.route('/createques/<int:quiz_id>', methods = ['GET','POST'])
def createques(quiz_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        redirect(url_for('login'))

    if request.method == 'POST':
        question = request.form['question']
        options = request.form['options']
        answer = request.form['answer']

        question = Questions(Quiz_id = quiz_id, Question = question, Options = options, Answer = answer)
        db.session.add(question)
        db.session.commit()
        flash('Question added Successfully')
        return redirect(url_for('quiz', quiz_id = quiz_id))
    return render_template('createques.html')


@app.route('/editques/<int:ques_id>', methods = ['GET', 'POST'])
def editques(ques_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        redirect(url_for('login'))
    
    question = Questions.query.get_or_404(ques_id)
    if request.method == 'POST':
        question1 = request.form['question']
        options = request.form['options']
        answer = request.form['answer']

        question.Question = question1
        question.Options = options
        question.Answer = answer

        db.session.commit()
        flash('Question Edited Successfully')
        return redirect(url_for('quiz', quiz_id = question.Quiz_id))
    return render_template('editques.html')


@app.route('/deleteques/<int:ques_id>', methods = ["GET","POST"])
def deleteques(ques_id):

    if 'user_id' not in session and session.get('role') != 'admin':
        flash('Access denied. Admins only.')
        redirect(url_for('login'))

    question = Questions.query.get_or_404(ques_id)
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted Successfully")
    return redirect(url_for('quiz', quiz_id = question.Quiz_id))


@app.route('/user_dashboard', methods = ['GET','POST'])
def user_dashboard():

    if 'user_id' in session and session.get('role') == 'user':
        subjects = Subject.query.all()
        chapters = Chapter.query.all()
        quiz = Quiz.query.all()

        return render_template('userdashboard.html', subjects = subjects, chapters = chapters, quiz = quiz)

    else:
        flash('Access denied. LOGIN.')
        return redirect(url_for('login'))


@app.route('/quizattempt/<int:quiz_id>', methods = ["GET", "POST"])

def quizattempt(quiz_id):

    if 'user_id' not in session and session.get('role') != 'user':
        flash('Access denied. LOGIN.')
        return redirect(url_for('login'))

    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Questions.query.filter_by(Quiz_id = quiz_id).all()

    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.form.get(str(question.Id))
            if answer == str(question.Answer):
                score += 1

        user_id = session.get('user_id')
        score = Scores(Quiz_id = quiz_id, User_id = user_id, Timestampofattempt = datetime.now(), Totalscored = score)
        db.session.add(score)
        db.session.commit()
        flash('Quiz Attempted Successfully')
        return redirect(url_for('user_dashboard'))
    return render_template('quizattempt.html', quiz = quiz, questions = questions)


@app.route('/viewquiz/<int:quiz_id>', methods = ["GET", "POST"])

def viewquiz(quiz_id):

    if 'user_id' not in session and session.get('role') != 'user':
        flash('Access denied. LOGIN.')
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Questions.query.filter_by(Quiz_id = quiz_id).all()
    q = db.session.query(Questions).count()

    return render_template('viewquiz.html', quiz = quiz, questions = questions, q = q)

@app.route('/summaryuser', methods = ["GET", "POST"])
def summaryuser():
    if 'user_id' not in session and session.get('role') != 'user':
        flash("Access Denied. LOGIN.")
        return redirect(url_for('login'))







with app.app_context():
    db.create_all()
    setup_admin()
    
if __name__ == "__main__":
    app.run(debug=True)