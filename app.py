from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Subject, Chapter, Quiz, Questions, Scores
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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



@app.route('/login', methods = ['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #ADMIN
        admin_user = User.query.filter_by(Username=username, Role='admin').first()

        if admin_user and check_password_hash(admin_user.Password, password):
            session['user_id'] = admin_user.Id
            session['role'] = admin_user.Role  
            flash('Admin login successful!')
            return redirect(url_for('admin_dashboard'))  
        else:
            flash('Invalid credentials. Please try again.')

        #USER












    
    return render_template('user_login.html')



@app.route('/admin_dashboard', methods = ['GET','POST'])
def admin_dashboard():

    if 'user_id' in session and session.get('role') == 'admin':
        subjects = Subject.query.all()
        chapters = Chapter.query.all()


        return render_template('admindashboard.html', subjects = subjects)

    else:
        flash('Access denied. Admins only.')
        return redirect(url_for('admin_login'))



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
    for chap in chapter:
        db.session.delete(chap)
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
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted Successfully")
    return redirect(url_for('admin_dashboard'))






























with app.app_context():
    db.create_all()
    setup_admin()
    
if __name__ == "__main__":
    app.run(debug=True)