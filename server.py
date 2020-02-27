from flask import Flask, render_template,session,request,redirect,make_response
import data_handler
import os

app = Flask(__name__)
path = os.path.dirname(__file__)
app.secret_key = '12345'


@app.route('/set-cookie')
def cookie_insertion():
    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('cookie-name', value='values')
    return response


def is_valid_registration():
    return " " not in request.form["username"] and\
           " " not in request.form["password"] and\
           request.form["username"] is not "" and\
           request.form["password"] is not ""


@app.route('/registration', methods=["POST"])
def registration():
    if is_valid_registration():
        if request.form["username"] in data_handler.get_usernames_from_database():
            error = "This username is already taken"
            return render_template("error.html", error=error)
        data_handler.registration(request.form["username"], request.form["password"])
        session["username"] = request.form["username"]
    return redirect("/")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if data_handler.get_hash_from_database(request.form["username"]) is not None:
            database_password = data_handler.get_hash_from_database(request.form["username"])
            verify_password = data_handler.verify_password(request.form["password"],
                                                           database_password["hashed_password"])
            if verify_password:
                session["username"] = request.form["username"]
                return redirect("/")
        error = "Invalid username or password"
        return render_template("error.html", error=error)
    error = "Invalid username or password"
    return render_template("error.html", error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/')
def main_page():
    all_spiders = data_handler.get_spider_data()
    username = session.get("username")
    user_id = data_handler.get_user_id(username)
    return render_template('main_page.html', all_spiders=all_spiders, username=username, user_id=user_id)


@app.route('/new-spider')
def get_new_spider():
    return render_template("new_spider.html")


@app.route('/new-spider-detail', methods=["GET","POST"])
def add_new_spider():
    spider_name = request.args["spider-name"]
    world = request.args["world"]
    price = request.args["price"]
    info = request.args["info"]
    data_handler.insert_new_spiders(spider_name, world, int(price), info)
    return redirect("/")


@app.route('/cart/<user_id>')
def get_cart_items():
    return render_template("cart.html")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
