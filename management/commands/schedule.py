# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from django.core.management.base import NoArgsCommand
from django.db.models import Q

from trabajitos.apps.user.models import Search, Find, Job
from trabajitos.apps.infojobs.infojobs import InfojobsSearch, InfoJobsJoin, InfoJobsLogin

class Command(NoArgsCommand):
    help = 'Trow all queries to job\'s portal/s '
    
    def handle(self, *args, **options):
        searchs = Search.objects.all()

        for search in searchs:
            print search.words+"::"+search.provinces
            find = Find(search=search,total=0,efective=0)
            find.save()
            
            firefoxProfile = FirefoxProfile()
            firefoxProfile.set_preference("general.useragent.override", "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us)")
            browser = webdriver.Firefox(firefoxProfile)
            
            
            infojobs = InfojobsSearch(search.words,search.provinces.lower().split(','),browser)
            joblist = infojobs.find()
            afind = False
            pjoblist = []
            for i in joblist:
                if not Job.objects.filter(Q(user=search.user) & Q(url=i)):
                    afind = True
                    pjoblist.append(i)
            
            find.total = joblist.__len__()
            find.efective = 0;
            
            print pjoblist.__len__()
            if afind:
                infologin = InfoJobsLogin("peybon79@gmail.com","javi652858710",browser)
                browser = infologin.login()
            
                for i in pjoblist:
                    for non in search.non.split(','):
                        print "test"+non
                        if "ong" in i:
                            continue
                    print i
                    previous = Job.objects.filter(Q(user=search.user) & Q(url=i))
                
                    print previous
                    if not previous or previous.__len__() <=0 :
                        infocommit = InfoJobsJoin(i,browser) 
                        state = infocommit.commit()
                        job = Job(find=find,status=state,user=search.user,url=i,siteid=i)
                        job.save()
                        find.efective = find.efective +1;
                    
            find.save()
            
            browser.close()
