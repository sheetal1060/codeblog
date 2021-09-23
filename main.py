from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime



with open('config.json', 'r') as c:
    parameter = json.load(c)['parameter']

local_server = True
app = Flask(__name__)
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = parameter['gmail-user'],
    MAIL_PASSWORD = parameter['gmail-password']

)
mail=Mail(app)
print(mail.connect())
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_uri']
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(13),  nullable=False)
    phone_num= db.Column(db.String(80),  nullable=False)
    mes = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20),  nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(20),  nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20),  nullable=False)


@app.route('/')
def home():
    return render_template('index.html', parameter = parameter)

@app.route('/post/<string:post_slug>',methods=['GET'])
def post(post_slug):
    post=Posts.query.filter_by(slug =post_slug).first()
    return render_template('post.html',parameter = parameter,post=post)

@app.route('/about')
def about():
    return render_template("about.html",parameter = parameter)

@app.route('/contact', methods=['GET','POST'])
def contact():
    if (request.method == "POST"):
        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name,email=email,phone_num=phone,mes=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from Blog '+ name , sender=email, recipients=[parameter['gmail-user']],
                          body = message +"\n"+ phone
                          )

    return render_template('contact.html',parameter = parameter)

app.run(debug=True)
