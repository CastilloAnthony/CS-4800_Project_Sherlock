#VIEWS

#to get flask on your computers
# pip install flask
# python app.py
# this simply adds routes for the sites that will allow different sites to be hit. 
# from controllers.trackWebsite import TrackWebsite
from flask import Flask, render_template, request
# from controllers.trackWebsite import TrackWebsite
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
    #TODO: grab all the items in the masterlist send it to the template: AddPreset.html then make a form that has all the presets with checkboxxes next to all of them 
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
            # for url in newData['data']['url']:
            list_of_masterlist_urls.append(newData['data']['url'])
        if newData['data'] == False:
            #Sorry
            pass
    else:
        x.append(newData['id'])

    #print('list_of_masterlist_urls')
    #[{'id': UUID('8a452346-3a5e-49f1-8190-c954a70d4a74'), 'data': {'_id': ObjectId('6531c3b37a653892efba49ec'), 'url': 'www.google.com'}}]
    
    return render_template('AddPreset.html', masterList = list_of_masterlist_urls)

@app.route('/addPreset/newAddedPreset',methods=['POST'])
def newAddedPreset():
    #for incorrect data comming in
    x = [] 
    # TODO: read in the items that were checkboxxed before the submit button was pressed. 
    # TODO: those that were pressed should then request the information on those respective urls via database
    # TODO: grab that information and present the data in this file. 
    presetLists = request.form['presetsList']
    name = request.form['name']
    
    print('name: ', name)
    
    #request 1: INSERT URL: 
    # needs (UUID, request_type=[insert,remove,or request], column=[masterList, pollingData, presets, users], 'query'=actual data)
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
def viewPresets():
    
    #WE WANT TO GRAB ALL THE REQUESTS AND HAVE THEM DISPLAYED ON THE PAGE... 
    #MAYBE WITH A LIMIT OF 5 PRESETS PER PAGE AS WELL AS HAVE  A BUTTON THAT
    #CAN LET'S YOU SEE THE NEXT 5 PRESETS
    
    #GRABBING ALL OF THE PRESETS
    
    presetRequest = {'id':uuid.uuid4(),
                  'request_type':'insert',
                  'column':'masterList',
                  'query': {}          
                  }
    app.requestQ.put(presetRequest)
    
    #ALL PRESETS ARE IN allPresets
    
    allPresets = app.dataQ.get() 
    
    #SENDING PRESETS FROM allPresets INTO THE viewPresets.html
    
    render_template('viewPreset.html', allPresets = allPresets)
    
    
#########################################################################################################################################################
#########################################################################################################################################################        
@app.route('/deletePreset')
def deletePreset():
    #SEE WHAT PRESETS WANT TO BE DELETED
    presetsRequest = {'id':uuid.uuid4(),
                  'request_type':'request',
                  'column':'masterList',
                  'query': {}          
                  }
    app.requestQ.put(presetsRequest)
    
    #ALL PRESETS ARE IN allPresets
    
    presets = app.dataQ.get() 
    
    return render_template('DeletePreset.html', presets = presets)

@app.route('/deletePreset/deletedPresets', methods=['POST'])
def deletedPresets():
    deletedPresets = request.form['url']
    #WE NEED TO FIND OUT WHAT HAPPENS WHEN USER SELECTS MULTIPLE, DOES DELETEPRESETS RETURN A LIST OR JUST ONE THING?
    
    #IF LIST
    for preset in deletedPresets:
        deletePresetRequest = {'id':uuid.uuid4(),
                  'request_type':'remove',
                  'column':'masterList',
                  'query': preset          #preset might need to be in a dictionary
                  }
    
    #IF SINGLE 
    deletePresetRequest = {'id':uuid.uuid4(),
                  'request_type':'remove',
                  'column':'masterList',
                  'query': deletedPresets          #preset might need to be in a dictionary
                  }
    
    #IF ALL IS WELL, WE SHOULD SEND A "DELETION WAS SUCCESSFULL MESSAGE AND RETURN THE DELETED PRESETS TO CONFIRM WITH USER"
    # return 'URL INFO<br/> %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (info), url 
    
    return 'Deleted Presets<br/> %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (deletedPresets) 
#########################################################################################################################################################
#########################################################################################################################################################    



@app.route('/deleteWebsite')
def deleteWebsite():
    return render_template('DeleteWebsite.html')

@app.route('/editPreset')
def editPreset():
    return render_template('EditPreset.html')

@app.route('/addWebsite') #add website // trackWebsite
def trackWebsite():
    return render_template('AddWebsite.html') #add website // trackWebsite
    
# We are going to request some data in
# trackWebsite specifically the url
# and then we will return the url so that we
# can send it to the client

@app.route('/addWebsite/addedWebsite',methods=['POST'])
def addWebsite():
    x = []
    url = request.form['url']
    # print('url: ', url)
    # trackWebsite = TrackWebsite()
    # print(type(trackWebsite))
    
    #request 1: INSERT URL
    one = {'id':uuid.uuid4(),
                  'request_type':'insert',
                  'column':'masterList',
                  'query': url          
                  }
    app.requestQ.put(one)

    
    x = [{"number":1},{"number":2}]
    # call a function that
    # will give me some cool graphs and info on that website
    # Possibly a thing that sends
    # the url to the client right here
    # return 'Hello %s %s have fun learning python <br/> <a href="/">Back Home</a>' % (first_name, last_name)
    # return 'URL INFO<br/> %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (info), url 
    return render_template('AddWebsite_new.html', url=url, x=x)


#REQUESTQ:Q IS FOR 
#INSERT: No get() needed, REMOVE: no get() needed, REQUEST: get() needed 
# needs (UUID, request_type=[insert,remove,or request], column=[masterList, pollingData, presets, users], 'query'=actual data)

#COLLECTIONS
# users = information on users such as password, username, email
# pollingData = polled data for websites. This has hundreds of thousands, do not poll from this unless you are graphing or do analytics
# presets = holds set of websites ["google.com", "bing.com", "burgerking.com"] 
# masterList = list of urls that need to be polled

#{'id':uuid.uuid4(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'} 

#RETURNS NOTHING 

#DATA_Q:Q IS 
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
    