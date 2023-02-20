from functools import total_ordering
from pymongo import MongoClient

def get_db_client(username, password):
    
    connection_string = 'mongodb+srv://{username}:{password}@menuitems.wdbco70.mongodb.net/?retryWrites=true&w=majority'.format(
        username=username
        , password=password
    )

    return MongoClient(connection_string)

@total_ordering
class Item:
    def __init__(self, id, value):
        self.id = id
        self.value = value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __repr__(self):
        return f'Item(\'{self.id}\', {self.value})'


    
#TODO : rewrite this with heapq

class TopN:
    def __init__(self, max_size):
        self.max_size = max_size
        self.elements = [None] * max_size
    
    def push(self, obj):

        insert = obj
        for i in range(self.max_size):
            if(self.elements[i] is None):
                self.elements[i] = insert
                break
            elif(self.elements[i] < insert):
                temp = self.elements[i]
                self.elements[i] = insert
                insert = temp
    
    def getTopN(self):
        return self.elements