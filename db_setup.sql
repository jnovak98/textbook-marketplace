CREATE database textbook_marketplace;
create user 'mysql_username'@'localhost' identified with mysql_native_password by 'mysql_password';
grant all on eaterank_project.* to 'mysql_username'@'localhost';
flush privileges;

use team_11;

CREATE TABLE user (
    user_id int,
    username varchar(11),
    userpassword varchar(11),
    
    primary key(user_id)
);

CREATE TABLE publisher(
	pub_id int,
	pub_name varchar(11),

primary key(pub_id)
);

CREATE TABLE book(
	isbn varchar(20),
	subject varchar(11),
	title varchar(32),
	description varchar(140),
	pub_id int,
	
	primary key(isbn),
foreign key (pub_id) references publisher(pub_id)
);



CREATE TABLE order_basket (
order_basket_id int,
user_id int,
address varchar(32),
date_made varchar(11),
order_basket_status varchar(11), 

Primary key(order_basket_id, user_id),
Foreign key(user_id) references user(user_id)
);

CREATE TABLE listing (
	listing_id int,
	price varchar(11),
	listing_status varchar(11),
	listing_condition varchar(32),
	user_id int,
	order_basket_id int,
	book_isbn varchar(20),

	Primary key(listing_id, user_id),
	Foreign key(order_basket_id) references order_basket(order_basket_id),
	Foreign Key(book_isbn) references book(isbn),
	Foreign key(user_id) references user(user_id)
);

CREATE TABLE author (
	author_id int,
	author_name varchar(20),

	primary key(author_id)
);

CREATE TABLE authors (
	author_id int,
	isbn varchar(20),

	primary key(author_id, isbn),
foreign key(author_id) references author(author_id),
foreign key(isbn) references book(isbn)
);
