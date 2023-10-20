#to get flask on your computers
# pip install flask
# python app.py
# this simply adds routes for the sites that will allow different sites to be hit. 
from controllers.trackWebsite import TrackWebsite
from flask import Flask, render_template, request
import uuid
from multiprocessing import Queue as Q

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/addPreset')
def addPreset():
    return render_template('AddPreset.html')

@app.route('/addPreset/newAddedPreset',methods=['POST'])
def newAddedPreset():
    url = request.form['url']
    print('url: ', url)
    trackWebsite = TrackWebsite()
    print(type(trackWebsite))
    
    #request 1: INSERT URL: needs (UUID, request_type=[insert,remove,or request], column=[masterlist, websiteData, presets, users], 'query'=actual data)
    # {'id':uuid.uuid4(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'}    
    info = q.put({'id':uuid.uuid4(),
                  'request_type':'insert',
                  'column':'presets',
                  'query':str(url)
                  })
    
    #request 2: RETRIEVAL OF MASTER LIST
    
    # request 3 INSERT OF PRESET 
    return 'URL INFO<br/> %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (info), url 

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
    url = request.form['url']
    print('url: ', url)
    trackWebsite = TrackWebsite()
    print(type(trackWebsite))
    
    #request 1: INSERT URL
    info = q(str(url))
    
    #request 2: RETRIEVAL OF MASTER LIST
    
    # request 3 INSERT OF PRESET 
    
    
    # call a function that
    # will give me some cool graphs and info on that website
    # Possibly a thing that sends
    # the url to the client right here
    # return 'Hello %s %s have fun learning python <br/> <a href="/">Back Home</a>' % (first_name, last_name)
    return 'URL INFO<br/> %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (info), url 




def startFlask(q):#parameter: multiproccessor.Queue
    app.run(host="0.0.0.0", port=7777)#, debug=True)

# if __name__ == '__main__':
#     startFlask()
    