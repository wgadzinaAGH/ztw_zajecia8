from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    borrowed_books = db.relationship('Borrow', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    borrows = db.relationship('Borrow', backref='book', lazy=True)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)

with app.app_context():
    db.create_all()
    book1 = Book(title="Pan Tadeusz", author="Adam Mickiewicz")
    book2 = Book(title="Lalka", author="Bolesław Prus")
    book3 = Book(title="Krzyżacy", author="Henryk Sienkiewicz")
    db.session.add_all([book1, book2, book3])
    db.session.commit()

@app.route('/')
def book_list():
    available_books = Book.query.filter_by(is_available=True).all()
    return render_template('books.html', books=available_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        if not title or not author:
            flash("Tytuł i autor są wymagane!", "danger")
        else:
            new_book = Book(title=title, author=author)
            db.session.add(new_book)
            db.session.commit()
            flash(f"Książka '{title}' została dodana!", "success")
            return redirect(url_for('book_list'))
    return render_template('add_book.html')

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        
        borrow = Borrow(user_id=user.id, book_id=book.id, borrow_date=date.today())
        book.is_available = False
        db.session.add(borrow)
        db.session.commit()
        
        flash(f"Książka '{book.title}' została wypożyczona przez {username}.", "success")
        return redirect(url_for('book_list'))
    
    return render_template('borrow.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)

####

# simple_page = Blueprint('simple_page', __name__)
# app.register_blueprint(simple_page)

# @app.route('/home')
# def home():
#     return "Witaj na stronie głównej!"

####

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Nie znaleziono'}), 404)

# @app.route('/not_exist')
# def not_exist():
#     pass

# if __name__ == '__main__':
#     app.run(debug=True)


# @app.route('/')
# def about():
#     return render_template('about.html', name='Wojciech', surname='Gadzina', age='23')     

# chapters = {
#     1: "Oto rozdział pierwszy Pana Tadeusza...",
#     2: "Oto rozdział drugi Pana Tadeusza...",
#     3: "Oto rozdział trzeci Pana Tadeusza...",
#     4: "Oto rozdział czwarty Pana Tadeusza...",
#     5: "Oto rozdział piąty Pana Tadeusza...",
#     6: "Oto rozdział szósty Pana Tadeusza...",
#     7: "Oto rozdział siódmy Pana Tadeusza...",
#     8: "Oto rozdział ósmy Pana Tadeusza...",
#     9: "Oto rozdział dziewiąty Pana Tadeusza...",
#     10: "Oto rozdział dziesiąty Pana Tadeusza...",
#     11: "Oto rozdział jedenasty Pana Tadeusza...",
#     12: "Oto rozdział dwunasty Pana Tadeusza...",
# }

# @app.route("/chapter/<int:chapter_id>")
# def index(chapter_id=None):
#     if chapter_id is None or chapter_id not in chapters:
#         selected_text = "Wybierz rozdział z menu po lewej stronie."
#     else:
#         selected_text = chapters[chapter_id]

#     return render_template("index.html", chapter_text=selected_text)

# if __name__ == '__main__':
#     app.run(debug=True)

