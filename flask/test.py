from flask import Flask, render_template, request, session, url_for
from werkzeug.utils import redirect
import sqlite3
import random
import json
from datetime import datetime
from hashfunction import hashfunc

app = Flask(__name__)
app.config.update(SECRET_KEY="b'\xec\xadF;\x94\xc0&J\xe7\n\xc7w\x9elNg'")




@app.route("/", methods=['GET'])
def home():
    return redirect(url_for('login'))


@app.route("/createtopic", methods=['GET','POST'])
def topiccreate():
    if request.method == 'POST':
        topicname = request.form["topicname"]     
        topicname1 = topicname.replace(" ", "_")
        topicdesc=request.form["topicdesc"]
        topicdesc1 = topicdesc.replace(" ", "_")
        con = sqlite3.connect('databaseforwebapp.db')
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO topic (topicName, topicDescription) VALUES (?, ?)",
            (topicname1, topicdesc1),
            )
        con.commit()
        return render_template('topic.html')
    return render_template('topic.html')

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




@app.route("/topicchoice",methods=['GET','POST'])
def topic():

    if request.method == 'POST':
        userID1 = session['userID']
        topic = request.form.get("topics")
        mediaS = request.form.get("mediasource")
        mediaT = request.form.get("mediatype")
        dayChoice = request.form.getlist("day")
        print(dayChoice)
        counter1 = ("")
        for num in dayChoice:
            counter1 = counter1 + num

        con = sqlite3.connect('databaseforwebapp.db')
        cursor = con.cursor()

        row = cursor.execute("SELECT topicID FROM topic WHERE topicName=trim(?)",(topic,))
        topicid = row.fetchone()
        topicid = topicid[0]

        date = datetime.today()
        date = str(date).split(" ")[0]
        date = date.replace("-","")
        date = int(date)

        row = cursor.execute("SELECT mediaSourceID FROM mediaSource WHERE mediaSourceName=trim(?)",(mediaS,))
        mediaS = row.fetchone()
        mediaS = mediaS[0]

        row = cursor.execute("SELECT mediaTypeID FROM mediaType WHERE mediaName=trim(?)",(mediaT,))
        mediaT = row.fetchone()
        mediaT = mediaT[0]

        cursor.execute(
            "INSERT INTO userTopic (userID, topicID, startDate) VALUES (?, ?, ?)",
            (userID1, topicid, date,)
            )

        cursor.execute("SELECT userTopicID FROM userTopic WHERE topicID=trim(?) AND userID=trim(?) AND startDate=trim(?)",(topicid,userID1,date))
        usertopicid = row.fetchone()
        usertopicid = usertopicid[0]

        cursor.execute(
            "INSERT INTO scheduling (mediaSourceID, mediaTypeID, userTopicID, day) VALUES (?, ?, ?, ?)",
            (mediaS, mediaT, usertopicid, counter1)

        )
        


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
        row = con.execute("SELECT * FROM scheduling")
        print(row.fetchall)
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