# -*- coding: utf-8 -*-

import smtplib

from trabajitos.apps.user.models import Account

from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.db.models import Q

from random import sample

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from trabajitos.apps.infojobs.infojobs import InfoJobsLogin, InfojobsUpdate

import logging

logger = logging.getLogger('schedule')

class Command(NoArgsCommand):
    help = 'Trow all alerts jobs portal/s '
    
    def handle(self, *args, **options):
	accounts = Account.objects.filter(Q(update=True))
        
        for account in accounts:
            useragent = sample(settings.USER_AGENTS,1)[0]
            logger.debug(useragent)
            
            firefoxProfile = FirefoxProfile()
            firefoxProfile.set_preference("general.useragent.override", useragent)
            firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
            firefoxProfile.set_preference('permissions.default.image', 2)

            browser = webdriver.Firefox(firefoxProfile)
            
            login = account.login
            password = account.password

            infologin = InfoJobsLogin(login,password,browser)
            browser = infologin.login()

            updater = InfojobsUpdate(browser)
            updater.update()
