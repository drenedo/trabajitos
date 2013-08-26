# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from django.core.management.base import NoArgsCommand
from django.db.models import Q
from django.conf import settings

from random import sample

from trabajitos.apps.user.models import Search, Find, Job, Account
from trabajitos.apps.infojobs.infojobs import InfojobsSearch, InfoJobsJoin, InfoJobsLogin, InfojobsJob

import logging

logger = logging.getLogger('schedule')

class Command(NoArgsCommand):
    help = 'Trow all queries to join job\'s portal/s '
    
    def handle(self, *args, **options):
        #searchs = Search.objects.all().filter(Q(user=2))
	searchs = Search.objects.all()

        for search in searchs:
            
            logger.debug(search.words+"::"+search.provinces)
            find = Find(search=search,total=0,efective=0)
            find.save()
            
            useragent = sample(settings.USER_AGENTS,1)[0]
            logger.debug(useragent)
            
            firefoxProfile = FirefoxProfile()
            firefoxProfile.set_preference("general.useragent.override", useragent)
            firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
            firefoxProfile.set_preference('permissions.default.image', 2)
            browser = webdriver.Firefox(firefoxProfile)
            browser.delete_all_cookies()
            
            
            logger.debug("Searching...")
            infojobs = InfojobsSearch(search.words,search.provinces.lower().split(','),browser)
                
            joblist = infojobs.find()
            if joblist.__len__() <=0 :
                old_find = Find.objects.all().filter(search_id=search).order_by('-date','-time')[1]
                if old_find and old_find.total>0:
                    browser.delete_all_cookies()
                    infojobs = InfojobsSearch(search.words,search.provinces.lower().split(','),browser)
                    joblist = infojobs.find()
            
            afind = False
            pjoblist = []
            for i in joblist:
                logger.debug(i.href)
                if not Job.objects.filter(Q(user=search.user) & Q(url=i.href)):
                    afind = True
                    pjoblist.append(i)
            
            find.total = joblist.__len__()
            find.efective = 0;
            
            logger.debug(pjoblist.__len__())
            if afind:
                account = Account.objects.filter(Q(user=search.user))[:1]
                login=''
                password=''
                if account and account.__len__()>0:
                    login = account[0].login
                    password = account[0].password
                else:
                    continue
                
                infologin = InfoJobsLogin(login,password,browser)
                browser = infologin.login()
            
                #TODO Aqui
                for i in pjoblist:
                    if search.non:
                        nexto = False
                        for non in search.non.split(','):
                            logger.debug("test::"+non)
                            if non in i.href or non in i.title or i.company:
                                nexto = True
                        if nexto:
                            continue
                    logger.debug(i.href)
                    previous = Job.objects.filter(Q(user=search.user) & Q(url=i.href))
                
                    logger.debug(previous)
                    if not previous or previous.__len__() <=0 :
                        infocommit = InfoJobsJoin(i.href,browser) 
                        state = infocommit.commit()
                        job = Job(find=find,status=state,user=search.user,url=i.href,siteid=i.href,title=i.title,company=i.company,description=i.description)
                        job.save()
                        find.efective = find.efective +1;
                    
            find.save()
            
            browser.close()
