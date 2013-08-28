# -*- coding: utf-8 -*-

import smtplib

from trabajitos.apps.user.models import Alert, JobAlert

from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.db.models import Q

from random import sample

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from trabajitos.apps.infojobs.infojobs import InfojobsSearch, InfoJobsJoin, InfojobsJob

import logging

logger = logging.getLogger('schedule')

class Command(NoArgsCommand):
    help = 'Trow all alerts jobs portal/s '
    
    def handle(self, *args, **options):
        alerts = Alert.objects.all()
        
        for alert in alerts:
            logger.debug(alert.words+"::"+alert.provinces)
            
            useragent = sample(settings.USER_AGENTS,1)[0]
            logger.debug(useragent)
            
            firefoxProfile = FirefoxProfile()
            firefoxProfile.set_preference("general.useragent.override", useragent)
            firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
            firefoxProfile.set_preference('permissions.default.image', 2)

            browser = webdriver.Firefox(firefoxProfile)
            
            infojobs = InfojobsSearch(alert.words,alert.provinces.lower().split(','),browser)
            joblist = infojobs.find()
            
            jobalerts=[]
            for i in joblist:
                logger.debug(i.href)
                jobs=JobAlert.objects.filter(Q(user=alert.user) & Q(url=i.href))
                if jobs.__len__() == 0:
                    jobalerts.append(i)
            
	    logger.debug("Send alerts!")
            if jobalerts.__len__() > 0:
                body = ''
                for i in joblist:
                    jobalert = JobAlert(alert=alert,user=alert.user,url=i.href,siteid=i.href,title=i.title,company=i.company,description=i.description)
                    try:
                        jobalert.save()
                        body = body + i.title+" - "+i.company+"<br/>"+i.description+"<br/>"+i.href
                    except Exception:
                        logger.debug("Is present!"+i.href)
                #user = User.objects.get(id=alert.user)
                    
                if alert.user:
                    
                    sender = 'respira@gmail.com'
                    recipient = alert.user.email
                    subject = 'Alertas: '+alert.words+' en '+alert.provinces
                    
                    headers = ["from: " + sender,
                               "subject: " + subject,
                               "to: " + recipient,
                               "mime-version: 1.0",
                               "content-type: text/html"]
                    headers = "\r\n".join(headers)
                    
                    session = smtplib.SMTP('smtp.gmail.com', 587)
                    
                    session.ehlo()
                    session.starttls()
                    session.ehlo
                    session.login('mail@gmail.com', 'pass')
                
                    logger.debug("sendmail")
                    session.sendmail(sender.encode("utf-8"), recipient.encode("utf-8"), headers.encode("utf-8") + "\r\n\r\n" + body.encode("utf-8"))
                    session.quit()
            
            browser.close()
