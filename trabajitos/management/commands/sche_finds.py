# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from django.core.management.base import NoArgsCommand
from django.db.models import Q
from django.conf import settings

from random import sample

from trabajitos.apps.user.models import Search, Find, Job, Account
from trabajitos.apps.infojobs.infojobs import InfojobsSearch, InfoJobsJoin, InfoJobsLogin, InfojobsJob

class Command(NoArgsCommand):
    help = 'Trow all queries to join job\'s portal/s '
    
    def handle(self, *args, **options):
        searchs = Search.objects.all()

        for search in searchs:
            
            print search.words+"::"+search.provinces
            find = Find(search=search,total=0,efective=0)
            find.save()
            
            useragent = sample(settings.USER_AGENTS,1)[0]
            print useragent
            
            firefoxProfile = FirefoxProfile()
            firefoxProfile.set_preference("general.useragent.override", useragent)
            firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
            firefoxProfile.set_preference('permissions.default.image', 2)
            browser = webdriver.Firefox(firefoxProfile)
            
            
            print "Searching..."
            try:
                infojobs = InfojobsSearch(search.words,search.provinces.lower().split(','),browser)
            except Exception:
                print "Something was wrong..."
                try:
                    infojobs = InfojobsSearch(search.words,search.provinces.lower().split(','),browser)
                except Exception:
                    #This no matter, sometimes infojobs portal make stranges redirections, maybe anti scraping, I don't know
                    continue
                
            joblist = infojobs.find()
            afind = False
            pjoblist = []
            for i in joblist:
                print i.href
                if not Job.objects.filter(Q(user=search.user) & Q(url=i.href)):
                    afind = True
                    pjoblist.append(i)
            
            find.total = joblist.__len__()
            find.efective = 0;
            
            print pjoblist.__len__()
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
                            print "test::"+non
                            if non in i.href or non in i.title or i.company:
                                nexto = True
                        if nexto:
                            continue
                    print i.href
                    previous = Job.objects.filter(Q(user=search.user) & Q(url=i.href))
                
                    print previous
                    if not previous or previous.__len__() <=0 :
                        infocommit = InfoJobsJoin(i.href,browser) 
                        state = infocommit.commit()
                        job = Job(find=find,status=state,user=search.user,url=i.href,siteid=i.href,title=i.title,company=i.company,description=i.description)
                        job.save()
                        find.efective = find.efective +1;
                    
            find.save()
            
            browser.close()
