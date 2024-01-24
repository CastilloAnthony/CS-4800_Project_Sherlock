# CHRISTIAN
from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify

import uuid
import time
#pip install bcrypt
import bcrypt
from multiprocessing import Queue

#CLASS IMPORTATION
from controllers.login import Login

from controllers.homepage import Homepage

from controllers.addPreset import AddPreset
from controllers.deletePreset import DeletePreset 
from controllers.editPreset import EditPreset 
from controllers.viewPreset import ViewPreset 

from controllers.addWebsite import AddWebsite 
from controllers.deleteWebsite import DeleteWebsite 
from controllers.viewWebsite import ViewWebsite 

import webbrowser

# import controllers.graphTableGenerator

class MyFlaskApp:
    def __init__(self, requestQ:Queue, dataQ:Queue):
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        # self.admin_view = Blueprint('admin_routes',__name__, template_folder='../templates', static_folder='../static')
        
        self.app.secret_key = 'your_secret_key_here'
        
        self.app.requestQ = requestQ
        self.app.dataQ = dataQ
        
        self.curr_email = ''
        #ROUTECREATING
        #Example: self.app.add_url_rule(route='<route>', name='<name>', function=<function>, OPTIONAL methods=[<typeOfRequest>])
        
        ########
        self.app.add_url_rule('/logged_in', 'logged_in', self.logged_in)
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST', 'GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout, methods=['POST', 'GET'])
        self.app.add_url_rule('/', 'index', self.index, methods=['POST', 'GET'])
        
        ########
        
        #HOMEPAGE
        self.app.add_url_rule('/home', 'home', self.home)
        #ABOUTPAGE
        self.app.add_url_rule('/about', 'about', self.about)
        
        #FORPRESETS
        #ADDPRESET
        self.app.add_url_rule('/addPreset', 'addPreset', self.addPreset)
        self.app.add_url_rule('/addPreset/newAddedPreset', 'newAddedPreset', self.newAddedPreset, methods=['POST'])
        self.app.add_url_rule('/addPresetWebList', 'addPresetWebList', self.addPresetWebList)
        #DELETEPRESET
        self.app.add_url_rule('/deletePreset', 'deletePreset', self.deletePreset)
        self.app.add_url_rule('/deletePreset/newDeletedPreset', 'newDeletedPreset', self.newDeletedPreset, methods=['POST'])
        #VIEWPRESET
        self.app.add_url_rule('/viewPreset', 'viewPreset', self.viewPreset)
        self.app.add_url_rule('/viewPreset/newViewPreset', '/viewPreset/newViewPreset', self.newViewPreset, methods=['POST'])
        #EDITPRESET
        self.app.add_url_rule('/editPreset', 'editPreset', self.editPreset)
        self.app.add_url_rule('/editPreset/newEditedPreset', 'newEditedPreset', self.newEditedPreset, methods=['POST'])
        self.app.add_url_rule('/editPreset/newEditedPreset/edit', 'edit', self.edit, methods=['POST'])
        
        #FORWEBSITES
        #ADDWEBSITE
        self.app.add_url_rule('/addWebsite', 'addWebsite', self.addWebsite)
        self.app.add_url_rule('/addWebsite/newAddedWebsite', 'newAddedWebsite', self.newAddedWebsite, methods=['POST'])
        #DELETEWEBSITE
        self.app.add_url_rule('/deleteWebsite', 'deleteWebsite', self.deleteWebsite)
        self.app.add_url_rule('/deleteWebsite/newDeletedWebsite', 'newDeletedWebsite', self.newDeletedWebsite, methods=['POST'])
        #VIEWEBSITE
        self.app.add_url_rule('/viewWebsite', 'viewWebsite', self.viewWebsite)
        self.app.add_url_rule('/viewWebsite/newViewWebsite', '/viewWebsite/newViewWebsite', self.newViewWebsite, methods=['POST'])
        self.app.add_url_rule('/viewWebsite/viewWebsiteWebList', '/viewWebsite/viewWebsiteWebList', self.viewWebsiteWebList)
        self.app.add_url_rule('/viewWebsite/viewWebsiteWebList/newViewWebsite', '/viewWebsite/viewWebsiteWebList/newViewWebsite', self.newViewWebsite, methods=['POST'])
        
        #CLASS_INITIALIZATION
        self.loginClass = Login(self.app.requestQ, self.app.dataQ)
        
        self.homeClass = Homepage(self.app.requestQ, self.app.dataQ)
        
        self.addPresetClass = AddPreset(self.app.requestQ, self.app.dataQ)
        self.deletePresetClass = DeletePreset(self.app.requestQ, self.app.dataQ)
        self.editPresetClass = EditPreset(self.app.requestQ, self.app.dataQ)    
        self.viewPresetClass = ViewPreset(self.app.requestQ, self.app.dataQ)
        
        
        self.addWebsiteClass = AddWebsite(self.app.requestQ, self.app.dataQ)
        self.deleteWebsiteClass = DeleteWebsite(self.app.requestQ, self.app.dataQ)   
        self.viewWebsiteClass = ViewWebsite(self.app.requestQ, self.app.dataQ)

        webbrowser.open("http://127.0.0.1:7777")
             
            
        
    ################################
    #        AUTH ROUTING          #
    ################################
    #FINISHED
    def index(self):
        """_summary_: first page that user will see, if signed in already skip to login, if they haven't fill information and get in database

        Returns:
            html: send them to logged_in.html to back to here so that they can redo their passwords or because they already signed in with those credentials 
        """
        #FOR FIRST TIME LOGGING IN
        message = ''
        # if "email" in session:
        #     self.curr_email = session["email"]
        #     return redirect(url_for("home"))
        if request.method == "POST":
            user = request.form.get("fullname")
            email = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            
            #result needs to be a 
            result = self.register_user(user, email, password1, password2)
            if result == email:
                self.curr_email = email
                return render_template('auth/logged_in.html', email=result)
            else:
                message = result
                return render_template('auth/index.html', message=message)
        return render_template('auth/index.html')
    #FINISHED
    def login(self):
        """_summary_: we check for email and password, first email if email is found then check for email and 
                        password password is done using bcrypt and seeing if password is similar enough

        Returns:
            url or html: depending we send them to homepage or back to the login because they messed up
        """
        message = 'Please login to your account'
        # if "email" in session:
        #     return redirect(url_for("logged_in"))

        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            #Start an insert query
            #don't have user_database will need to to a query and find_user_by_email
            email_found = self.loginClass.find_user_by_email(email) 
            if email_found:
                email_val = email_found['email']
                passwordcheck = email_found['password']

                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    session["email"] = email_val
                    self.curr_email = email_val
                    return redirect(url_for('home'))#MAY CHANGE
                else:
                    if "email" in session:
                        return redirect(url_for("home"))#MAY CHANGE
                    message = 'Wrong password'
                    return render_template('auth/login.html', message=message)
            else:
                message = 'Email not found'
                return render_template('auth/login.html', message=message)
        return render_template('auth/login.html', message=message)
    #FINISHED
    def logged_in(self):
        """_summary_: if logged in we just want to send them into their application so go to the homepage.html different then index

        Returns:
            html or url: depending, we will usually send to homepage tho
        """
        if "email" in session:
            email = session["email"]
            self.curr_email = email
            self.addPresetClass.getEmail(self.curr_email)
            #TODO: pass username as context w/ or instead of email.
            return render_template('homepage.html', email=email) #changed from auth/logged_in.html
        else:
            return redirect(url_for("login"))
    #FINISHED
    def register_user(self, user, email, password1, password2):
        """_summary_: for checking whether this user with all this information is in our system as well as inserting them into our system if not

        Args:
            user (str): users chosen username usually first name
            email (str): any strinng we are not checking for valid emails yet
            password1 (str): string of letters numbers and symbols users puts in
            password2 (str): hopefully same letters numbers and symbols might not be we need to check

        Returns:
            str: email that is actually taken from the database so that we know that an insertion occured and that we are now on that document in auth
        """
        # don't have user_database will need to to a query and find_user_by_email as well as name
        user_found = self.loginClass.find_user_by_name(user) 
        email_found = self.loginClass.find_user_by_email(email) 
        
        
        # user_found= {'id': UUID('103d3cac-3fe3-4e19-bfa2-c551456d9d4a'), 'timestamp': 1700092919.792062, 'data': 'Not Yet Implemented'}
        # user_found = (user_found['data'] != 'Not Yet Implemented') #should be False if it is not
        # email_found = (email_found['data'] != 'Not Yet Implemented') #should be False if it is not
        # print('user_found',user_found)
        # print('email_found',email_found)
        
        if user_found:
            return 'There already is a user by that name'
        if email_found:
            return 'This email already exists in the database'
        if password1 != password2:
            return 'Passwords should match'

        hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        
        user_input = {'name': user, 'email': email, 'id':str(uuid.uuid4()), 'password': hashed, 'creationTime':time.time()}
        self.loginClass.insert_user(user_input)
        user_data = self.loginClass.find_user_by_email(email)
        print('user_data|', user_data)
        new_email = user_data['email']
        return new_email
    
    #NOT REALLY USING THIS: #FINISHED
    def logout(self):
        """_summary_: users will have ability to unsign from their account, this really only happens after a user registers

        Returns:
            html or back to home/registration: either shows the signout page or the homepage 
        """
        if "email" in session:
            session.pop("email", None)
            return render_template("auth/signout.html")
        else:
            return redirect(url_for('index')) #right now index is home.html but it will be index when done
    
    
    
    
    
    ################################
    #        NORMAL ROUTING        #
    ################################
    
    #TODO: get numpy in in the query1() so it isn't as slow
    def home(self):
        """_summary_: first thing after being logged in, gives buttons for users to press, this function just renders templates and sends in the email

        Returns:
            html: homepage.html
        """
        # works just fine
        #print(self.viewWebsiteClass.query1())
        self.homeClass.getEmail(self.curr_email)
        
        return render_template('homepage.html', userName=self.homeClass.query()) #data=self.viewWebsiteClass.query1())
    
    def about(self):
        """_summary_: just shows an about page that shows what we meant to do with this, as well as describe the makers, and what we believe and hope

        Returns:
            html: aboutpage.html
        """
        return render_template('aboutpage.html') 
    
    #FINISHED
    def addPreset(self):
        """_summary_: grab the email and send it in so that that class can know who is signed in also render html as well as send in every url we have

        tag: masterList

        Returns:
            html: AddPreset.html
        """
        self.addPresetClass.getEmail(self.curr_email)
        return render_template('AddPreset.html', masterList=self.addPresetClass.query())

    def newAddedPreset(self):
        """_summary_: simply takes what user gave us in addPreset and updates users info 

        Returns:
            url: go back home
        """
        self.addPresetClass.addPreset()
        # Redirect to the /home route and render the home.html template
        return redirect(url_for('home'))

    def addPresetWebList(self):
        """summary: grabs user's email to query database for user's local webList

        tag: webList

        Returns:
            html: addPresetWebList.html
        """
        self.addPresetClass.getEmail(self.curr_email)
        return render_template('addPresetWebList.html', masterList = self.addPresetClass.query2())
   
    #TODO: grab graphs to put into this
    def viewPreset(self):
        """_summary_: send in list of presets and let user choose

        Returns:
            html: viewPreset.html
        """
        self.viewPresetClass.getEmail(self.curr_email)
        return render_template('viewPreset.html', presets = self.viewPresetClass.query())
    
    def newViewPreset(self):
        # grab selected website
        # in viewWebsite class use that and use the 
        # website as a parameter to generateGraph('https://csustan.edu', 300, 15)
        # that gives me a picture
        # print(self.viewWebsiteClass.viewWebsite())
        return render_template('viewPresetNew.html', plot_html = self.viewPresetClass.viewPreset())
        
    #TODO: grab graphs to put into this
    def viewWebsite(self):
        """_summary_: grab all urls in MASTERLIST and let user choose which one
        
        tag: masterList

        Returns:
            html: viewWebsite.html and list of urls in dictionary format
        """
        #buttons to pick the website
        return render_template('viewWebsite.html', masterList = self.viewWebsiteClass.query2())
    
    def newViewWebsite(self):
        # grab selected website
        # in viewWebsite class use that and use the 
        # website as a parameter to generateGraph('https://csustan.edu', 300, 15)
        # that gives me a picture
        # print(self.viewWebsiteClass.viewWebsite())
        return render_template('viewWebsiteNew.html', plot_html=self.viewWebsiteClass.viewWebsite())
    
    def viewWebsiteWebList(self):
        """summary: grab all urls in weblist and let user choose which one

        tag: webList
        
        Returns:
            html: viewWebsite.html and list of urls in dictionary format
        """
        self.viewWebsiteClass.getEmail(self.curr_email)
        return render_template('viewWebsiteWebList.html', masterList = self.viewWebsiteClass.query3())
    
    #FINISHED
    def deletePreset(self):
        """_summary_: give email then send in list of presets as well as html

        Returns:
            html: html and dict
        """
        self.deletePresetClass.getEmail(self.curr_email)
        return render_template('DeletePreset.html', presets=self.deletePresetClass.query())

    def newDeletedPreset(self):
        """_summary_: from user selection we make a deletion or update in documents

        Returns:
            url: go back home
        """
        self.deletePresetClass.deletePreset()
        # Redirect to the /home route and render the home.html template
        return redirect(url_for('home'))

    #FINISHED
    def deleteWebsite(self):
        """_summary_: grab email list of websites from users document

        tag: webList

        Returns:
            html: send in html, list
        """
        self.deleteWebsiteClass.getEmail(self.curr_email)
        return render_template('DeleteWebsite.html', masterList = self.deleteWebsiteClass.query())
    
    def newDeletedWebsite(self):
        """_summary_: just delete what was given

        Returns:
            url: go back home
        """
        self.deleteWebsiteClass.deleteWebsite()
        # Redirect to the /home route and render the home.html template
        return redirect(url_for('home'))

    #FINISHED
    def editPreset(self):
        """_summary_: show html and give presets to be chosen and changed

        Returns:
            html: html and list
        """
        self.editPresetClass.getEmail(self.curr_email)
        return render_template('EditPreset.html', presets=self.editPresetClass.query())
    
    def newEditedPreset(self):
        """_summary_: user selected a preset to change, give them the one they changed so they know how to correctly reformat their new one
        
        tag: webList

        Returns:
            html:old preset as well as a new list of websites to choose to make a preset, as well as timestamp 
        """
        oldPreset=self.editPresetClass.editPreset()
        #turn timestamp that is in form: 1700691121.3678615
        #into a date
        timestamp = str(time.ctime(oldPreset['timestamp']))
        return render_template('EditPresetNew.html', oldPreset=oldPreset,masterList=self.editPresetClass.query2(), timestamp=timestamp)

    def edit(self):
        """_summary_: edit is now changed in documents and can go back home

        Returns:
            url: go back home
        """
        self.editPresetClass.editPreset1()
        return redirect(url_for('home'))

    #FINISHED
    def addWebsite(self):
        """_summary_: send email as well as render the template

        Returns:
            html: addWebsite
        """
        self.addWebsiteClass.getEmail(self.curr_email)
        return render_template('AddWebsite.html')
    
    def newAddedWebsite(self):
        """_summary_: just added whatever was in the textbox when they submitted

        Returns:
            url: go back home
        """
        self.addWebsiteClass.addWebsite()
        # Redirect to the /home route and render the home.html template
        return redirect(url_for('home'))

    ################################
    #      TECHNICAL FUNCTIONS     #
    ################################
    def run(self):
        self.app.run(host="0.0.0.0", port=7777)

    def newRequest(self, queryRequest):
        pass

def startFlask(requestQ, dataQ):
    newFlask = MyFlaskApp(requestQ, dataQ)
    newFlask.run()

# Usage
if __name__ == '__main__':
    request_queue = Queue()
    data_queue = Queue()
    my_flask_app = MyFlaskApp(request_queue, data_queue)
    my_flask_app.run()
