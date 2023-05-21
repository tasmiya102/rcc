from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy




import numpy as np
import pickle



app = Flask(__name__)
model = pickle.load(open('Kidney.pkl', 'rb'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/contact'
db=SQLAlchemy(app)   

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=False)
    number = db.Column(db.String(12),  nullable=False)
    message = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=True)



@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/index',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry = Contacts(name=name, number=phone,message=message,email=email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')


@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')
@app.route('/blog',methods=['GET'])
def blog():
    return render_template('blog.html')

@app.route('/form_login',methods=['POST'])
def form():
    title= "Thank You!"
    return render_template('form.html', title=title)



@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        sg = float(request.form['sg'])
        htn = float(request.form['htn'])
        hemo = float(request.form['hemo'])
        dm = float(request.form['dm'])
        al = float(request.form['al'])
        appet = float(request.form['appet'])
        rc = float(request.form['rc'])
        pc = float(request.form['pc'])

        values = np.array([[sg, htn, hemo, dm, al, appet, rc, pc]])
        prediction = model.predict(values)

        return render_template('result.html', prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)

