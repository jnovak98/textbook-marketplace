#INSERT_CREW = ("INSERT INTO crew(location, cuisine_type0, cuisine_type1, cuisine_type2, selected_restaurant)"
#                "VALUES(null, null, null, null, null)")
GET_ISBN_TITLE = ("SELECT book.ISBN "
"FROM book "
"WHERE book.title = %s")

GET_TITLE_ISBN = ("SELECT book.title"
"FROM book "
"WHERE book.ISBN = %s")

INSERT_USER = ("INSERT INTO user "
"VALUES(%s, %s, %s")

GET_TITLE_ISBN = ("COUNT(DISTINCT ISBN)"
"FROM book "
"WHERE book.ISBN = %s")

BUY_BOOK = ("DELETE FROM BOOK "
"FROM book "
"WHERE book.ISBN = %s")

INSERT_AUTHOR = ("INSERT INTO author "
"VALUES(%s, %s)")

INSERT_LISTING =  ("INSERT INTO listing "
"VALUES(%s, %s, %s, %s, %s, %s, %s)")

MATCH_USER_ORDER_BASKET = ("SELECT order_basket_id"
"FROM order_basket, user"
"WHERE order_basket.user_id = uuser.user_id")

MATCH_ORDER_BASKET_LISTING = ("SELECT listing.listing_id"
"FROM listing, order_basket"
"WHERE order_basket.order_basket_id = listing.order_order_basket_id")



MATCH_AUTHORNAME_ISBN = (
"SELECT author.author_name"
"FROM authors, author"
"WHERE author.author_id = authors.author_id ^ authors.isbn = %s")

MATCH_PUBLISHER_BOOK = (
"SELECT book.ISBN"
"FROM book, publisher"
"WHERE book.publisher_pub_id = publisher.pub_id"
)


SORT_LOWEST_PRICE = (
"SELECT listing.listing_id"
"FROM LISTING"
"ORDER BY listing.price ASC"
)

GET_NUMLISTINGS = ("SELECT COUNT(DISTINCT listing_id)"
"FROM user, listing"
"WHERE user.user_id = listing.user_id")


INSERT_AUTHORS = ("INSERT INTO authors"
"VALUES(%s, %s)")

INSERT_PUBLISHER = ("INSERT INTO publisher "
"VALUES(%s, %s)")
