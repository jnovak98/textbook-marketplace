#INSERT_CREW = ("INSERT INTO crew(location, cuisine_type0, cuisine_type1, cuisine_type2, selected_restaurant)"
#                "VALUES(null, null, null, null, null)")
INSERT_CREW = ("INSERT INTO crew(selected_restaurant, vote_started) "
                "VALUES(null, false)")
UPDATE_CREW_LOCATION_CUISINETYPE = ("UPDATE crew "
                                    "SET location=%s, cuisine_type0=%s, cuisine_type1=%s, cuisine_type2=%s "
                                    "WHERE crew_id=%s")
GET_CREW = ("SELECT crew_id "
            "FROM crew "
            "WHERE crew_id=%s")

UPDATE_CREW_VOTING = ("UPDATE crew "
                        "SET vote_started=%s "
                        "WHERE crew_id=%s ")

GET_CREW_VOTING = ("SELECT vote_started "
                    "FROM crew "
                    "WHERE crew_id=%s")

GET_CREW_SELECTED_REST = ("SELECT selected_restaurant "
                            "FROM crew "
                            "WHERE crew_id=%s")

SELECTED_RESTAURANT = ("SELECT restaurant_id "
                        "FROM vote "
                        "WHERE crew_id = %s "
                        "GROUP BY restaurant_id "
                        "HAVING MAX(vote_num)")
UPDATE_CREW_SELECTED_RESTAURANT = ("UPDATE crew "
                                    "SET selected_restaurant=%s "
                                    "WHERE crew_id=%s")
DELETE_CREW = ("DELETE FROM crew "
                "WHERE crew_id=%s")

RESTAURANT_EXISTS = ("SELECT restaurant_id "
                    "FROM restaurant "
                    "WHERE address=%s")
INSERT_RESTAURANT = ("INSERT INTO restaurant(name, cuisine, address, rating, price_range, menu_url, image_url) "
                    "VALUES(%s, %s, %s, %s, %s, %s, %s)")
GET_RESTAURANT_IDS = ("SELECT restaurant_id "
                        "FROM vote "
                        "WHERE crew_id=%s")
GET_RESTID_INFO = ("SELECT restaurant_id, name, cuisine, address, rating, price_range, menu_url, image_url "
                    "FROM restaurant "
                    "WHERE restaurant_id=%s")
INSERT_VOTE = ("INSERT INTO vote(crew_id, restaurant_id, vote_num) "
                    "VALUES(%s, %s, 0)")

GET_VOTE_NUM = ("SELECT vote_num FROM vote "
                    "WHERE crew_id=%s AND restaurant_id=%s")

UPDATE_VOTE_COUNT = ("UPDATE vote "
                    "SET vote_num =%s "
                    "WHERE crew_id=%s AND restaurant_id=%s")
GET_CREW_VOTES = ("SELECT vote_id "
                    "FROM vote "
                    "WHERE crew_id=%s")

DELETE_CREW_VOTES = ("DELETE FROM vote "
                    "WHERE vote_id=%s")
