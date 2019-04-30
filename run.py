#!/usr/bin/python3
import functools
from werkzeug.security import check_password_hash, generate_password_hash
import configparser
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import mysql.connector
from queries import*

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Create a function for fetching data from the database.
def sql_query(sql, params):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor(prepared = True)
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def sql_execute(sql, params):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor(prepared = True)
    cursor.execute(sql, params)
    db.commit()
    cursor.close()
    db.close()

def sql_execute_many(sql, params):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor(prepared = True)
    cursor.executemany(sql, params)
    db.commit()
    cursor.close()
    db.close()

# For this example you can select a handler function by
# uncommenting one of the @app.route decorators.

#@app.route('/')
def basic_response():
    return "It works!" #example

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
@login_required
def index():
    #we havent decided what these books should be, maybe books with most recently made listings?
    book = sql_query(GET_EVERY_BOOK, params = ())
    title1 = book[0][2].decode("utf-8") 
    subject1 = book[0][1].decode("utf-8")
    description1 = book[0][5].decode("utf-8")
    isbn1 =book[0][0].decode("utf-8")
    author1 = book[0][4].decode("utf-8")

    title2 = book[1][2].decode("utf-8") 
    subject2 = book[1][1].decode("utf-8")
    description2 = book[1][5].decode("utf-8")
    isbn2 =book[1][0].decode("utf-8")
    author2 = book[1][4].decode("utf-8")

    title3 = book[2][2].decode("utf-8") 
    subject3 = book[2][1].decode("utf-8")
    description3 = book[2][5].decode("utf-8")
    isbn3 =book[2][0].decode("utf-8")
    author3 = book[2][4].decode("utf-8")

    placeholder_books=[{'title': title1 , 'subject': subject1, 'description': description1,'isbn':isbn1, 'author':author1},
        {'title': title2 , 'subject': subject2, 'description': description2,'isbn':isbn2, 'author':author2},
        {'title': title3 , 'subject': subject3, 'description': description3,'isbn':isbn3, 'author':author3}]

    return render_template('home.html', books=placeholder_books)

@app.route('/search')
@login_required
def search():

    if ('query' in request.args and request.args.get('query')):
        search_query = request.args.get('query')
        # these books should be every book in the DB that contains "search_query",
        # either in the name or description, based on how much it shows up

        book_search = sql_query(GET_BOOK_TITLE, params=(search_query, ))
        listofbooks = []

        for x in book_search:
            sample_book = {}
            sample_book["title"] = x[0].decode("utf-8")
            sample_book["subject"] = x[1].decode("utf-8")
            sample_book["description"] = x[2].decode("utf-8")
            sample_book["isbn"] = x[3].decode("utf-8")
            sample_book["author"] = x[4].decode("utf-8")
            listofbooks.append(sample_book)

        # placeholder_books = [
        #     {'title': listing_books[0][0], 'subject': listing_books[0][1], 'description': listing_books[0][2],
        #      'isbn': 123456, 'authors': [{'author_name': 'Author'}]},
        #     {'title': 'Book Search Result 2', 'subject': 'Physics', 'description': 'Same', 'isbn': 123123123,
        #      'authors': [{'author_name': 'Author'}]},
        #     {'title': 'Book Search Result 3', 'subject': 'English', 'description': 'yeet', 'isbn': 789789789,
        #      'authors': [{'author_name': 'Author'}]},
        #     {'title': 'Book Search Result 4', 'subject': 'a subject', 'description': 'a description', 'isbn': 456456456,
        #      'authors': [{'author_name': 'Author'}]}]
        return render_template('search.html', books=listofbooks, query=search_query)
    else:
        return redirect(url_for('index'))


@app.route('/book-listings/<int:isbn>', methods=('GET', 'POST'))
@login_required
def book_listings(isbn):
    if request.method == 'GET':
        #get book based on 'isbn'. Make sure this includes an array of all the authors
        book_result = sql_query(GET_BOOK_ISBN, params=(isbn,))
        title = book_result[0][0].decode("utf-8")
        subject = book_result[0][1].decode("utf-8")
        description = book_result[0][2].decode("utf-8")
        author = book_result[0][4].decode("utf-8")

        book_details={'title': title, 'subject': subject, 'description': description,
            'isbn': isbn, 'author': author}
        # listings of 'isbn' that are available. Make sure this includes the username of the user who made the listing

        listing_search = sql_query(GET_LISTING_BOOK_ISBN, params=(isbn,))
        listoflistings = []
        for x in listing_search:
            sample_listing = {}
            sample_listing["listing_id"] = x[0]
            sample_listing["price"] = x[1].decode("utf-8")
            sample_listing["listing_condition"] = x[2].decode("utf-8")
            sample_listing["username"] = x[3]
            listoflistings.append(sample_listing)



        #User's unordered baskets
        baskets=[{'order_basket_id':149872},{'order_basket_id': 476343},{'order_basket_id':345645}]


        return render_template('book-listings.html', book=book_details, listings=listoflistings, baskets=baskets)

    elif request.method == 'POST':
        l_id = request.form['listing_id']
        ob_id = request.form['order_basket_id']
        status = 'SOLD'
        #add listing_id to order_basket with id=order_basket_id
        vals = (ob_id,status,l_id)
        sql_execute(UPDATE_LISTING, params=vals)
        return redirect(url_for('account'))

@app.route('/make-listing', methods=('GET', 'POST'))
@login_required
def make_listing():
    if request.method == 'GET':
        return render_template('make-listing.html')
    elif request.method == 'POST':
        isbn = request.form['isbn']
        price = request.form['price']
        listing_condition = request.form['listing_condition']
        #add this listing to DB (get user from g.user['id'])

        bookCount = sql_query(GET_NUMISBN, params = (isbn, ))
        # this should check if a book with ISBN 'isbn' already exists
        if (bookCount[0])[0] > 0:
            user_id = sql_query(RETURN_USER, params=(g.user['id']))[0][2]
            sql_execute(INSERT_LISTING, params = (price, 'selling', listing_condition, user_id, isbn))
            return redirect(url_for('book_listings', isbn=isbn))
        else:
            return redirect(url_for('add_book', isbn = isbn, price=price, listing_condition=listing_condition))

@app.route('/add-book/<isbn>/<price>/<listing_condition>', methods=('GET', 'POST'))
@login_required
def add_book(isbn, price, listing_condition):
    if request.method == 'GET':
        return render_template('add-book.html', isbn=isbn, price=price, listing_condition=listing_condition)
    elif request.method == 'POST':
        subject = request.form['subject']
        title = request.form['title']
        author = request.form['authors']
        publisher = request.form['publisher'] 
        description = request.form['description']
        vals = (isbn, subject, title, publisher, author, description)

        sql_execute(INSERT_BOOK, params = vals)
        #add this new book to DB

        #insert listing
        sql_execute(INSERT_LISTING, params=(price, 'SELLING', listing_condition, 1, isbn))

        return redirect(url_for('book_listings', isbn=isbn))

@app.route('/new-order', methods=('GET', 'POST'))
@login_required
def new_order():
    if request.method == 'GET':
        return render_template('new-order.html')
    elif request.method == 'POST':
        address = request.form['address']
        #add new order basket for user at given address
        sql_execute(INSERT_ORDER_BASKET, params=(1, address, 'OPEN'))

        return redirect(url_for('account'))

@app.route('/account')
@login_required
def account():
    user_details = {'username':g.user['id']}

    listing_search = sql_query(MATCH_LISTING_USERID, params=(g.user['id'],))
    listings = []
    for x in listing_search:
        sample_listing = {}
        sample_listing["listing_id"] = x[0]
        sample_listing["price"] = x[1].decode("utf-8")
        sample_listing["listing_condition"] = x[2].decode("utf-8")
        sample_listing["title"] = x[3].decode("utf-8")
        sample_listing["listing_status"] = x[4].decode("utf-8")
        listings.append(sample_listing)


    # listings=[{'listing_id':123123123,'price': '$20', 'listing_condition': 'New', 'title': 'Placeholder Title 1', 'listing_status':'Listed'},
    #     {'listing_id':456456456,'price': '$10', 'listing_condition': 'Used - Good','title': 'Placeholder Title 2','listing_status':'Ordered'},
    #     {'listing_id':789789789,'price': '$15', 'listing_condition': 'Used - Like New','title': 'Placeholder Title 3','listing_status':'Delivered'}]
    order_baskets = [{'order_basket_id': 12345, 'date_made': '4/17/19', 'address': '1234 Road Rd.','order_basket_status': 'Not Ordered',
        'listings':[{'listing_id':135135135,'price': '$21', 'listing_condition': 'New', 'username': 'user1', 'title': 'Placeholder Title 4'}]},
        {'order_basket_id': 67890, 'date_made': '1/17/19', 'address': '3456 Street St.','order_basket_status': 'Delivered',
        'listings':[{'listing_id':246246246,'price': '$42', 'listing_condition': 'User - Very Good', 'username': 'user2', 'title': 'Placeholder Title 5'},
                    {'listing_id':369369369,'price': '$12', 'listing_condition': 'User - Good', 'username': 'user3', 'title': 'Placeholder Title 6'}]}]
    return render_template('account.html', user_details=user_details,listings=listings,order_baskets=order_baskets)

#@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    print(request.form)
    if "buy-book" in request.form:
        book_id = int(request.form["buy-book"])
        sql = "delete from book where id={book_id}".format(book_id=book_id)
        sql_execute(sql)
    template_data = {}
    sql = "select id, title from book order by title"
    books = sql_query(sql)
    template_data['books'] = books
    return render_template('home-w-data.html', template_data=template_data)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        existing_user = sql_query(RETURN_USER, params=(username, ))

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif existing_user:
            #This should check if a user with that name already exists
            error = 'User {} is already registered.'.format(username)
        if error is None:
            sql_execute(INSERT_USER, params=(username, password))
            return redirect(url_for('login'))

        flash(error)

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        #check if 'username' exists in db and save results as 'user'
        user = sql_query(RETURN_USER, params=(username, ))
        if not user:
            error = 'Incorrect username.'
        elif user[0][1].decode("utf-8") != password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0][0].decode("utf-8")
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.before_request
def load_logged_in_user():
    username = session.get('user_id')

    if username is None:
        g.user = None
    else:
        #make sure user_id is in the database and add it as g.user['id']
        user = sql_query(RETURN_USER, params=(username, ))
        if user:
            g.user = {'id': user[0][0].decode("utf-8")}
        else:
            g.user = None

if __name__ == '__main__':
    app.run(**config['app'])

#1a
def getISBNTitle(title):
    return sql_query(GET_ISBN_TITLE, title)
#1b
def getTitleISBN(isbn):
    return sql_query(GET_TITLE_ISBN, isbn)

#4
def getNumISBN(isbn):
    return sql_query(GET_ISBNCOUNT, ISBN)

#7
def insertAuthor(author_id, author_name):
    return sql_query(INSERT_AUTHOR, (author_id, author_name))

#10
def matchUserIDOrderBasket(user_id):
    return sql_query(MATCH_USER_ORDER_BASKET,user_id)

#13
def matchISBNAuthorName(isbn):
    return sql_query(MATCH_ISBN_AUTHORNAME,isbn)

#16
def getNumListings(isbn):
    return sql_query(GET_NUMLISTINGS, isbn)

#19
def insertPublisher(pub_id, pub_name):
    return sql_query(INSERT_PUBLISHER, pub_id, pub_name)

#2
def insertUser(user_id, username, password):
    return sql_query(INSERT_USER, user_id, username, password)
#5
def buyBook(listing_id):
    return sql_query(BUY_BOOK, listing_id)
#8
def insertListing(listing_id, price, listing_status, listing_condition, user_id, order_basket_id, book_isbn):
    return sql_query(INSERT_LISTING, listing_id, price, listing_status, listing_condition, user_id, order_basket_id, book_isbn)
#11
def matchOrderBasketListing(order_basket_id):
    return sql_query(MATCH_ORDER_BASKET_LISTING, order_basket_id)
#14
def matchPublisherBook(pub_id):
    return sql_query(MATCH_PUBLISHER_BOOK, pub_id);
#17
def sortLowestPrice(book_isbn):
    return sql_query(SORT_LOWEST_PRICE, book_isbn)
#6
def insertPublisher(pub_id, pub_name):
    return sql_query(INSERT_PUBLISHER, pub_id, pub_name)

#3
def insertBook(isbn, subject, title, description, pub_id):
    return sql_query(INSERT_BOOK, isbn, subject, title, description, pub_id)
#9
def insertOrderBasket(order_basket_id, user_id, address, date_made, order_basket_status):
    return sql_query(INSERT_ORDER_BASKET, order_basket_id, user_id, address, date_made, order_basket_status)

#12
def matchOrderUser(order_basket_id):
    return sql_query(MATCH_ORDER_USER, order_basket_id)

#15
def matchBookListingID(isbn):
    return sql_query(MATCH_BOOK_LISTING_ID, isbn)


#18
def sumOrderBasket(listing_id):
    return sql_query(SUM_ORDER_BASKET, listing_id)




