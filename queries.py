#1.A get book isbn from input book title
GET_ISBN_TITLE = ("SELECT book.ISBN FROM book WHERE book.title = %s")

#1.B get all ordered books from isbn from input book isbn
GET_BOOK_ISBN = ("SELECT * FROM book WHERE book.ISBN = %s ORDER BY isbn")

#1.C return all books from book
GET_EVERY_BOOK = ("SELECT* FROM book;")

#1.D Selecting all books and displaying its title when given an isbn
GET_TITLE_ISBN = ("SELECT book.title FROM book WHERE book.ISBN = %s")

#2.A inserting username and userpassword into user
INSERT_USER = ("INSERT INTO user (username, userpassword)"
"VALUES( %s, %s)")

#2.B Selecting username, userpassword, userid when given a username
RETURN_USER = ("SELECT username, userpassword, user_id FROM user WHERE username=%s")

#2.C Returning a user given a user_id
GET_USER_FROM_ID = ("SELECT username, userpassword, user_id FROM user WHERE user_id=%s")

#3 Insert Book
INSERT_BOOK = ("INSERT INTO book(isbn, subject, title, publisher, author, description)"
                "VALUES(%s, %s, %s, %s, %s, %s)")

#4 Getting the number of books with a given isbn
GET_NUMISBN = ("SELECT COUNT(DISTINCT isbn) FROM book WHERE book.isbn = %s")

#5 changes listing_status to sold. takes order basket, listing id
BUY_BOOK = ("UPDATE listing "
"SET listing_status = 'sold', order_basket_id = %s "
"WHERE listing_id = %s")

#6 inserts a publisher and takes pub_id, pub_name
INSERT_PUBLISHER = ("INSERT INTO publisher "
"VALUES(%s, %s)")


#7 Insert an author while given author_id, author_name
INSERT_AUTHOR = ("INSERT INTO author "
"VALUES(%s, %s)")

#8 Insert a new listing, listing status is all caps
INSERT_LISTING =  ("INSERT INTO listing(price, listing_status, listing_condition, user_id, book_isbn)"
"VALUES(%s, %s, %s, %s, %s)")

#9 Insert Order Basket
INSERT_ORDER_BASKET = ("INSERT INTO order_basket(user_id, address, order_basket_status)"
                       "VALUES(%s, %s, %s)")

#10 matches user id to basket id(user_id)
MATCH_USER_ORDER_BASKET = ("SELECT order_basket_id FROM order_basket, user WHERE order_basket.user_id = %s")

#10.B gets all a users unordered baskets
MATCH_USER_ORDER_BASKET_UNORDERED = ("SELECT DISTINCT order_basket_id FROM order_basket, user WHERE order_basket.user_id = %s AND order_basket.order_basket_status=\"OPEN\"")

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

#20 get number of listings for user
GET_NUMPUBLISHERS = ("SELECT COUNT(DISTINCT pub_id) FROM publisher WHERE %s = pub_id")

#21 Get a listing based on a books isbn
GET_LISTING_BOOK_ISBN = ("SELECT listing.listing_id, listing.price, listing.listing_condition, listing.user_id FROM book, listing WHERE book.isbn = %s AND book.isbn = listing.book_isbn AND listing.listing_status = 'selling'")

#22 Get a book from the book title
GET_BOOK_TITLE = ("SELECT book.title, book.subject, book.description, book.isbn, book.author FROM book WHERE book.title = %s")

#23 Get a book from the book isbn
GET_BOOK_ISBN = ("SELECT book.title, book.subject, book.description, book.isbn, book.author FROM book WHERE book.isbn = %s")

#24 Update a listing.order_basket_id given a listing_id
UPDATE_LISTING = ("UPDATE listing SET order_basket_id = %s WHERE listing_id = %s")

#25 Obtaining every book
GET_EVERY_BOOK = ("SELECT * FROM book")

#26 Obtaining the listing from the user_id
MATCH_LISTING_USERID = ("SELECT listing.listing_id, listing.price, listing.listing_condition, book.title, listing_status FROM listing, book WHERE listing.book_isbn=book.isbn AND listing.user_id = %s")

#27 Obtaining an order_basket from the user_id
GET_ORDER_BASKET_USER_ID = ("SELECT DISTINCT order_basket.order_basket_id, order_basket.address, order_basket.order_basket_status FROM order_basket, user WHERE order_basket.user_id = user.user_id AND user.user_id = %s")

#28 Obtaining a listing from an order_basket_id
GET_LISTING_ORDER_BASKET_ID = ("SELECT listing.listing_id, listing.price, listing.listing_condition, listing.user_id, listing.book_isbn FROM order_basket, listing WHERE order_basket.order_basket_id = listing.order_basket_id AND order_basket.order_basket_id = %s")

#29 Updating a listing to sold when given a listing_id
BUY_LISTING = ("UPDATE listing SET listing_status = 'SOLD', listing.order_basket_id = NULL WHERE listing_id = %s")

#30 Updating an order_basket to closed when given an order_basket_id
BUY_ORDER_BASKET = ("UPDATE order_basket SET order_basket_status = 'CLOSED' WHERE order_basket_id = %s")

#31 Delete an order_basket when given a order_basket_id
DELETE_ORDER_BASKET = ("DELETE FROM order_basket WHERE order_basket_id = %s")
