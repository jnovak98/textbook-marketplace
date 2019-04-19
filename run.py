import configparser
from flask import Flask, render_template, request
import mysql.connector

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

# Home page
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('home.html')



@app.route('/', methods=['GET', 'POST'])
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
#20
def insertPublisher(pub_id, pub_name):
    return sql_query(INSERT_PUBLISHER, pub_id, pub_name)

