#!/usr/bin/python3
import configparser
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from queries import*

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__)

# Create a function for fetching data from the database.
def sql_query(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def sql_execute(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

# For this example you can select a handler function by
# uncommenting one of the @app.route decorators.

#@app.route('/')
def basic_response():
    return "It works!" #example

@app.route('/')
def index():
    #we havent decided what these books should be, maybe books with most recently made listings?
    placeholder_books=[{'title': 'Featured Book Title 1', 'subject': 'Math', 'description': 'This is a placeholder','isbn':789789789, 'authors':[{'author_name': 'Author'}]},
        {'title': 'Featured Book Title 2', 'subject': 'Physics', 'description': 'This is also a placeholder','isbn':123123123, 'authors':[{'author_name': 'Author'}]},
        {'title': 'Featured Book Title 3', 'subject': 'English', 'description': 'Another placeholder','isbn':456456456, 'authors':[{'author_name': 'Author'}]}]
    return render_template('home.html', books=placeholder_books)

@app.route('/search')
def search():
    if('query' in request.args and request.args.get('query')):
        search_query=request.args.get('query')
        #these books should be every book in the DB that contains "search_query",
        #either in the name or description, based on how much it shows up
        placeholder_books=[{'title': 'Book Search Result 1', 'subject': 'Math', 'description': 'This is a placeholder search result','isbn':123456, 'authors':[{'author_name': 'Author'}]},
        {'title': 'Book Search Result 2', 'subject': 'Physics', 'description': 'Same','isbn':123123123 , 'authors':[{'author_name': 'Author'}]},
        {'title': 'Book Search Result 3', 'subject': 'English', 'description': 'yeet','isbn':789789789, 'authors':[{'author_name': 'Author'}]},
        {'title': 'Book Search Result 4', 'subject': 'a subject', 'description': 'a description','isbn':456456456, 'authors':[{'author_name': 'Author'}]}]
        return render_template('search.html', books=placeholder_books, query=search_query)
    else:
        return redirect(url_for('index'))

@app.route('/book-listings/<int:isbn>', methods=('GET', 'POST'))
def book_listings(isbn):
    if request.method == 'GET':
        #get book based on 'isbn'. Make sure this includes an array of all the authors
        book_details={'title': 'Placeholder Book', 'subject': 'Math', 'description': 'This is a placeholder book listings page',
            'isbn': isbn, 'authors':[{'author_name': 'Author 1'}, {'author_name': 'Author 2'}]}
        # listings of 'isbn' that are available. Make sure this includes the username of the user who made the listing
        listings=[{'listing_id':123123123,'price': '$20', 'listing_condition': 'New', 'username': 'user1'},
        {'listing_id':456456456,'price': '$10', 'listing_condition': 'Used - Good','username': 'user2'},
        {'listing_id':789789789,'price': '$15', 'listing_condition': 'Used - Like New','username': 'user3'}]
        #User's unordered baskets
        baskets=[{'order_basket_id':149872},{'order_basket_id': 476343},{'order_basket_id':345645}]
        return render_template('book-listings.html', book=book_details, listings=listings, baskets=baskets)
    elif request.method == 'POST':
        listing_id = request.form['listing_id']
        order_basket_id = request.form['order_basket_id']
        #add listing_id to order_basket with id=order_basket_id
        return redirect(url_for('account'))

@app.route('/make-listing', methods=('GET', 'POST'))
def make_listing():
    if request.method == 'GET':
        return render_template('make-listing.html')
    elif request.method == 'POST':
        isbn = request.form['isbn']
        price = request.form['price']
        listing_condition = request.form['listing_condition']
        #add this listing to DB (get user from g.user['id'])
        if False: #this should check if a book with ISBN 'isbn' already exists
            return redirect(url_for('book_listings', isbn=isbn))
        else:
            return redirect(url_for('add_book', isbn=isbn))

@app.route('/add-book/<int:isbn>', methods=('GET', 'POST'))
def add_book(isbn):
    if request.method == 'GET':
        return render_template('add-book.html', isbn=isbn)
    elif request.method == 'POST':
        subject = request.form['subject']
        title = request.form['title']
        authors = request.form['authors'] #names seperated by commas. Might need to make new author if author with that name doesn't already exist
        publisher = request.form['publisher'] #might have to make new publisher if publisher with this name doesn't exist
        description = request.form['description']
        #add this new book to DB
        return redirect(url_for('book_listings', isbn=isbn))

@app.route('/new-order', methods=('GET', 'POST'))
def new_order():
    if request.method == 'GET':
        return render_template('new-order.html')
    elif request.method == 'POST':
        address = request.form['address']
        #add new order basket for user at given address
        return redirect(url_for('account'))

@app.route('/account')
def account():
    user_details = {'username':'placeholder_username'}
    listings=[{'listing_id':123123123,'price': '$20', 'listing_condition': 'New', 'title': 'Placeholder Title 1', 'listing_status':'Listed'},
        {'listing_id':456456456,'price': '$10', 'listing_condition': 'Used - Good','title': 'Placeholder Title 2','listing_status':'Ordered'},
        {'listing_id':789789789,'price': '$15', 'listing_condition': 'Used - Like New','title': 'Placeholder Title 3','listing_status':'Delivered'}]
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




