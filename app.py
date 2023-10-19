#to get flask on your computers
# pip install flask
# python app.py
# this simply adds routes for the sites that will allow different sites to be hit. 
# import pymongo
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/addPreset')
def addPreset():
    return render_template('AddPreset.html')

@app.route('/deletePreset')
def deletePreset():
    return render_template('DeletePreset.html')

@app.route('/deleteWebsite')
def deleteWebsite():
    return render_template('deleteWebsite.html')

@app.route('/editPreset')
def editPreset():
    return render_template('EditPreset.html')

@app.route('/trackWebsite')
def trackWebsite():
    return render_template('TrackWebsite.html')
    
# We are going to request some data in
# trackWebsite specifically the url
# and then we will return the url so that we
# can send it to the client

@app.route('/trackWebsite/newTrackedWebsite',methods=['POST'])
def newPreset():
    url = request.form['url']
    print('url: ', url)
    # call a function that
    # will give me some cool graphs and info on that website
    # Possibly a thing that sends
    # the url to the client right here
    return 'URL = %s <br/> <a href="/trackWebsite">TrackWebsite</a>' % (url), url



if __name__ == '__main__':
    app.run(debug=True)
    