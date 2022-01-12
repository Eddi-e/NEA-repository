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
        if (dbpass[2] == password):
            session['userID'] = dbpass[0]
            return redirect(url_for('topic'))
    return render_template('login.html')

@app.route("/topicchoice",methods=['GET','POST'])
def topic():

    if request.method == 'POST':
        print('hey')
        userID1 = session['userID']
        topic = request.form.get("topics")
        mediaS = request.form.get("mediasource")
        mediaT = request.form.get("mediatype")
        dayChoice = request.form.getlist("day")
        counter1 = ("")
        for num in dayChoice:
            counter1 = counter1 + num

        con = sqlite3.connect('databaseforwebapp.db')
        cursor = con.cursor()

        row = cursor.execute("SELECT topicID FROM topic WHERE topicName=trim(?)",(topic,))
        topicid = row.fetchone()

        cursor.execute(
            "INSERT INTO userTopic (userID, topicID) VALUES (?, ?)",
            (userID1, topicid),
            )
        cursor.execute("SELECT userTopicID FROM userTopic WHERE topicName=trim(?)",(topic,))
        
        con.commit()
        
        print(topic,mediaS,mediaT,dayChoice, counter1)

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
    valueJSON = json.dumps(largeuserdic)

    row = con.execute("SELECT topicName FROM topic")
    topiclist = row.fetchall()
    topicDIC = {}
    for x in range(0,len(topiclist)):
        topicDIC[x] = topiclist[x][0]

    topicJSON = json.dumps(topicDIC)

    row = con.execute("SELECT mediaSourceName FROM mediaSource")
    mediaSource = row.fetchall()
    mediaSourceDIC = {}
    for x in range(0,len(mediaSource)):
        mediaSourceDIC[x] = mediaSource[x][0]
    mediaSourceJSON = json.dumps(mediaSourceDIC)
    row = con.execute("SELECT mediaName FROM mediaType")
    mediaType = row.fetchall()
    mediaTypeDIC = {}
    for x in range(0,len(mediaType)):
        mediaTypeDIC[x] = mediaType[x][0]
    mediaTypeJSON = json.dumps(mediaTypeDIC)

    print(topicJSON)
    return render_template('schedule.html',topics= valueJSON, topiclist= topicJSON, mediaSourcelist= mediaSourceJSON, mediaTypelist= mediaTypeJSON)


if __name__ == "__main__":
    app.run(debug=True)