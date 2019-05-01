#!/usr/bin/python3
import functools
from werkzeug.security import check_password_hash, generate_password_hash
import werkzeug.exceptions
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

# A function that changes data in the databases 
def sql_execute(sql, params):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor(prepared = True)
    cursor.execute(sql, params)
    db.commit()
    cursor.close()
    db.close()


# A function that redirects user to the login page

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# Home page. Displays the first 3 books in the database. 
@app.route('/')
@login_required
def index():
    # Query to get every book in the database. 
    book = sql_query(GET_EVERY_BOOK, params = ())

    # Selects the top 3 book and displays the title, subject,description,isbn, author
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

# Returns the book based on its title. 
@app.route('/search')
@login_required
def search():

    if ('query' in request.args and request.args.get('query')):
        search_query = request.args.get('query')
        # these books should be every book in the DB that contains "search_query",
        # either in the name or description, based on how much it shows up

        # User will search for a book based on its title. Shows all the book with the same title. 
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
        #      'authors': [{'author_name': 'Author'}]}]
        return render_template('search.html', books=listofbooks, query=search_query)
    else:
        return redirect(url_for('index'))

# List all the current listings for a specific book based on the book's isbn. 
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

        # Based on the book isbn, return the listings for the specific book.
        listing_search = sql_query(GET_LISTING_BOOK_ISBN, params=(isbn,))
        listoflistings = []
        for x in listing_search:
            sample_listing = {}
            sample_listing["listing_id"] = x[0]
            sample_listing["price"] = x[1].decode("utf-8")
            sample_listing["listing_condition"] = x[2].decode("utf-8")
            sample_listing["username"] = sql_query(GET_USER_FROM_ID, params=(x[3], ))[0][0].decode("utf-8")
            listoflistings.append(sample_listing)

        #User's unordered baskets
        baskets = sql_query(MATCH_USER_ORDER_BASKET_UNORDERED, params=(g.user['id'], ))

        return render_template('book-listings.html', book=book_details, listings=listoflistings, baskets=baskets)

    # When a user is adding to basket, they will be redirected to the accounts page. Order basket will show the listing.
    elif request.method == 'POST':
        l_id = request.form['listing_id']
        ob_id = request.form['order_basket_id']
        #add listing_id to order_basket with id=order_basket_id
        vals = (ob_id,l_id)
        sql_execute(UPDATE_LISTING, params=(ob_id, l_id))
        return redirect(url_for('account'))

# When a user does not have a order basket yet, they will be redirecred to their accounts page and they can open an order basket. 
@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return redirect(url_for('account'))

# Make listing for a book. 
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
            # If it doesn't exist, it will insert new listing to the database. 
            sql_execute(INSERT_LISTING, params = (price, 'SELLING', listing_condition, g.user['id'], isbn))
            return redirect(url_for('book_listings', isbn=isbn))
        else:
            return redirect(url_for('add_book', isbn = isbn, price=price, listing_condition=listing_condition))

# Add a book if it does not exist in the database. 
@app.route('/add-book/<isbn>/<price>/<listing_condition>', methods=('GET', 'POST'))
@login_required
def add_book(isbn, price, listing_condition):
    if request.method == 'GET':
        return render_template('add-book.html', isbn=isbn, price=price, listing_condition=listing_condition)

    # Insert a book given the user input. 
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
        sql_execute(INSERT_LISTING, params=(price, 'SELLING', listing_condition, g.user['id'], isbn))

        return redirect(url_for('book_listings', isbn=isbn))

# When a user creates a new order. 
@app.route('/new-order', methods=('GET', 'POST'))
@login_required
def new_order():
    if request.method == 'GET':
        return render_template('new-order.html')
    elif request.method == 'POST':
        # Ask the user for their home address
        address = request.form['address']
        # add new order basket for user at given address. 
        sql_execute(INSERT_ORDER_BASKET, params=(g.user['id'], address, 'OPEN'))

        return redirect(url_for('account'))

@app.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    if request.method == 'POST':
        basket_id=request.form['order_basket_id']
        sql_execute(BUY_ORDER_BASKET,params=(basket_id, ))
        listings = sql_query(GET_LISTING_ORDER_BASKET_ID, params=(basket_id, ))
        for listing in listings:
            sql_execute(BUY_LISTING,params=(listing[0], ))

        sql_execute(DELETE_ORDER_BASKET, params=(basket_id, ))
        return redirect(url_for('account'))

    user_details = {'username':g.user['id']}

    listing_search = sql_query(MATCH_LISTING_USERID, params=(g.user['id'], ))
    listings = []
    for x in listing_search:
        sample_listing = {}
        sample_listing["listing_id"] = x[0]
        sample_listing["price"] = x[1].decode("utf-8")
        sample_listing["listing_condition"] = x[2].decode("utf-8")
        sample_listing["title"] = x[3].decode("utf-8")
        sample_listing["listing_status"] = x[4].decode("utf-8")
        listings.append(sample_listing)



    user_order_basket_search = sql_query(GET_ORDER_BASKET_USER_ID, params=(g.user['id'], ))
    order_baskets = []
    for x in user_order_basket_search:
        sample_order_basket = {}
        sample_order_basket["order_basket_id"] = x[0]
        sample_order_basket["address"] = x[1].decode("utf-8")
        sample_order_basket["order_basket_status"] = x[2].decode("utf-8")
        listing_order_basket_search = sql_query(GET_LISTING_ORDER_BASKET_ID, params=(x[0], ))

        sample_order_basket["listings"] = []
        for y in listing_order_basket_search:
            sample_listing_order_basket = {}
            sample_listing_order_basket["listing_id"] = y[0]
            sample_listing_order_basket["price"] = y[1].decode("utf-8")
            sample_listing_order_basket["listing_condition"] = y[2].decode("utf-8")
            sample_listing_order_basket["username"] = y[3]
            title = sql_query(GET_TITLE_ISBN, params= (y[4].decode("utf-8"), ))
            sample_listing_order_basket["title"] = title[0][0].decode("utf-8")
            sample_order_basket["listings"].append(sample_listing_order_basket)
        order_baskets.append(sample_order_basket)

    unordered_baskets = sql_query(MATCH_USER_ORDER_BASKET_UNORDERED, params=(g.user['id'], ))
   
    user_details = {'username': sql_query(GET_USER_FROM_ID, params=(g.user['id'], ))[0][0].decode("utf-8")}
    return render_template('account.html', user_details=user_details,listings=listings,order_baskets=order_baskets,unordered_baskets=unordered_baskets)

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
            session['user_id'] = user[0][2]
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        #make sure user_id is in the database and add it as g.user['id']
        user = sql_query(GET_USER_FROM_ID, params=(user_id, ))
        if user:
            g.user = {'id': user[0][2]}
        else:
            g.user = None

if __name__ == '__main__':
    app.run(**config['app'])

