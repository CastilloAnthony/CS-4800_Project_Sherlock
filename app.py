from flask import Flask, render_template
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


if __name__ == '__main__':
    app.run(debug=True)
    