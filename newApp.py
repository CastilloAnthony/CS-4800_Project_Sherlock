from flask import Flask, render_template, request
import uuid
from multiprocessing import Queue

class MyFlaskApp:
    def __init__(self, requestQ, dataQ):
        self.app = Flask(__name__)
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

    def index(self):
        return render_template('homepage.html')

    def addPreset(self):
        x = []
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'masterList',
            'query': {}
        }
        self.app.requestQ.put(masterListRequest)
        list_of_masterlist_urls = []
        newData = self.app.dataQ.get()
        if newData['id'] == masterListRequest['id']:
            if newData['data'] is not False:
                list_of_masterlist_urls.append(newData['data']['url'])
        return render_template('AddPreset.html', masterList=list_of_masterlist_urls)

    def newAddedPreset(self):
        x = []
        presetLists = request.form['presetsList']
        name = request.form['name']
        userDictionary = {
            'name': name,
            'presetLists': presetLists
        }
        newPreset = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'presets',
            'query': userDictionary
        }
        self.app.requestQ.put(newPreset)
        return '0'

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

    def trackWebsite(self):
        return render_template('AddWebsite.html')

    def addWebsite(self):
        x = []
        url = request.form['url']
        one = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'masterList',
            'query': url
        }
        self.app.requestQ.put(one)
        x = [{"number": 1}, {"number": 2}]
        return render_template('AddWebsite_new.html', url=url, x=x)

    def run(self):
        self.app.run(host="0.0.0.0", port=7777)

# Usage
if __name__ == '__main__':
    request_queue = Queue()
    data_queue = Queue()
    my_flask_app = MyFlaskApp(request_queue, data_queue)
    my_flask_app.run()
