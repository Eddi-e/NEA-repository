from flask import Flask, render_template, request, session, url_for
from werkzeug.utils import redirect
import sqlite3
import random
import json
from hashfunction import hashfunc

app = Flask(__name__)
app.config.update(SECRET_KEY="b'\xec\xadF;\x94\xc0&J\xe7\n\xc7w\x9elNg'")

@app.route("/", methods=['GET'])
def home():
    return redirect(url_for('login'))


@app.route("/signup", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email=request.form["email"]
        password=hashfunc(request.form["password"])
        con = sqlite3.connect('databaseforwebapp.db')
        cursor = con.cursor()
        #try:
#          for row in cursor.execute("SELECT userID FROM user WHERE email=trim(?)",(email,)):#trim function removes extra spaces
#              list.append("")
        cursor.execute(
            "INSERT INTO user (email, password) VALUES (?, ?)",
            (email, password),
            )
        con.commit()
        return render_template('index.html')
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password=hashfunc(request.form["password"])
        con = sqlite3.connect('databaseforwebapp.db')
        row = con.execute("SELECT * FROM user WHERE email=trim(?)",(email,))#trim function removes extra spaces
        dbpass = row.fetchone()
        print(dbpass[2] == password)
        if (dbpass[2] == password):
            session['userID'] = dbpass[0]
            return redirect(url_for('topic'))
    return render_template('login.html')

@app.route("/topicchoice",methods=['GET','POST'])
def topic():
    userID = session['userID']
    print(userID)
    con = sqlite3.connect('databaseforwebapp.db')
    row = con.execute("SELECT userTopicID FROM userTopic WHERE userID=trim(?)",(userID,))
    userTopic = row.fetchall()
    print(userTopic)
    largeuserdic = {}
    for i in range(0,len(userTopic)):
        row = con.execute("SELECT mediaSourceID, mediaTypeID FROM scheduling WHERE userTopicID=trim(?)",(userTopic[i][0],))
        results = row.fetchone()
        mediasourceid = results[0]
        mediatypeid = results[1]
        row = con.execute("SELECT mediaSourceName FROM mediaSource WHERE mediaSourceID=trim(?)",(mediasourceid,))
        mediasource = row.fetchone()
        mediasourcename = mediasource[0]
        row = con.execute("SELECT mediaName FROM mediaType WHERE mediaTypeID=trim(?)",(mediatypeid,))
        mediatype = row.fetchone()
        mediatypename = mediatype[0]
        row = con.execute("SELECT topic.topicName FROM userTopic INNER JOIN topic ON topic.topicID=userTopic.topicID WHERE userTopicID=trim(?)",(userTopic[i][0],))
        topicrow = row.fetchone()
        topicname = topicrow[0]
        row = con.execute("SELECT day FROM scheduling WHERE userTopicID=trim(?)",(userTopic[i][0],))
        dayrow = row.fetchone()
        day = dayrow[0]
        print(mediasourcename,mediatypename,topicname,day)
        valueDic = {
            "mediasource" : mediasourcename,
            "mediatype" : mediatypename,
            "topicname" : topicname,
            "day" : day
        }
        largeuserdic[i] = valueDic
    print(largeuserdic)    
    valueJSON = json.dumps(largeuserdic)
        
    print(userTopic[0][0])
    return render_template('schedule.html',topics = valueJSON)


if __name__ == "__main__":
    app.run(debug=True)