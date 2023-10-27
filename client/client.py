from flask import Flask, render_template, request
import uuid
import time
from multiprocessing import Queue
from controllers.addPreset import AddPreset
from controllers.deletePreset import DeletePreset 
from controllers.editPreset import EditPreset 
import controllers.graphTableGenerator
from controllers.addWebsite import AddWebsite 
#CALL THE CLASES



class MyFlaskApp:
    def __init__(self, requestQ:Queue, dataQ:Queue):
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        self.app.requestQ = requestQ
        self.app.dataQ = dataQ

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/addPreset', 'addPreset', self.addPreset)
        self.app.add_url_rule('/addPreset/newAddedPreset', 'newAddedPreset', self.newAddedPreset, methods=['POST'])
        self.app.add_url_rule('/viewPresets', 'viewPresets', self.viewPresets)
        self.app.add_url_rule('/deletePreset', 'deletePreset', self.deletePreset)
        self.app.add_url_rule('/deletePreset/deletedPresets', 'deletedPresets', self.deletedPresets, methods=['POST'])
        self.app.add_url_rule('/deleteWebsite', 'deleteWebsite', self.deleteWebsite)
        self.app.add_url_rule('/editPreset', 'editPreset', self.editPreset)
        self.app.add_url_rule('/addWebsite', 'trackWebsite', self.trackWebsite)
        self.app.add_url_rule('/addWebsite/addedWebsite', 'addWebsite', self.addWebsite, methods=['POST'])
        
        self.addPresetClass = AddPreset(self.app.requestQ, self.app.dataQ)

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
        presetsRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'masterList',
            'query': {}
        }
        self.app.requestQ.put(presetsRequest)
        presets = self.app.dataQ.get()
        return render_template('DeletePreset.html', presets=presets)

    def deletedPresets(self):
        deletedPresets = request.form.getlist('url')
        for preset in deletedPresets:
            deletePresetRequest = {
                'id': uuid.uuid4(),
                'request_type': 'remove',
                'column': 'masterList',
                'query': preset
            }
            self.app.requestQ.put(deletePresetRequest)
        return 'Deleted Presets<br/> %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (deletedPresets)

    def deleteWebsite(self):
        return render_template('DeleteWebsite.html')

    def editPreset(self):
        return render_template('EditPreset.html')
    
    #grabbing Data
    def trackWebsite(self):
        return render_template('AddWebsite.html')
    
    #show Data is put in 
    def addWebsite(self):
        message = self.AddWebsite.addWebsite()
        
        return render_template('AddWebsite_new.html', message)

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
