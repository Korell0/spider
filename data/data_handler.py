import database_common
import bcrypt


@database_common.connection_handler
def insert_new_spiders(cursor, spider_name, world, price, info):
    cursor.execute("""
                        INSERT INTO spiders (spider_name, world, price, information) 
                        VALUES (%(spider_name)s,%(world)s,%(price)s,%(info)s)
        """, {"spider_name": spider_name, "world": world, "price": price, "info": info})


@database_common.connection_handler
def get_spider_data(cursor):
    cursor.execute("""
                    SELECT spiders.id,spiders.spider_name,spiders.world,spiders.price,spiders.information FROM spiders
    """)
    all_spiders = cursor.fetchall()
    return all_spiders


@database_common.connection_handler
def get_usernames_from_database(cursor):
    cursor.execute("""
                    SELECT user_name FROM users
                    """,)
    names = cursor.fetchall()
    return [item["user_name"] for item in names]


@database_common.connection_handler
def get_username_by_user_id(cursor, user_id):
    cursor.execute("""
                SELECT user_name FROM users
                WHERE id = %(user_id)s
    """,
                   {"user_id":user_id})
    username = cursor.fetchone()
    return username

@database_common.connection_handler
def get_user_id_by_username(cursor,username):
    cursor.execute("""
                    SELECT users.id FROM users
                    WHERE users.user_name = %(username)s
    """, {"username": username})
    user_id = cursor.fetchall()
    return user_id


@database_common.connection_handler
def insert_order(cursor,user_id,spider_id):
    cursor.execute("""
                    INSERT INTO orders (spider_id, user_id ) 
                    VALUES (%(spider_id)s,%(user_id)s)
    """, {"user_id": user_id, "spider_id": spider_id})


@database_common.connection_handler
def get_hash_from_database(cursor, username):
    cursor.execute("""
                SELECT users.hashed_password FROM users
                WHERE user_name = %(username)s
    """,
                   {"username": username})
    hash = cursor.fetchone()
    return hash


def get_hash_from_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    decoded_hash = hashed_password.decode('utf-8')
    return decoded_hash


def verify_password(password, hash):
    hashed_bytes_password = hash.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def registration(cursor, username, password):
    hashed_bytes = get_hash_from_password(password)
    cursor.execute("""
                    INSERT INTO users (user_name,hashed_password)
                    VALUES (%(username)s,%(hashed_bytes)s);
                   """,
                   {"username": username,
                    "hashed_bytes": hashed_bytes})


@database_common.connection_handler
def get_username_by_user_id(cursor, userid):
    cursor.execute("""
                SELECT user_name FROM users
                WHERE id = %(userid)s
    """,
                   {"userid": userid})
<<<<<<< HEAD:data/data_handler.py
<<<<<<< Updated upstream:data_handler.py
=======


@database_common.connection_handler
def get_spider_by_id(cursor, spider_id):
    cursor.execute("""
                    SELECT * FROM spiders
                    WHERE spiders.id = %(spider_id)s
    """, {"spider_id": spider_id})
=======
>>>>>>> master:data_handler.py


@database_common.connection_handler
def get_spider_by_name(cursor,name):
    cursor.execute("""
                  SELECT spiders.id FROM spiders
                  WHERE spiders.spider_name = %(name)s
                  LIMIT 1
    """, {"name": name})
    spiderid = cursor.fetchone()
    return spiderid

@database_common.connection_handler
def get_all_spider_names(cursor):
    cursor.execute("""
                    SELECT spiders.spider_name FROM spiders
    """)
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def insert_spider_img(cursor, spider_id, filename):
    cursor.execute("""
                INSERT INTO spider_imgs (spider_id, images)
                VALUES (%(spider_id)s, %(filename)s)   
    """, {"spider_id": spider_id, "filename": filename})

<<<<<<< HEAD:data/data_handler.py
@database_common.connection_handler
def get_cart_content(cursor):
    pass

@database_common.connection_handler
def get_user_id(cursor, user_name):
    cursor.execute("""SELECT id FROM users WHERE user_name = %(user_name)s;""", {'user_name': user_name})
    user_id = cursor.fetchall()

    return user_id
>>>>>>> Stashed changes:data/data_handler.py
=======

@database_common.connection_handler
def get_spider_by_id(cursor, spider_id):
    cursor.execute("""
                    SELECT spiders.id, spiders.spider_name, spiders.world, spiders.price, spiders.information,si.images AS images FROM spiders
                    LEFT JOIN spider_imgs si on spiders.id = si.spider_id
                    WHERE  spiders.id = %(spider_id)s
    """, {"spider_id": spider_id})
    details = cursor.fetchall()
    return details


@database_common.connection_handler
def edit_spider(cursor, spider_id, spider_name, world, price, info):
    cursor.execute("""
                    UPDATE spiders
                    SET spider_name = %(spider_name)s, world = %(world)s, price = %(price)s, information = %(info)s
                    WHERE spiders.id = %(spider_id)s
    """, {"spider_id": spider_id, "spider_name": spider_name, "world": world, "price": price, "info": info})


@database_common.connection_handler
def delete_spider_by_id(cursor,spider_id):
    cursor.execute("""
                    DELETE FROM spiders
                    WHERE id = %(spider_id)s
    """, {"spider_id": spider_id})
>>>>>>> master:data_handler.py
