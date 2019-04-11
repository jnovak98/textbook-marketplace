#INSERT_CREW = ("INSERT INTO crew(location, cuisine_type0, cuisine_type1, cuisine_type2, selected_restaurant)"
#                "VALUES(null, null, null, null, null)")
GET_ISBN_TITLE = ("SELECT book.ISBN "
"FROM book "
"WHERE book.title = %s")

GET_TITLE_ISBN = ("SELECT book.title"
"FROM book "
"WHERE book.ISBN = %s")

sell_book
GET_TITLE_ISBN = ("COUNT(DISTINCT ISBN)"
"FROM book "
"WHERE book.ISBN = %s")



INSERT_AUTHOR = ("INSERT INTO author "
"VALUES(%s, %s)")


MATCH_USER_ORDER_BASKET = ("SELECT order_basket_id"
"FROM order_basket, user"
"WHERE order_basket.user_id = uuser.user_id")



GET_AUTHORNAME_ISBN = (
"SELECT author.author_name"
"FROM authors, author"
"WHERE author.author_id = authors.author_id ^ authors.isbn = %s")


GET_NUMLISTINGS = ("SELECT COUNT(DISTINCT listing_id)"
"FROM user, listing"
"WHERE user.user_id = listing.user_id")


INSERT_AUTHORS = ("INSERT INTO authors"
"VALUES(%s, %s)")

