from json import JSONEncoder
from trabajitos.apps.user.models import Search, Find

from datetime import datetime

class ViewFind:
    def __init__(self, search=None, find=None):
        self.search=search
        self.find=find
    def toJSON(self, ):
        date = datetime.combine(self.find.date, self.find.time)
        dateString  = date.strftime("%H:%M:%S - %d-%m-%Y")
        
        return dict(id=self.find.id, provinces=self.search.provinces, words=self.search.words,
            date=dateString,total=self.find.total,efective=self.find.efective)
    
    

class MyEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'toJSON'):
            return obj.toJSON()
        
        return JSONEncoder.default(self, obj)