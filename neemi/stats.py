import time,datetime

from django.http import HttpResponseRedirect, HttpResponse

from mongoengine.queryset import DoesNotExist, MultipleObjectsReturned
from mongoengine.django.auth import User
from mongoengine.connection import get_db

from pymongo import MongoClient

from models import *

class DBAnalysis(object):

    def __init__(self, request=None):
        self.url = '/get_stats/'
        self.mongo_db = get_db()
        self.file = open('statistic.txt', 'a')
        self.html_stats = []

        print "mongoDB: ", self.mongo_db
        print "username: ", request.user.username

        cursor = self.mongo_db['user'].find({'username':request.user.username})

        self.currentuser = ''
        for data in cursor:
            if '_id' in data.keys():                
                self.currentuser = data['_id']


    def basic_stats(self):
        print [self.mongo_db]
        self.printStats(text = "\n ------------------------------------ \n")
        self.printStats(text = "===> Statistics - " + time.strftime("%c"))

        dbStats = self.mongo_db.command("dbstats")

        self.printStats(text = "Total size in bytes of the data held in this database: " + str(dbStats['dataSize']))
        self.file.write("Average size of each document in bytes: " + str(dbStats['avgObjSize']) + '\n')
        self.printStats(text = "Number of objects: " + str(dbStats['objects']))
        self.printStats(text = "Number of collections: " + str(dbStats['collections']))
        self.printStats(text = "")

        collectionsList = self.mongo_db.collection_names()
        self.printStats(text = "Collections: ")
        for item in collectionsList:
            if item.find('data') != -1:
                try:
                    self.printStats(text = "----")
                    self.printStats(text = item)

                    colStats = self.mongo_db.command("collstats", item)
                    self.printStats(text = "Number of documents: " + str(colStats['count']))
                    self.printStats(text = "Collection size in bytes: " + str(colStats['size']))
                    if (colStats['count'] > 0):
                        self.printStats(text = "Average object size in bytes: " + str(colStats['avgObjSize']))
                    self.printStats(text = "")
                    self.collectionAnalysis(collection = item)
                except Exception as e:
                    print 'Error:', e
                    continue

        #return HttpResponseRedirect(self.url)
        return self.html_stats


    def collectionAnalysis(self, collection=None):
        dbcollection = self.mongo_db[collection]
        docs = dbcollection.find({"neemi_user" : self.currentuser})

        data_types = set()
        count = {}

        if (collection == 'dropbox_data') or (collection == 'facebook_data') or (collection == 'gcal_data') or (collection == 'linked_in_data') or (collection == 'gmail_data') or (collection == 'foursquare_data'):
            for data in docs:
                if 'data_type' in data.keys():                
                    data_type = data['data_type']
                    count[data_type] = count.get(data_type, 0) + 1   
#                else:
#                    print data
        elif (collection == 'gcontacts_data'):
            for data in docs:
                if 'data_type' in data.keys():
                    data_type = data['data_type']
                    count[data_type] = count.get(data_type, 0) + 1
                    string = data['data'][1:len(data['data']) - 1] 
        elif (collection == 'gplus_data'):   
            for data in docs:
                if 'data_type' in data.keys():
                    data_type = data['data_type']
                    count[data_type] = count.get(data_type, 0) + 1
#                else:
#                    print data
        elif (collection == 'twitter_data'):
            friends = set()
            followers =set()
            for data in docs:
                if 'data_type' in data.keys():
                    #print data['data'][0][1]
                    #return
                    data_type = data['data_type']
                    if data_type == 'FRIEND':
                        friends.add(data['data']['screen_name'])
                    elif data_type == 'FOLLOWER':
                        followers.add(data['data']['screen_name'])
                    elif data_type == 'TIMELINE':
                        #print data['data'].keys()
                        pass
                    count[data_type] = count.get(data_type, 0) + 1
#                else:
#                    print data

        for x in count: 
            self.printStats(text = str(x) + ': ' + str(count[x]))

    def printStats(self, text=None):
        print text
        self.file.write(text + '\n')
        self.html_stats.append(text)
        						
									
									
									















class DBTopkFacebook(object):

    def __init__(self, request=None):
        self.url = '/get_topk/'
        self.mongo_db = get_db()
        self.file = open('topk.txt', 'a')
        self.topk = []

        print "mongoDB: ", self.mongo_db
        print "username: ", request.user.username

        cursor = self.mongo_db['user'].find({'username':request.user.username})

        self.currentuser = ''
        for data in cursor:
            if '_id' in data.keys():                
                self.currentuser = data['_id']


    def top_stats(self):
        print [self.mongo_db]
        pipeline =[ {'$match':{'data_type':'STATUS'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.updated_time", 'like_count':{'$sum':1}}},{'$sort':{'like_count':-1}},{'$limit':10},{'$project': {"_id":0, "updated_time":"$_id","like_count": 1}} ]
        facebook_data =self.mongo_db.facebook_data
        topStats=self.mongo_db.command('aggregate','facebook_data',pipeline=pipeline)
        # topStats=self.mongo_db.facebook_data.aggregate([ {'$match':{'data_type':'STATUS'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.updated_time", 'like_count':{'$sum':1}}},{'$project': {"_id":0, "updated_time":"$_id","like_count": 1}} ])
        # topStats = self.mongo_db.command("dbstats")
        print len(topStats.items())
        #print topStats['result'].items()
        x=topStats[u'result']
        k=[]
        i=0
        for d in x:
         k.append([])
         for j in xrange(1):
		 k[i].append((d[u'like_count']))
         k[i].append((d[u'updated_time']))
         i+=1
        #for post in iter(topStats):
         #print post
         # print 'prashant'
        self.printStats(text = str(topStats))
        # self.printStats(text = "Total size in bytes of the data held in this database: " + str(dbStats['dataSize']))
        # self.file.write("Average size of each document in bytes: " + str(dbStats['avgObjSize']) + '\n')
        # self.printStats(text = "Number of objects: " + str(dbStats['objects']))
        # self.printStats(text = "Number of collections: " + str(dbStats['collections']))
        # self.printStats(text = "")
        # collectionsList = self.mongo_db.collection_names()
        # self.printStats(text = "Collections: ")
        # for item in collectionsList:
            # if item.find('data') != -1:
                # try:
                    # self.printStats(text = "----")
                    # self.printStats(text = item)

                    # colStats = self.mongo_db.command("collstats", item)
                    # self.printStats(text = "Number of documents: " + str(colStats['count']))
                    # self.printStats(text = "Collection size in bytes: " + str(colStats['size']))
                    # if (colStats['count'] > 0):
                        # self.printStats(text = "Average object size in bytes: " + str(colStats['avgObjSize']))
                    # self.printStats(text = "")
                    # self.collectionAnalysis(collection = item)
                # except Exception as e:
                    # print 'Error:', e
                    # continue

        #return HttpResponseRedirect(self.url)
        return k


    def collectionAnalysis(self, collection=None):
        dbcollection = self.mongo_db[collection]
        docs = dbcollection.find({"neemi_user" : self.currentuser})

        data_types = set()
        count = {}

        if (collection == 'dropbox_data') or (collection == 'facebook_data') or (collection == 'gcal_data') or (collection == 'linked_in_data') or (collection == 'gmail_data') or (collection == 'foursquare_data'):
            for data in docs:
                if 'data_type' in data.keys():                
                    data_type = data['data_type']
                    count[data_type] = count.get(data_type, 0) + 1   
#                else:
#                    print data
        elif (collection == 'gcontacts_data'):
            for data in docs:
                if 'data_type' in data.keys():
                    data_type = data['data_type']
                    count[data_type] = count.get(data_type, 0) + 1
                    string = data['data'][1:len(data['data']) - 1] 
        elif (collection == 'gplus_data'):   
            for data in docs:
                if 'data_type' in data.keys():
                    data_type = data['data_type']
                    count[data_type] = count.get(data_type, 0) + 1
#                else:
#                    print data
        elif (collection == 'twitter_data'):
            friends = set()
            followers =set()
            for data in docs:
                if 'data_type' in data.keys():
                    #print data['data'][0][1]
                    #return
                    data_type = data['data_type']
                    if data_type == 'FRIEND':
                        friends.add(data['data']['screen_name'])
                    elif data_type == 'FOLLOWER':
                        followers.add(data['data']['screen_name'])
                    elif data_type == 'TIMELINE':
                        #print data['data'].keys()
                        pass
                    count[data_type] = count.get(data_type, 0) + 1
#                else:
#                    print data

        for x in count: 
            self.printStats(text = str(x) + ': ' + str(count[x]))

    def printStats(self, text=None):
        print text
        self.file.write(text + '\n')
        self.topk.append(text)									
									

     
class DBTopkFacebook_status(object):

    def __init__(self, request=None):
        self.url = '/get_topk/'
        self.mongo_db = get_db()
        self.file = open('topk.txt', 'a')
        self.topk = []

        print "mongoDB: ", self.mongo_db
        print "username: ", request.user.username

        cursor = self.mongo_db['user'].find({'username':request.user.username})

        self.currentuser = ''
        for data in cursor:
            if '_id' in data.keys():                
                self.currentuser = data['_id']


    def top_stats(self):
        print [self.mongo_db]
        pipeline =[ {'$match':{'data_type':'STATUS'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.updated_time", 'like_count':{'$sum':1}}},{'$sort':{'like_count':-1}},{'$limit':10},{'$project': {"_id":0, "updated_time":"$_id","like_count": 1}} ]
        facebook_data =self.mongo_db.facebook_data
        topStats=self.mongo_db.command('aggregate','facebook_data',pipeline=pipeline)
        # topStats=self.mongo_db.facebook_data.aggregate([ {'$match':{'data_type':'STATUS'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.updated_time", 'like_count':{'$sum':1}}},{'$project': {"_id":0, "updated_time":"$_id","like_count": 1}} ])
        # topStats = self.mongo_db.command("dbstats")
        print len(topStats.items())
        #print topStats['result'].items()
        x=topStats[u'result']
        k=[]
        i=0
        streetno = {}
        k.append([])
        k[0].append('Likes')
        k[0].append('Time')
        for d in x:
		if int(time.strftime("%H",time.strptime(d['updated_time'],'%Y-%m-%dT%H:%M:%S+0000'))) in streetno:
		 streetno[int(time.strftime("%H",time.strptime(d['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')))]=streetno[int(time.strftime("%H",time.strptime(d['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')))]+d[u'like_count']
		else :
		 streetno[int(time.strftime("%H",time.strptime(d['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')))]=d[u'like_count']
        #for post in iter(topStats):
         #print post
         # print 'prashant'
        self.printStats(text = str(topStats))
        # self.printStats(text = "Total size in bytes of the data held in this database: " + str(dbStats['dataSize']))
        # self.file.write("Average size of each document in bytes: " + str(dbStats['avgObjSize']) + '\n')
        # self.printStats(text = "Number of objects: " + str(dbStats['objects']))
        # self.printStats(text = "Number of collections: " + str(dbStats['collections']))
        # self.printStats(text = "")
        # collectionsList = self.mongo_db.collection_names()
        # self.printStats(text = "Collections: ")
        # for item in collectionsList:
            # if item.find('data') != -1:
                # try:
                    # self.printStats(text = "----")
                    # self.printStats(text = item)

                    # colStats = self.mongo_db.command("collstats", item)
                    # self.printStats(text = "Number of documents: " + str(colStats['count']))
                    # self.printStats(text = "Collection size in bytes: " + str(colStats['size']))
                    # if (colStats['count'] > 0):
                        # self.printStats(text = "Average object size in bytes: " + str(colStats['avgObjSize']))
                    # self.printStats(text = "")
                    # self.collectionAnalysis(collection = item)
                # except Exception as e:
                    # print 'Error:', e
                    # continue

        #return HttpResponseRedirect(self.url)
        return streetno
    def printStats(self, text=None):
        print text
        self.file.write(text + '\n')
        self.topk.append(text)


		
		
class DBTopkFacebook_links(object):

    def __init__(self, request=None):
        self.url = '/get_topk/'
        self.mongo_db = get_db()
        self.file = open('topk.txt', 'a')
        self.topk = []

        print "mongoDB: ", self.mongo_db
        print "username: ", request.user.username

        cursor = self.mongo_db['user'].find({'username':request.user.username})

        self.currentuser = ''
        for data in cursor:
            if '_id' in data.keys():                
                self.currentuser = data['_id']


    def top_stats(self):
        print [self.mongo_db]
        pipeline =[ {'$match':{'data_type':'LINK'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.created_time", 'like_count':{'$sum':1}}},{'$sort':{'like_count':-1}},{'$limit':10},{'$project': {"_id":0, "created_time":"$_id","like_count": 1}}]
        facebook_data =self.mongo_db.facebook_data
        topStats=self.mongo_db.command('aggregate','facebook_data',pipeline=pipeline)
        # topStats=self.mongo_db.facebook_data.aggregate([ {'$match':{'data_type':'STATUS'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.updated_time", 'like_count':{'$sum':1}}},{'$project': {"_id":0, "updated_time":"$_id","like_count": 1}} ])
        # topStats = self.mongo_db.command("dbstats")
        x=topStats[u'result']
        k=[]
        i=0
        streetno = {}
        k.append([])
        k[0].append('Likes')
        k[0].append('Time')
        for d in x:
		if int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))) in streetno:
		 streetno[int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000')))]=streetno[int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000')))]+d[u'like_count']
		else :
		 streetno[int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000')))]=d[u'like_count']
        print len(topStats.items())
        #print topStats['result'].items()
        x=topStats[u'result']
        k=[]
        i=0
        k.append([])
        k[0].append('Likes')
        k[0].append('Time')
        for d in x:
         k.append([])
         for j in xrange(1):
		 k[i].append((d[u'like_count']))
         k[i].append((time.strftime("%H:%M:%S",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))))
         i+=1
        #for post in iter(topStats):
         #print post
         # print 'prashant'
        self.printStats(text = str(topStats))
        # self.printStats(text = "Total size in bytes of the data held in this database: " + str(dbStats['dataSize']))
        # self.file.write("Average size of each document in bytes: " + str(dbStats['avgObjSize']) + '\n')
        # self.printStats(text = "Number of objects: " + str(dbStats['objects']))
        # self.printStats(text = "Number of collections: " + str(dbStats['collections']))
        # self.printStats(text = "")
        # collectionsList = self.mongo_db.collection_names()
        # self.printStats(text = "Collections: ")
        # for item in collectionsList:
            # if item.find('data') != -1:
                # try:
                    # self.printStats(text = "----")
                    # self.printStats(text = item)

                    # colStats = self.mongo_db.command("collstats", item)
                    # self.printStats(text = "Number of documents: " + str(colStats['count']))
                    # self.printStats(text = "Collection size in bytes: " + str(colStats['size']))
                    # if (colStats['count'] > 0):
                        # self.printStats(text = "Average object size in bytes: " + str(colStats['avgObjSize']))
                    # self.printStats(text = "")
                    # self.collectionAnalysis(collection = item)
                # except Exception as e:
                    # print 'Error:', e
                    # continue

        #return HttpResponseRedirect(self.url)
        return streetno
    def printStats(self, text=None):
        print text
        self.file.write(text + '\n')
        self.topk.append(text)


class DBTopkFacebook_albums(object):

    def __init__(self, request=None):
        self.url = '/get_topk/'
        self.mongo_db = get_db()
        self.file = open('topk.txt', 'a')
        self.topk = []

        print "mongoDB: ", self.mongo_db
        print "username: ", request.user.username

        cursor = self.mongo_db['user'].find({'username':request.user.username})

        self.currentuser = ''
        for data in cursor:
            if '_id' in data.keys():                
                self.currentuser = data['_id']


    def top_stats(self):
        print [self.mongo_db]
        pipeline =[ {'$match':{'data_type':'ALBUM'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.created_time", 'like_count':{'$sum':1}}},{'$sort':{'like_count':-1}},{'$limit':10},{'$project': {"_id":0, "created_time":"$_id","like_count": 1}}]
        facebook_data =self.mongo_db.facebook_data
        topStats=self.mongo_db.command('aggregate','facebook_data',pipeline=pipeline)
        # topStats=self.mongo_db.facebook_data.aggregate([ {'$match':{'data_type':'STATUS'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.updated_time", 'like_count':{'$sum':1}}},{'$project': {"_id":0, "updated_time":"$_id","like_count": 1}} ])
        # topStats = self.mongo_db.command("dbstats")
        print len(topStats.items())
        #print topStats['result'].items()
        x=topStats[u'result']
        k=[]
        i=0
        streetno = {}
        k.append([])
        k[0].append('Likes')
        k[0].append('Time')
        for d in x:
		if int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))) in streetno:
		 streetno[int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000')))]=streetno[int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000')))]+d[u'like_count']
		else :
		 streetno[int(time.strftime("%H",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000')))]=d[u'like_count']
        x=topStats[u'result']
        k=[]
        i=0
        k.append([])
        k[0].append('Likes')
        k[0].append('Time')
        for d in x:
         k.append([])
         for j in xrange(1):
		 k[i].append((d[u'like_count']))
         k[i].append((time.strftime("%H:%M:%S",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))))
         i+=1
        #for post in iter(topStats):
         #print post
         # print 'prashant'
        self.printStats(text = str(topStats))
        # self.printStats(text = "Total size in bytes of the data held in this database: " + str(dbStats['dataSize']))
        # self.file.write("Average size of each document in bytes: " + str(dbStats['avgObjSize']) + '\n')
        # self.printStats(text = "Number of objects: " + str(dbStats['objects']))
        # self.printStats(text = "Number of collections: " + str(dbStats['collections']))
        # self.printStats(text = "")
        # collectionsList = self.mongo_db.collection_names()
        # self.printStats(text = "Collections: ")
        # for item in collectionsList:
            # if item.find('data') != -1:
                # try:
                    # self.printStats(text = "----")
                    # self.printStats(text = item)

                    # colStats = self.mongo_db.command("collstats", item)
                    # self.printStats(text = "Number of documents: " + str(colStats['count']))
                    # self.printStats(text = "Collection size in bytes: " + str(colStats['size']))
                    # if (colStats['count'] > 0):
                        # self.printStats(text = "Average object size in bytes: " + str(colStats['avgObjSize']))
                    # self.printStats(text = "")
                    # self.collectionAnalysis(collection = item)
                # except Exception as e:
                    # print 'Error:', e
                    # continue

        #return HttpResponseRedirect(self.url)
        return streetno
    def printStats(self, text=None):
        print text
        self.file.write(text + '\n')
        self.topk.append(text)


class DBTopkTwitter_retweets(object):

    def __init__(self, request=None):
        self.url = '/get_topk/'
        self.mongo_db = get_db()
        self.file = open('topk.txt', 'a')
        self.topk = []

        print "mongoDB: ", self.mongo_db
        print "username: ", request.user.username

        cursor = self.mongo_db['user'].find({'username':request.user.username})

        self.currentuser = ''
        for data in cursor:
            if '_id' in data.keys():                
                self.currentuser = data['_id']
 
    def top_stats(self):
        print [self.mongo_db]
        #pipeline =[ {'$match':{'data_type':'ALBUM'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.created_time", 'like_count':{'$sum':1}}},{'$sort':{'like_count':-1}},{'$limit':10},{'$project': {"_id":0, "created_time":"$_id","like_count": 1}}]
        #facebook_data =self.mongo_db.facebook_data
        topStats=self.mongo_db.twitter_data.find({'data_type':'RETWEET'},{'_id':0, 'data.created_at':1,'data.retweet_count': 1}).sort([('data.retweet_count',-1)]).limit (10)
        q=topStats
        # topStats=self.mongo_db.facebook_data.aggregate([ {'$match':{'data_type':'STATUS'}} ,{ '$unwind': "$data.likes.data"},{ '$group': { '_id':"$data.updated_time", 'like_count':{'$sum':1}}},{'$project': {"_id":0, "updated_time":"$_id","like_count": 1}} ])
        # topStats = self.mongo_db.command("dbstats")
        #print topStats['result'].items()
        #x=topStats[u'result']
        #streetno = {}
        k=[]
        i=1
        streetno = {}
        #for d in topStats:
         #print d
		 #print d[u'data'].values()
		 #for x in d[u'data'].keys():
          #print	d[u'data'][x]
          #k.append(d[u'data'][x])
        
       #k.append([])
       #k[0].append('Retweets')
       #k[0].append('Time')
       #for d in topStats:
        for i in range(2,5):
		 if int(time.strftime("%H",time.strptime(q[i][u'data']['created_at'] ,'%a %b %y %H:%M:%S +0000 %Y'))) in streetno:
		  streetno[int(time.strftime("%H",time.strptime(q[i][u'data']['created_at'] ,'%a %b %y %H:%M:%S +0000 %Y')))]=streetno[int(time.strftime("%H",time.strptime(q[1][u'data']['created_at'] ,'%a %b %y %H:%M:%S +0000 %Y')))]+q[i][u'data']['retweet_count']
		 else :
		  streetno[int(time.strftime("%H",time.strptime(q[i][u'data']['created_at'] ,'%a %b %y %H:%M:%S +0000 %Y')))]=q[i][u'data']['retweet_count']
        #x=topStats[u'result']
        #k=[]
        #i=0
        #k.append([])
        #k[0].append('Likes')
        #k[0].append('Time')
        #for d in x:
         #k.append([])
         #for j in xrange(1):
		 #k[i].append((d[u'like_count']))
         #k[i].append((time.strftime("%H:%M:%S",time.strptime(d['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))))
         #i+=1
        #for post in iter(topStats):
         #print post
         # print 'prashant'
        #self.printStats(text = str(topStats))
        # self.printStats(text = "Total size in bytes of the data held in this database: " + str(dbStats['dataSize']))
        # self.file.write("Average size of each document in bytes: " + str(dbStats['avgObjSize']) + '\n')
        # self.printStats(text = "Number of objects: " + str(dbStats['objects']))
        # self.printStats(text = "Number of collections: " + str(dbStats['collections']))
        # self.printStats(text = "")
        # collectionsList = self.mongo_db.collection_names()
        # self.printStats(text = "Collections: ")
        # for item in collectionsList:
            # if item.find('data') != -1:
                # try:
                    # self.printStats(text = "----")
                    # self.printStats(text = item)

                    # colStats = self.mongo_db.command("collstats", item)
                    # self.printStats(text = "Number of documents: " + str(colStats['count']))
                    # self.printStats(text = "Collection size in bytes: " + str(colStats['size']))
                    # if (colStats['count'] > 0):
                        # self.printStats(text = "Average object size in bytes: " + str(colStats['avgObjSize']))
                    # self.printStats(text = "")
                    # self.collectionAnalysis(collection = item)
                # except Exception as e:
                    # print 'Error:', e
                    # continue

        #return HttpResponseRedirect(self.url)
        return streetno
    def printStats(self, text=None):
        print text
        self.file.write(text + '\n')
        self.topk.append(text)
