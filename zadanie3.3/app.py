import json

from flask import Flask, render_template, session, redirect
from flask_bs4 import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
date = datetime.now()
app.config['SECRET_KEY'] = 'fghj678%^&TYU^&*6789yu&*(HJK'

class LoginForm(FlaskForm):
    userLogin = StringField('Nazwa użytkownika:', validators=[DataRequired()])
    userPass = PasswordField('Hasło:', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')

users = {
    1: {
        'userLogin': 'janek',
        'userPass': 'zaq1@WSX',
        'fname': 'Gospodarek',
        'lname': 'Jan'
    }
}
print(users)
def countAverage(subjectValue, termValue):
    """funkcja obliczająca średnią ocen"""
    with open('data/grades.json', encoding='utf-8') as file:
        grades = json.load(file)
        file.close()
    totlaSum = 0
    totalLen = 0
    if subjectValue == '' and termValue == '':
        for subject, terms in grades.items():
            for term, categories in terms.items():
                for category, grades in categories.items():
                    if category == 'answer' or category == 'quiz' or category == 'test':
                        for grade in grades:
                            totlaSum += grade
                            totalLen += 1
    else:
        for subject, terms in grades.items():
            if subject == subjectValue:
                for term, categories in terms.items():
                    if term == termValue:
                        for category, grades in categories.items():
                            if category == 'answer' or category == 'quiz' or category == 'test':
                                for grade in grades:
                                    totlaSum += grade
                                    totalLen += 1
    return round(totlaSum / totalLen, 2)


def yearlyAverage(value):
    with open('data/grades.json', encoding='utf-8') as file:
        grades = json.load(file)
        file.close()
    sum = 0
    len = 0
    for subject, terms in grades.items():
        if subject == value:
            for term, categories in terms.items():
                for category, grades in categories.items():
                    if category == 'answer' or category == 'quiz' or category == 'test':
                        for grade in grades:
                            sum += grade
                            len += 1
    return round(sum / len, 2)


subjects=[]



with open('data/grades.json', encoding='utf-8') as file:
    grades = json.load(file)
    file.close()
for subject,val in grades.items():
    grade=yearlyAverage(subject)
    subjects.append({'subject':subject,'grade':grade})
subjects.sort(key=lambda x: x['grade'], reverse=True)

bestGrades=[subjects[0],subjects[1]]

danger=[]
for subs in subjects:
    if subs['grade']<2.50:
        danger.append(subs['subject'])
        danger.append(subs['grade'])
print(danger)



@app.route('/')
def index():
    return render_template('index.html', title='Strona główna')

@app.route('/logIn', methods=['POST', 'GET'])
def logIn():
    login = LoginForm()
    if login.validate_on_submit():
        userLogin = login.userLogin.data
        userPass = login.userPass.data
        if userLogin == users[1]['userLogin'] and userPass == users[1]['userPass']:
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template('login.html', title='Logowanie', login=login, userLogin=session.get('userLogin'))

@app.route('/logOut')
def logOut():
    session.pop('userLogin')
    return redirect('logIn')

@app.route('/dashboard')
def dashboard():
    with open('data/grades.json', encoding='utf-8') as file:
        grades = json.load(file)
        file.close()
    return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'), date=date,
                           grades=grades, countAverage=countAverage, yearlyAverage=yearlyAverage,
                           dangers=danger,bestGrades=bestGrades)

if __name__ == '__main__':
    app.run(debug=True)

# e-szkolenia.net