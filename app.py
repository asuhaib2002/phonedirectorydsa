from datetime import datetime
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import linked_list

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dlifydrsectuyq:0f9b4424ae8f55ecc5cc2156ef647e7386abf7006d606414d5770a9fdaba3ba3@ec2-54-87-179-4.compute-1.amazonaws.com:5432/dejq2c7lc3ktan'
app.config['SECRET_KEY'] = 'b21dc07d19eba5e6f64f026f'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    number = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(200), nullable = True)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"


@app.route('/', methods = ['GET', 'POST'])
def add_user_page():
    if request.method =='POST':
        name =(request.form['name'])
        number =(request.form['number'])
        email =(request.form['email'])

        user = User(name=name, number=number, email=email)
        db.session.add(user)
        db.session.commit()
    return render_template('index.html')

@app.route("/displaydecending", methods=["GET"])
def display_decending_page():
    users = User.query.all()
    users_ll = linked_list.LinkedList()

    for user in users:
        users_ll.insert_beginning(
            {
                "sno": user.sno,
                "name": user.name,
                "number":user.number,
                "email": user.email,             
            }
        )
    decending_users = users_ll.to_list() 
    return render_template('display_decending.html', decending_users=decending_users) 

@app.route("/display", methods=["GET"])
def display_page():
    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
               "sno": user.sno,
                "name": user.name,
                "number":user.number,
                "email": user.email,
            }
        )

    assending_users = all_users_ll.to_list() 
    return render_template('display.html', assending_users=assending_users) 

@app.route("/update/<int:sno>", methods =['GET','POST'])
def update(sno):
    if request.method == 'POST':
        name =(request.form['name'])
        number =(request.form['number'])
        email =(request.form['email'])
        user = User.query.filter_by(sno=sno).first()
        user.name = name
        user.number = number
        user.email = email
        db.session.add(user)

        db.session.commit()
        return redirect('/')
    user = User.query.filter_by(sno=sno).first()
    return render_template('update.html', user=user) 

@app.route("/delete/<int:sno>")
def delete(sno):
    user = User.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/displaydecending")


if __name__ == "__main__":
    app.run(debug=True)