import os
from flask import Flask, render_template, request, redirect, url_for
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/path/to/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            
db = SQLAlchemy(app)



class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    url_for('uploaded_file', filename=filename)/uploads/filenameuploaded_file()
    return render_template('index.html', posts=posts)
    

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    


    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
