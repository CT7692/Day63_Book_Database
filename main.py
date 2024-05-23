from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import Integer, String, Float, select, func
from tkinter import messagebox

app = Flask(__name__)

class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    __tablename__ = "Books"
    id: Mapped[int] = mapped_column(primary_key=True, name="ID")
    title: Mapped[str] = mapped_column(unique=True, nullable=False, name="Title")
    author: Mapped[str] = mapped_column(nullable=False, name="Author")
    rating: Mapped[float] = mapped_column(nullable=False, name="Rating")

with app.app_context():
        db.create_all()


@app.route('/')
def home():
    with Session(app):
        count = db.session.query(Book).count()
        result = db.session.execute(select(Book).order_by(Book.title))
        books = result.scalars()
    return render_template("index.html", books=books, count=count)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with Session(app):
            book = Book(title=request.form['title'],author=request.form['author'],rating=request.form['rating'])
            db.session.add(book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(**kwargs):
    with Session(app):
        id = kwargs['id']
        desired_book  = db.get_or_404(Book, id)

        if request.method == 'POST':
            desired_book.rating = request.form['new_rating']
            db.session.commit()
            return redirect(url_for('home'))

    return render_template("edit.html", book=desired_book)

@app.route("/delete/<int:id>", methods=['GET'])
def delete(**kwargs):
    with Session(app):
        id = kwargs['id']
        undesired_book = db.get_or_404(Book, id)
        db.session.delete(undesired_book)
        db.session.commit()
    return  redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

