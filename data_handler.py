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
                    SELECT spiders.spider_name,spiders.world,spiders.price,spiders.information FROM spiders
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
def get_hash_from_database(cursor,username):
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
def registration(cursor,username,password):
    hashed_bytes = get_hash_from_password(password)
    cursor.execute("""
                    INSERT INTO users (user_name,hashed_password)
                    VALUES (%(username)s,%(hashed_bytes)s);
                   """,
                   {"username": username,
                    "hashed_bytes": hashed_bytes})


@database_common.connection_handler
def get_username_by_user_id(cursor,userid):
    cursor.execute("""
                SELECT user_name FROM users
                WHERE id = %(userid)s
    """,
                   {"userid": userid})


@database_common.connection_handler
def get_spider_by_id(cursor, spider_id):
    cursor.execute("""SELECT * FROM spiders WHERE  id = %(spider_id)s;""", {'spider_id': spider_id})
    spider = cursor.fetchall()
    return spider


@database_common.connection_handler
def get_user_id_by_username(cursor, username):
    cursor.execute("""SELECT * FROM users WHERE user_name = %(username)s;""", {'username': username})
    user = cursor.fetchall()
    return user


@database_common.connection_handler
def insert_order(cursor, user_id, spider_id):
    cursor.execute("""INSERT INTO orders (spider_id, user_id) VALUES (%(spider_id)s, %(user_id)s);""", {'spider_id': spider_id, 'user_id':user_id})


@database_common.connection_handler
def get_spider_by_name(cursor, spider_name):
    cursor.execute("""SELECT id FROM spiders WHERE spider_name = %(spider_name)s; """, {'spider_name': spider_name})
    spider = cursor.fetchall()
    return spider


@database_common.connection_handler
def get_all_spider_names(cursor):
    cursor.execute("""SELECT spider_name FROM spiders;""")
    all_spider_names = cursor.fetchall()
    return all_spider_names


@database_common.connection_handler
def insert_spider_img(cursor, spider_name, filename):
    cursor.execute("""INSERT INTO spider_imgs (name, images) VALUES (%(spider_name)s, %(filename)s); """, {'spider_name':spider_name, 'filename':filename})


@database_common.connection_handler
def get_user_id(cursor, username):
    cursor.execute("""SELECT id FROM users WHERE user_name = %(username)s;""", {'username':username})
    user_id = cursor.fetchall()
    return user_id


@database_common.connection_handler
def delete_spider_by_id(cursor, spider_id):
    cursor.execute("""DELETE FROM spiders WHERE id = %(s_id)s;""", {'s_id': spider_id})


@database_common.connection_handler
def edit_spider(cursor, spider_id, name, world, price, info):
    cursor.execute("""UPDATE spiders SET spider_name = %(name)s, world =%(world)s, price = %(price)s, info = %(info)s WHERE id = %(s_id)s;""",
                   {'name': name, 'price': price, 'world': world, 'info':info, 's_id': spider_id})