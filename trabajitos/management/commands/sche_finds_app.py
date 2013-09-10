# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

import logging

from trabajitos.apps.user.models import Search
from trabajitos.apps.infojobs.infojobsapi import InfojobsSearchAPI

logger = logging.getLogger('schedule')

class Command(NoArgsCommand):
    help = 'Trow all alerts jobs portal/s '

    def handle(self, *args, **options):
        logger.debug("SearchAPI")
        searchs = Search.objects.all()
        
        for search in searchs:
            logger.debug("SearchAPI::"+search.words+"::"+search.provinces)
            infojobs = InfojobsSearchAPI(search.words,search.provinces.lower().split(','))
            infojobs = infojobs.find()
