#VIEWS

#to get flask on your computers
# pip install flask
# python app.py
# this simply adds routes for the sites that will allow different sites to be hit. 
# from controllers.trackWebsite import TrackWebsite
from flask import Flask, render_template, request
from controllers.trackWebsite import TrackWebsite
import uuid
from multiprocessing import Queue as Q

app = Flask(__name__)
#requestQ = False
#dataQ = False
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/addPreset')
def addPreset():
    x = []
    #WE NEED A LIST OF ALL THE THINGS IN THE MASTER LIST
    masterListRequest = {'id':uuid.uuid4(),
                        'request_type':'request',
                        'column':'masterList',
                        'query': {}                
                  }
    
    app.requestQ.put(masterListRequest)
    list_of_masterlist_urls = []
    newData = app.dataQ.get() # {'id':uuid.uuid4(), 'data':data}
    #RETURNS DICTIONARY: Object and URL
    if newData['id'] == masterListRequest['id']:
        if newData['data'] != False:
            #   USE NEWDATA
            for key in newData['data']:
                masterList.append(key)
        if newData['data'] == False:
            #Sorry
            pass
    else:
        x.append(newData)

    
    
    return render_template('AddPreset.html', masterList = masterList)

@app.route('/addPreset/newAddedPreset',methods=['POST'])
def newAddedPreset():
    #for incorrect data comming in
    x = [] 
    presetLists = request.form['presetsList']
    name = request.form['name']
    
    print('url: ', url)
    trackWebsite = TrackWebsite()
    print(type(trackWebsite))
    
    #request 1: INSERT URL: 
    # needs (UUID, request_type=[insert,remove,or request], column=[masterList, websiteData, presets, users], 'query'=actual data)
    # {'id':uuid.uuid4(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'}    
    
    
    # requestQ.put({'id':uuid.uuid4(),
    #               'request_type':'insert',
    #               'column':'presets',
    #               'query':name
    #               })
    
    
    masterListRequest = {'id':uuid.uuid4(),
                        'request_type':'request',
                        'column':'masterList',
                        'query': {}                
                  }
    
    #request 1: RETRIEVAL OF MASTER LIST
    app.requestQ.put(masterListRequest)
    #   GOTTA CHECK THE DATA QUEUE FOR THE DATA
    newData = app.dataQ.get() 
    #RETURNS DICTIONARY: Object and URL
    if newData['id'] == masterListRequest['id']:
        if newData['data'] != False:
            #   USE NEWDATA
            pass
                
        if newData['data'] == False:
            #Sorry
            pass
    else:
        x.append(newData)
    
            
            
        
    #FOR EVERY ITEM ON THE MASTERLIST HAVE A CHECKBOX THAT
    #
    userDictionary = {
        'name':name, #STRING
        'presetLists':presetLists #LIST
    }
    
    newPreset = {'id':uuid.uuid4(),
                  'request_type':'insert',
                  'column':'presets',
                  'query': userDictionary          #nameOfPreset and list of websites
                  }
    
    # request 2 INSERT OF PRESET 
    app.requestQ.put(newPreset)
    
    # return 
    return 0

#WILL BE USED FOR VIEWING PRESETS INFORMATION
@app.route('/viewPresets')

@app.route('/deletePreset')
def deletePreset():
    return render_template('DeletePreset.html')

@app.route('/deleteWebsite')
def deleteWebsite():
    return render_template('deleteWebsite.html')

@app.route('/editPreset')
def editPreset():
    return render_template('EditPreset.html')

@app.route('/trackWebsite') #add website // trackWebsite
def trackWebsite():
    return render_template('TrackWebsite.html') #add website // trackWebsite
    
# We are going to request some data in
# trackWebsite specifically the url
# and then we will return the url so that we
# can send it to the client

@app.route('/trackWebsite/newTrackedWebsite',methods=['POST'])
def addWebsite():
    x = []
    url = request.form['url']
    print('url: ', url)
    # trackWebsite = TrackWebsite()
    # print(type(trackWebsite))
    
    #request 1: INSERT URL
    app.requestQ.put({
        
    })
    
    #request 2: RETRIEVAL OF MASTER LIST
    
    # request 3 INSERT OF PRESET 
    
    # request = {
    #     'id':uuid.uuid4(),
    #     'request_type':'insert',
    #     'column':'presets',
    #     'query': url
    # }
    
    # requestQ.put(request)
    # newData = dataQ.get() 
    # info = ""
    # #RETURNS DICTIONARY: Object and URL
    # if newData['id'] == request['id']:
    #     if newData['data'] != False:
    #         #   USE NEWDATA
    #         pass
                
    #     if newData['data'] == False:
    #         #Sorry
    #         pass
    # else:
    #     x.append(newData)
    
    x = [{"number":1},{"number":2}]
    # call a function that
    # will give me some cool graphs and info on that website
    # Possibly a thing that sends
    # the url to the client right here
    # return 'Hello %s %s have fun learning python <br/> <a href="/">Back Home</a>' % (first_name, last_name)
    # return 'URL INFO<br/> %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (info), url 
    return render_template('som.html', url=url, x=x)


#REQUESTQ:Q IS FOR 
#INSERTS, REMOVES, REQUESTS
#{'id':uuid.uuid4(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'}   
#RETURNS NOTHING 

#DATA_Q:Q IS FOR
# NONE
#RECEIVES
#RETURNS {'uuid':uuid.uuid4(), 'data':data}

#   EVERY REQUESTQ.PUT YOU DO , DO A DATAQ.GET

def startFlask(requestQ:Q, dataQ:Q):#parameter: multiproccessor.Queue
    app.requestQ = requestQ
    app.dataQ = dataQ
    app.run(host="0.0.0.0", port=7777)#, debug=True)

# if __name__ == '__main__':
#     startFlask(Q,Q)
    