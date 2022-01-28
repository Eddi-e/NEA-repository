
from googleapiclient.discovery import build

from youtube_transcript_api import YouTubeTranscriptApi

import json

import sqlite3

import os

ApiKey = "AIzaSyA2az7pxj2NqMyP95xdybDDLX9RzBO6q-k"
youtube = build('youtube','v3',developerKey = ApiKey)
class api():
    def __init__(self):
        self.enddate = self.fileread(0)
        self.startdate = self.fileread(1)
        self.topics = self.fileread(2)
        self.ApiKey = ""
    
    def fileread(self):
        pass
    


class youtubeapi(api):

    def fileread(self,mode):

        file = open("userchoices.txt","r")
        filelinelist = []
        nolinecharslist = []
        for lines in file:
            filelinelist.append(lines)
        for i in filelinelist:
            nolinecharslist.append(i.strip())
        if mode == 0:
            return str(nolinecharslist[0])
        elif mode == 1:
            return str(nolinecharslist[1])
        elif mode == 2:
            topicsplit = []
            topicsplit = nolinecharslist[2].split(",")
            topicaddition = ""
            if len(topicsplit) > 1:
                topicaddition = topicaddition + (topicsplit[0])
                for i in topicsplit:
                    topicaddition = topicaddition + ("|")
                    topicaddition = topicaddition + i
                    return(topicaddition)
            else:
                return(topicsplit[0])
    def youtubesearch(self):

        for x in self.enddate:
            print (x)
        request = youtube.search().list(
            part=("snippet"),
            maxResults=5,
            publishedBefore=str(self.enddate),
            publishedAfter=str(self.startdate),
            q=(self.topics)
            )
        feedback = request.execute()
        return (feedback)

    def requesttovidid(self,feedback):
        print(feedback)
        idreturn = []
        jsonstring = json.dumps(feedback)
        loadedjson = json.loads(jsonstring)
        for x in range(0,5):
            video1items = ((loadedjson['items'])[x])
            try:
                idreturn.append(((video1items['id'])['videoId']))
            except:
                idreturn.append(((video1items['id'])['playlistId']))
        return(idreturn)

def getid(TopicID):
    con = sqlite3.connect('databaseforwebapp.db')
    cursor = con.cursor()
    row = cursor.execute("SELECT topicName FROM topic WHERE topicID=trim(?)",(TopicID,))
    topicname = row.fetchone()[0]
    print(topicname)
    

if __name__ == '__main__':
    print(os.listdir())
    class1 = youtubeapi()
    store = (class1.youtubesearch())
    #store = {'kind': 'youtube#searchListResponse', 'etag': 'sl-06UJGHaatbnBHU-4ATtIjwiA', 'nextPageToken': 'CAUQAA', 'regionCode': 'GB', 'pageInfo': {'totalResults': 1000000, 'resultsPerPage': 5}, 'items': [{'kind': 'youtube#searchResult', 'etag': 'DKSI3NiZuULHvOyKFebhrCyJtFc', 'id': {'kind': 'youtube#video', 'videoId': 'YWd7_bwzdkw'}, 'snippet': {'publishedAt': '2019-12-11T17:00:09Z', 'channelId': 'UCB_qr75-ydFVKSF9Dmo6izg', 'title': 'Rookie Of The Year 2019: Norris, Russell or Albon?', 'description': 'Three fresh-faced rookies, each with an incredible debut season under their belts. We asked Lando Norris, George Russell and Alex Albon to pitch why THEY ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/YWd7_bwzdkw/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/YWd7_bwzdkw/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/YWd7_bwzdkw/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'FORMULA 1', 'liveBroadcastContent': 'none', 'publishTime': '2019-12-11T17:00:09Z'}}, {'kind': 'youtube#searchResult', 'etag': 'kvrgFFPVjAtj_sjjqwahnb-a08o', 'id': {'kind': 'youtube#video', 'videoId': 'MgTUfVfuMBI'}, 'snippet': {'publishedAt': '2019-12-11T20:30:00Z', 'channelId': 'UCB_qr75-ydFVKSF9Dmo6izg', 'title': 'Funniest F1 Moments of 2019!', 'description': "Before the racing, after the racing, and even during... there's always time to laugh! For more F1® videos, visit http://www.Formula1.com Like F1® on Facebook: ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/MgTUfVfuMBI/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/MgTUfVfuMBI/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/MgTUfVfuMBI/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'FORMULA 1', 'liveBroadcastContent': 'none', 'publishTime': '2019-12-11T20:30:00Z'}}, {'kind': 'youtube#searchResult', 'etag': 's5Z4Ok3q0J88ozfhN7qDv7yJGA4', 'id': {'kind': 'youtube#video', 'videoId': 'SFpQmwkBo4c'}, 'snippet': {'publishedAt': '2019-12-11T20:35:40Z', 'channelId': 'UCEY1ejsweY4DgMwOVJeEaBA', 'title': 'Jess Folley&#39;s star quality shines with &#39;Survivor&#39;  | X Factor: The Band | Arena Auditions', 'description': "16-year-old Jess Folley was the first to take the stage at the Arena Auditions, and she smashed it out of the park with Destiny's Child's super-hit 'Survivor'.", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/SFpQmwkBo4c/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/SFpQmwkBo4c/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/SFpQmwkBo4c/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'The X Factor UK', 'liveBroadcastContent': 'none', 'publishTime': '2019-12-11T20:35:40Z'}}, {'kind': 'youtube#searchResult', 'etag': 'WH1UJddeT1EuRAYOoF0njax080g', 'id': {'kind': 'youtube#video', 'videoId': 'O6SVU0PSNW8'}, 'snippet': {'publishedAt': '2019-12-11T12:00:03Z', 'channelId': 'UCP-Ng5SXUEt0VE-TXqRdL6g', 'title': 'Good Chemistry – LEGO Hidden Side Episode 8', 'description': "It's not a cannon, it's a negaton pulse conversion beam. And don't call it a haunted bottle – it's an Erlenmeyer flask… with a big ghost in it. This LEGO® Hidden ...", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/O6SVU0PSNW8/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/O6SVU0PSNW8/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/O6SVU0PSNW8/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'LEGO', 'liveBroadcastContent': 'none', 'publishTime': '2019-12-11T12:00:03Z'}}, {'kind': 'youtube#searchResult', 'etag': 'LEFiOivsYNWGGnG7tb6oM591piM', 'id': {'kind': 'youtube#video', 'videoId': 'XKJiOhoOJvY'}, 'snippet': {'publishedAt': '2019-12-11T10:00:11Z', 'channelId': 'UCUmC7gXciukRv73CQRQ5QGQ', 'title': 'Bring Me The Horizon - Ludens: Live in Tokyo', 'description': 'вrιng мe тнe нorιzon - “lυdenѕ” oυт now! https://smarturl.it/Ludens?IQid=YT waтcн тнe oғғιcιal vιdeo: ...', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/XKJiOhoOJvY/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/XKJiOhoOJvY/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/XKJiOhoOJvY/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'BMTHOfficialVEVO', 'liveBroadcastContent': 'none', 'publishTime': '2019-12-11T10:00:11Z'}}]}
    videoid = (class1.requesttovidid(store))
    print(videoid)
    for x in videoid:
        print(YouTubeTranscriptApi.get_transcript(x))            

