
from flask import Flask, render_template, request, redirect, url_for,session
from datetime import datetime
from flask_session import Session
from model import *




app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
url="postgresql://wglgundawjelqj:e9d1544596fffeadc069bf27eb34ec4fa810d4d76772664261eac0e37c303c03@ec2-107-20-153-39.compute-1.amazonaws.com:5432/d47b6lteda8844"
app.config["SQLALCHEMY_DATABASE_URI"] = url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def first():
    db.create_all()

with app.app_context():
    first()


@app.route("/")
def home():
    session.pop('username',None)
    return render_template("home.html")




@app.route("/login",methods=["GET", "POST"])
def login():
    if(request.method=="POST"):
        email=request.form.get("email")
        password=request.form.get("password")
        users=User.query.all()
        print(email,password)
        print(users)

        for user in users:
            e=user.email
            pwd=user.password
            u=user.username
            print(e,pwd)
            if(email==e) and(password==pwd):
                session['username']=u
                print(u)
                return render_template("searchbook.html")
            
        error="Invalid username and password"
        return render_template("login.html",error=error)
    else:
        return render_template("login.html")
    # return redirect(url_for('hello'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if(request.method=="POST"):
        uname = request.form.get("uname")
        email = request.form.get("email")
        password = request.form.get("password")
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        time=datetime.now()
        users=User.query.all()
        
        for user in users:
            u=user.username
            e=user.email
            if(email==e) or (uname==u):
                d="username or email is already Registered"
                # (return render_template("register.html",error=d)  )
                
        # print(uname,email,password)
        row=User(username=uname,email=email,password=password,timestamp=time)
        db.session.add(row)
        db.session.commit()

        return render_template("register.html",uname=uname)
    else:
        error="Invalid Username or password"
        return render_template("register.html",error=error)

@app.route('/admin')
def admin():
    return render_template("admin.html",users=User.query.all())

@app.route("/search",methods=["POST"])
def search():
    s=request.form.get("search")
    print(s)
    usr_isbn=Books.query.filter(Books.isbn.ilike('%'+s+'%')).all()
    usr_title=Books.query.filter(Books.title.ilike('%'+s+'%')).all()
    usr_author=Books.query.filter(Books.author.ilike('%'+s+'%')).all()
    usr_year=Books.query.filter(Books.year.ilike('%'+s+'%')).all()
    # print(usr_isbn)

    books=usr_isbn+usr_title+usr_author+usr_year
    return render_template('searchbook.html',books=books)

@app.route('/rr/<isbn>',methods=['GET',"POST"])
def rr(isbn):
    usr_isbn=Books.query.filter(Books.isbn==isbn).first()
    
    if request.method=="POST":
        if('reviewsubmit' in request.form):
            review=request.form.get("reviewdata")
            rating=request.form.get("ratingdata")
            name=session['username']
            print(name)
            print(rating)
            print(review)

            data=Review(isbn=isbn,name=name,review=review,rating=rating)
            db.session.add(data)
            db.session.commit()
            if 'rsubmit' in request.form:
                usr_isbn=Books.query.filter(Books.isbn==isbn).first()
                print(usr_isbn.title)
                t=usr_isbn.title
                i=usr_isbn.isbn
                a=usr_isbn.author
                y=usr_isbn.year
                
                s=Shelf(isbn=i,title=t,author=a,year=y)
                print(s)
                db.session.add(s)
                db.session.commit()
                return render_template("search.html")
        
        r=Review.query.filter(Review.isbn==isbn)
        print(r)
        return render_template("rr.html",book=usr_isbn,reviews=r)
    else:
        r=Review.query.filter(Review.isbn==isbn)

        return render_template("rr.html",book=usr_isbn,reviews=r)

@app.route('/bookshelf')
def bookshelf():
    
    return render_template("bookshelf.html",users=Shelf.query.all())

# @app.route('/bookdata/<isbn>',methods=['POST'])
# def shelf(isbn):

    

