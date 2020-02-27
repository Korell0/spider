from flask import Flask, render_template, session, request, redirect, make_response
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
            error = "This username is already in use"
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
    return render_template('main_page.html', all_spiders=all_spiders, username=username)


@app.route('/new-spider')
def get_new_spider():
    return render_template("new_spider.html",error=None)


@app.route('/new-spider-detail', methods=["GET", "POST"])
def add_new_spider():
    spider_name = request.form["spider-name"]
    all_names_raw = data_handler.get_all_spider_names()
    list_of_spiders = []
    for items in all_names_raw:
        for key , value in items.items():
            list_of_spiders.append(value)
    if spider_name in list_of_spiders:
        error = "There are a spider like that already"
        return render_template('new_spider.html', error=error)
    else:
        world = request.form["world"]
        price = request.form["price"]
        info = request.form["info"]
        data_handler.insert_new_spiders(spider_name, world, int(price), info)
        if request.files['file']:
            file = request.files['file']
            file.save(path + "/static/images/" + file.filename)
            spider_id = data_handler.get_spider_by_name(request.form["spider-name"])
            for key, value in spider_id.items():
                data_handler.insert_spider_img(value, file.filename)
        return redirect("/")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
