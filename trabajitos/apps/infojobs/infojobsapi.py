from django.conf import settings

import logging
import urllib
import urllib2

from infojobs import InfojobsJob
import simplejson as json

logger = logging.getLogger('schedule')
TRIM_API_URL = 'https://api.infojobs.net/api'

class InfojobsSearchAPI:
    def __init__(self, key=None, provlist=None):
        self.key = key
        self.provlist = provlist
        self.petition = 1
        self.total = 1

    def find(self):
        joblist = []
	joblist = self.getPetition(self.petition)

        while self.petition > 1 and self.total > 1 and self.petition <= self.total:
            joblist.extend(self.getPetition(self.petition))
            
            

    def getPetition(self,num):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, TRIM_API_URL, settings.INFOJOBSID, settings.INFOJOBSCR)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        url = TRIM_API_URL+'/1/offer?'
        if self.provlist:
            for pro in self.provlist:
                url = url+'province='+pro+'&'

        if self.key:
            url = url+'q='+self.key


        response = urllib2.urlopen(url)
        content = response.read().strip()
        objects = json.loads(content)

        logger.debug("Load::"+url)
        logger.debug(objects['offers'].__len__())

	self.petition = self.petition + 1
	self.total = objects['totalPages']

        return self.getObjects(objects['offers'])

    def getObjects(self,objects):
        joblist=[]
        if objects:
            for object in objects:
                ifj = InfojobsJob(object['link'],object['title'],object['author']['name'],object['study']['value']+' '+object['requirementMin'])
                logger.debug("Link::"+ifj.title)
                logger.debug("Load::"+ifj.href)
                logger.debug("Load::"+ifj.company)
                logger.debug("Load::"+ifj.description)
                if(ifj.href!=None):
                    joblist.append(ifj)
        return joblist
