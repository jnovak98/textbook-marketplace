

#1.A
GET_ISBN_TITLE = ("SELECT book.ISBN "
"FROM book "
"WHERE book.title = %s")

#1.B
GET_TITLE_ISBN = ("SELECT book.title FROM book WHERE book.ISBN = %s")

#2 (username, password)
INSERT_USER = ("INSERT INTO user (username, userpassword)"
"VALUES( %s, %s)")

#3 Insert Book
INSERT_BOOK = ("INSERT INTO book(isbn, subject, title, publisher, author, description)"
                "VALUES(%s, %s, %s, %s, %s, %s)")

#4 get title by isbn
GET_NUMISBN = ("SELECT COUNT(DISTINCT isbn) FROM book WHERE book.isbn = %s")

BUY_NUMISBN = ("SELECT COUNT(DISTINCT isbn) FROM book WHERE book.isbn = 63")

#5 changes listing_status to sold. takes order basket, listing id
BUY_BOOK = ("UPDATE listing "
"SET listing_status = 'sold', order_basket_id = %s "
"WHERE listing_id = %s")

#6 takes pub_id, pub_name
INSERT_PUBLISHER = ("INSERT INTO publisher "
"VALUES(%s, %s)")


#7 (author_id, author_name)
INSERT_AUTHOR = ("INSERT INTO author "
"VALUES(%s, %s)")

#8 (listing_id, user.user_id, order_basket_id, IBSN, price, listing_status, listing_condition)
INSERT_LISTING =  ("INSERT INTO listing(price, listing_status, listing_condition, user_id, book_isbn)"
"VALUES(%s, %s, %s, %s, %s)")

#9 Insert Order Basket
INSERT_ORDER_BASKET = ("INSERT INTO order_basket(user_id, address, order_basket_status)"
                       "VALUES(%s, %s, %s")

#10 matches user id to basket id(user_id)
MATCH_USER_ORDER_BASKET = ("SELECT order_basket_id FROM order_basket, user WHERE order_basket.user_id = %s")

#11 matches orderbasket_id to listing_id
MATCH_ORDER_BASKET_LISTING = ("SELECT listing.listing_id FROM listing, order_basket  WHERE order_basket.order_basket_id = %s")

#12 match order to user
MATCH_ORDER_USER = ("SELECT user_id FROM order_basket, user WHERE order_basket_id = %s AND order_basket.user_id = user.user_id")


#13 matches isbn to author name
MATCH_ISBN_AUTHORNAME = ("SELECT author.author_name FROM authors, author WHERE author.author_id = authors.author_id ^ authors.isbn = %s")

#14 matches publisherid to book
MATCH_PUBLISHER_BOOK = (
"SELECT book.ISBN FROM book, publisher WHERE book.pub_id = %s"
)

#15 matches book to listing_id
MATCH_BOOK_LISTING_ID = ("SELECT listing_id FROM listing, book WHERE book.isbn = %s AND listing.book_isbn= book.isbn")

#16 get number of listings for user
GET_NUMLISTINGS = ("SELECT COUNT(DISTINCT listing_id) FROM listing WHERE %s = listing.user_id")


#17 takes listing's isbn
SORT_LOWEST_PRICE = (
"SELECT listing.listing_id FROM listing, book WHERE book.isbn = %s ORDER BY listing.price ASC"
)

#18 sums the total cost of the order_basket
SUM_ORDER_BASKET= (
"SELECT SUM(price) FROM listing, order_basker WHERE listing_id = %s AND listing.order_basket_id = order_basket.order_basket_id")
                   
#19 takes author_id, isbn
INSERT_AUTHORS = ("INSERT INTO authors VALUES(%s, %s)")

#21 get number of listings for user
GET_NUMPUBLISHERS = ("SELECT COUNT(DISTINCT pub_id) FROM publisher WHERE %s = pub_id")

GET_LISTING_BOOK_ISBN = ("SELECT book.title, listing.price, listing.listing_condition FROM book, listing WHERE book.title = %s AND book.isbn = listing.book_isbn AND listing.listing_status = 'selling'")

GET_BOOK_TITLE = ("SELECT book.title, book.subject, book.description, book.isbn, book.author FROM book WHERE book.title = %s")

UPDATE_LISTING = ("UPDATE listing SET order_basket_id = %s, listing_status = %s WHERE listing_id = %s")

GET_EVERY_BOOK = ("SELECT * FROM book")




