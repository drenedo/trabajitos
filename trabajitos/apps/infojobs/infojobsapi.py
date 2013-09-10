from django.conf import settings

import logging

import urllib
import urllib2

import simplejson as json

logger = logging.getLogger('schedule')
TRIM_API_URL = 'https://api.infojobs.net/api'

class InfojobsSearchAPI:
    def __init__(self, key=None, provlist=None):
        self.key = key
        self.provlist = provlist

    def find(self):
        joblist = []
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
            url = url+'q'+self.key
	
	
        response = urllib2.urlopen(url)
        url = response.read().strip()
        objects = json.loads(url)

        logger.debug(objects['offers'].__len__())     
 
