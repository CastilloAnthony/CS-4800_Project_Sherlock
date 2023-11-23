# CHRISTIAN
from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify

import uuid
import time
#pip install bcrypt
import bcrypt
from multiprocessing import Queue

#CLASS IMPORTATION
from controllers.login import Login

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
        
        #FORPRESETS
        #ADDPRESET
        self.app.add_url_rule('/addPreset', 'addPreset', self.addPreset)
        self.app.add_url_rule('/addPreset/newAddedPreset', 'newAddedPreset', self.newAddedPreset, methods=['POST'])
        #DELETEPRESET
        self.app.add_url_rule('/deletePreset', 'deletePreset', self.deletePreset)
        self.app.add_url_rule('/deletePreset/newDeletedPreset', 'newDeletedPreset', self.newDeletedPreset, methods=['POST'])
        #VIEWPRESET
        self.app.add_url_rule('/viewPreset', 'viewPreset', self.viewPreset)
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
        
        
        #CLASS_INITIALIZATION
        
        self.loginClass = Login(self.app.requestQ, self.app.dataQ)
        
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
        #FOR FIRST TIME LOGGIN IN
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
        if "email" in session:
            email = session["email"]
            self.curr_email = email
            self.addPresetClass.getEmail(self.curr_email)
            return render_template('homepage.html', email=email)#changed from auth/logged_in.html
        else:
            return redirect(url_for("login"))
    #FINISHED
    def register_user(self, user, email, password1, password2):
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
        # please put data back in when a little quicker for debugging purposes
        # works just fine
        #print(self.viewWebsiteClass.query1())
        return render_template('homepage.html', email=self.curr_email) #data=self.viewWebsiteClass.query1())
    
    #FINISHED
    def addPreset(self):
        self.addPresetClass.getEmail(self.curr_email)
        return render_template('AddPreset.html', masterList=self.addPresetClass.query())

    def newAddedPreset(self):
        self.addPresetClass.addPreset()
        # Redirect to the /home route and render the home.html template
        return redirect(url_for('home'))

    #TODO: grab graphs to put into this
    def viewPreset(self):
        return render_template('viewPreset.html')
    
    #TODO: grab graphs to put into this
    def viewWebsite(self):
        #buttons to pick the website
        return render_template('viewWebsite.html', masterList = self.viewWebsiteClass.query2())
    def newViewWebsite(self):
        # grab selected website
        # in viewWebsite class use that and use the 
        # website as a parameter to generateGraph('https://csustan.edu', 300, 15)
        # that gives me a picture
        # print(self.viewWebsiteClass.viewWebsite())
        return render_template('viewWebsiteNew.html', plot_html = self.viewWebsiteClass.viewWebsite()[0], url=self.viewWebsiteClass.viewWebsite()[1])
        
    #FINISHED
    def deletePreset(self):
        self.deletePresetClass.getEmail(self.curr_email)
        return render_template('DeletePreset.html', presets=self.deletePresetClass.query())

    def newDeletedPreset(self):
        self.deletePresetClass.deletePreset()
        # Redirect to the /home route and render the home.html template
        return redirect(url_for('home'))

    #FINISHED
    def deleteWebsite(self):
        self.deleteWebsiteClass.getEmail(self.curr_email)
        return render_template('DeleteWebsite.html', masterList = self.deleteWebsiteClass.query())
    
    def newDeletedWebsite(self):
        self.deleteWebsiteClass.deleteWebsite()
        # Redirect to the /home route and render the home.html template
        return redirect(url_for('home'))

    #FINISHED
    def editPreset(self):
        self.editPresetClass.getEmail(self.curr_email)
        return render_template('EditPreset.html', presets=self.editPresetClass.query())
    
    def newEditedPreset(self):
        oldPreset=self.editPresetClass.editPreset()
        #turn timestamp that is in form: 1700691121.3678615
        #into a date
        timestamp = str(time.ctime(oldPreset['timestamp']))
        return render_template('EditPresetNew.html', oldPreset=oldPreset,masterList=self.editPresetClass.query1(), timestamp=timestamp)
    
    def edit(self):
        self.editPresetClass.editPreset1()
        return redirect(url_for('home'))

    #FINISHED
    def addWebsite(self):
        self.addWebsiteClass.getEmail(self.curr_email)
        return render_template('AddWebsite.html')
    
    def newAddedWebsite(self):
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

    # NOT USED
    # def checkForData(self, queryRequest):
    #     #ANTHONY
    #     initialDataID = False
    #     while self.app.dataQ.empty() != True:
    #         newData = self.app.dataQ.get()
    #         if newData['id'] == initialDataID:
    #             self.app.requestQ.put(queryRequest)
    #             time.sleep(1) #import time
    #             initialDataID = False
    #         elif initialDataID == False:
    #             initialDataID = newData['id']
    #         if newData['id'] == queryRequest['id']:
    #             if newData['data'] is not False:
    #                 return newData
    #         else:
    #             self.app.dataQ.put(newData)

def startFlask(requestQ, dataQ):
    newFlask = MyFlaskApp(requestQ, dataQ)
    newFlask.run()

# Usage
if __name__ == '__main__':
    request_queue = Queue()
    data_queue = Queue()
    my_flask_app = MyFlaskApp(request_queue, data_queue)
    my_flask_app.run()
