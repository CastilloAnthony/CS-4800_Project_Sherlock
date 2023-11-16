from flask import Flask, render_template, request, url_for, redirect, session, Blueprint
import pymongo
import bcrypt

auth_view = Blueprint('auth_routes',__name__, template_folder='../templates/auth', static_folder='../static', url_prefix='auth')
auth_view.secret_key = "testing"

## Registering blueprints
# app = Flask(__name__)
# from client.auth import auth_view

# app.register_blueprint(auth_view)

class MongoDBClient:
    def __init__(self, host="localhost", port=27017, database_name="total_records", collection_name="register"):
        self.client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def find_user_by_name(self, name):
        return self.collection.find_one({"name": name})

    def find_user_by_email(self, email):
        return self.collection.find_one({"email": email})

    def insert_user(self, user_data):
        self.collection.insert_one(user_data)

    def update_user_password(self, email, new_password):
        self.collection.update_one({"email": email}, {"$set": {"password": new_password}})

class UserRegistrationApp:
    def __init__(self):
        self.mongo = MongoDBClient()
        self.register_routes()

    def register_routes(self):
        app.add_url_rule('/', 'index', self.index, methods=['POST', 'GET'])
        app.add_url_rule('/logged_in', 'logged_in', self.logged_in)
        app.add_url_rule('/login', 'login', self.login, methods=['POST', 'GET'])
        app.add_url_rule('/logout', 'logout', self.logout, methods=['POST', 'GET'])

    def register_user(self, user, email, password1, password2):
        user_found = self.mongo.find_user_by_name(user)
        email_found = self.mongo.find_user_by_email(email)

        if user_found:
            return 'There already is a user by that name'
        if email_found:
            return 'This email already exists in the database'
        if password1 != password2:
            return 'Passwords should match'

        hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        user_input = {'name': user, 'email': email, 'password': hashed}
        self.mongo.insert_user(user_input)
        user_data = self.mongo.find_user_by_email(email)
        new_email = user_data['email']
        return new_email

    def index(self):
        message = ''
        if "email" in session:
            return redirect(url_for("logged_in"))
        if request.method == "POST":
            user = request.form.get("fullname")
            email = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            result = self.register_user(user, email, password1, password2)

            if result == email:
                return render_template('logged_in.html', email=result)
            else:
                message = result
                return render_template('index.html', message=message)
        return render_template('index.html')

    def logged_in(self):
        if "email" in session:
            email = session["email"]
            return render_template('logged_in.html', email=email)
        else:
            return redirect(url_for("login"))

    def login(self):
        message = 'Please login to your account'
        if "email" in session:
            return redirect(url_for("logged_in"))

        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            email_found = self.mongo.find_user_by_email(email)
            if email_found:
                email_val = email_found['email']
                passwordcheck = email_found['password']

                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    session["email"] = email_val
                    return redirect(url_for('logged_in'))
                else:
                    if "email" in session:
                        return redirect(url_for("logged_in"))
                    message = 'Wrong password'
                    return render_template('login.html', message=message)
            else:
                message = 'Email not found'
                return render_template('login.html', message=message)
        return render_template('login.html', message=message)

    def logout(self):
        if "email" in session:
            session.pop("email", None)
            return render_template("signout.html")
        else:
            return redirect(url_for('index'))
