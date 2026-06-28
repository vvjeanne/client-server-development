# Ava Lindgren

from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse

class AnimalShelter(object):
    
    # property variables
    records_updated = 0 # keep record of records updated in operation
    records_matched = 0 # keep record of records matched in operation
    records_deleted = 0 # keep record of records deleted in operation

    # constructor to init the mongodb
    # should be singleton
    def __init__(self, _password, _username = 'aacuser'):
        
        # must be percent escaped as per pymongo documentation
        username = urllib.parse.quote_plus(_username)
        password = urllib.parse.quote_plus(_password)
        
        self.client = MongoClient('mongodb://%s:%s@localhost:27017/?authSource=aac' % (username, password))
        self.database = self.client['aac']
       
    # creating a record with createRecord method
    def createRecord(self, data):
        if data:
            _insertValid = self.database.animals.insert_one(data)
            # check status on inserted value 
            return True if _insertValid.acknowledged else False
        else:
            raise Exception("No document to save. Data is empty.")
    
    # get documents using guid    
    def getRecordId(self, postId):
        _data = self.database.animals.find_one({'_id': ObjectId(postId)})
        return _data
    
    # get records with criteria
    # all records are returned if criteria is None, default is None, and does not return the _id
    
    def getRecordCriteria(self, criteria = None):
        try: 
            if criteria:
                _data = list(self.database.animals.find(criteria, {'_id' : 0}))
            else:
                _data = list(self.database.animals.find({}, {'_id' : 0}))
            return _data
    
        except Exception as e:
            print(f"Read Error: {e}")
            return []
    
    # update a record
    def updateRecord(self, query, newValue):
        if not query:
            raise Exception("No search criteria is present.")
        if not newValue:
            raise Exception("No update value is present.")
        try:
            _updateValid = self.database.animals.update_many(query, {"$set": newValue})
            self.records_updated = _updateValid.modified_count
            self.records_matched = _updateValid.matched_count

            # return number of docs that were changed
            return _updateValid.modified_count
        
        except Exception as e:
            print(f"Update Error: {e}")
            return 0
    
    # delete a record
    def deleteRecord(self, query):
        if not query:
            raise Exception("No search criteria is present.")
        try:
            _deleteValid = self.database.animals.delete_many(query)
            self.records_deleted = _deleteValid.deleted_count
            
            # return number of docs delted
            return _deleteValid.deleted_count
        except Exception as e:
            print(f"Delete Error: {e}")
            return 0