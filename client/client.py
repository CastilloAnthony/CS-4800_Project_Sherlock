from flask import Flask, render_template, request
import uuid
import time
from multiprocessing import Queue

from controllers.addPreset import AddPreset
from controllers.deletePreset import DeletePreset 
from controllers.editPreset import EditPreset 
from controllers.addWebsite import AddWebsite 
from controllers.deleteWebsite import DeleteWebsite 

import controllers.graphTableGenerator

#CALL THE CLASES



class MyFlaskApp:
    def __init__(self, requestQ:Queue, dataQ:Queue):
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        self.app.requestQ = requestQ
        self.app.dataQ = dataQ
        
        #ROUTECREATING
        #Example: self.app.add_url_rule(route='<route>', name='<name>', function=<function>, OPTIONAL methods=[<typeOfRequest>])
        
        #HOMEPAGE
        self.app.add_url_rule('/', 'index', self.index)
        
        #FORPRESETS
        #ADDPRESET
        self.app.add_url_rule('/addPreset', 'addPreset', self.addPreset)
        self.app.add_url_rule('/addPreset/newAddedPreset', 'newAddedPreset', self.newAddedPreset, methods=['POST'])
        #DELETEPRESET
        self.app.add_url_rule('/deletePreset', 'deletePreset', self.deletePreset)
        self.app.add_url_rule('/deletePreset/newDeletedPreset', 'newDeletedPreset', self.newDeletedPreset, methods=['POST'])
        #VIEWPRESET
        self.app.add_url_rule('/viewPresets', 'viewPresets', self.viewPresets)
        #EDITPRESET
        self.app.add_url_rule('/editPreset', 'editPreset', self.editPreset)
        
        #FORWEBSITES
        #ADDWEBSITE
        self.app.add_url_rule('/addWebsite', 'addWebsite', self.addWebsite)
        self.app.add_url_rule('/addWebsite/newAddedWebsite', 'newAddedWebsite', self.newAddedWebsite, methods=['POST'])
        #DELETEWEBSITE
        self.app.add_url_rule('/deleteWebsite', 'deleteWebsite', self.deleteWebsite)
        self.app.add_url_rule('/deleteWebsite/newDeletedWebsite', 'newDeletedWebsite', self.newDeletedWebsite, methods=['POST'])
        
        
        #CLASS_INITIALIZATION
        self.addPresetClass = AddPreset(self.app.requestQ, self.app.dataQ)
        self.deletePresetClass = DeletePreset(self.app.requestQ, self.app.dataQ)
        self.editPresetClass = EditPreset(self.app.requestQ, self.app.dataQ)    
        
        self.addWebsiteClass = AddWebsite(self.app.requestQ, self.app.dataQ)
        self.deleteWebsiteClass = DeleteWebsite(self.app.requestQ, self.app.dataQ)        
            
        
        

    def index(self):
        return render_template('homepage.html')

    def addPreset(self):
        return render_template('AddPreset.html', masterList=self.addPresetClass.query())

    def newAddedPreset(self):
        self.addPresetClass.addPreset()
        return "YOU HAVE SUCCESSFULLY ADDED A PRESET PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>"

    def viewPresets(self):
        presetRequest = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'masterList',
            'query': {}
        }
        self.app.requestQ.put(presetRequest)
        allPresets = self.app.dataQ.get()
        return render_template('viewPreset.html', allPresets=allPresets)

    def deletePreset(self):
        return render_template('DeletePreset.html', presets=self.deletePresetClass.query())

    def newDeletedPreset(self):
        self.deletePresetClass.deletePreset()
        return "YOU HAVE SUCCESSFULLY ADDED A PRESET PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>"

    def deleteWebsite(self):
        return render_template('DeleteWebsite.html', masterList = self.deleteWebsiteClass.query())
    
    def newDeletedWebsite(self):
        self.deleteWebsiteClass.deleteWebsite()
        return "YOU HAVE SUCCESSFULLY DELETED A WEBSITE PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>"

    def editPreset(self):
        return render_template('EditPreset.html')
    
    #grabbing Data
    def addWebsite(self):
        return render_template('AddWebsite.html')
    
    #show Data is put in 
    def newAddedWebsite(self):
        self.addWebsiteClass.addWebsite()
        return "YOU HAVE SUCCESSFULLY ADDED A WEBSITE, PRESS THIS LINK TO GET BACK TO THE HOMEPAGE <br><br><a href='../'>Visit Homepage</a>"

    def run(self):
        self.app.run(host="0.0.0.0", port=7777)

    def newRequest(self, queryRequest):
        pass

    def checkForData(self, queryRequest):
        #ANTHONY
        initialDataID = False
        while self.app.dataQ.empty() != True:
            newData = self.app.dataQ.get()
            if newData['id'] == initialDataID:
                self.app.requestQ.put(queryRequest)
                time.sleep(1) #import time
                initialDataID = False
            elif initialDataID == False:
                initialDataID = newData['id']
            if newData['id'] == queryRequest['id']:
                if newData['data'] is not False:
                    return newData
            else:
                self.app.dataQ.put(newData)

def startFlask(requestQ, dataQ):
    newFlask = MyFlaskApp(requestQ, dataQ)
    newFlask.run()

# Usage
if __name__ == '__main__':
    request_queue = Queue()
    data_queue = Queue()
    my_flask_app = MyFlaskApp(request_queue, data_queue)
    my_flask_app.run()
