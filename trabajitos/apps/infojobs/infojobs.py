# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from utils import remove_accents

import time
import logging

logger = logging.getLogger('schedule')

class InfojobsJob:
    def __init__(self, href=None, title=None, company=None, description=None):
        self.title=title
        self.href=href
        self.company=company
        self.description=description

class InfojobsUpdate:
    def __init__(self, browser=None):
        self.browser = browser

    def update(self):
        self.browser.execute_script("javascript:actualizarFechaCVThickBox();")

class InfojobsSearch:
    def __init__(self, key=None, provlist=None, browser=None):
        self.key = key
        self.provlist = provlist
        self.browser = browser
    
    def find(self):
        joblist = []
        
        if not self.browser:
            return joblist
        
	    logger.debug("Get infojobs")
        self.browser.get("http://www.infojobs.net")

        logger.debug("Sleep 2")
        time.sleep(2)

        logger.debug("Provincia")
        self.browser.find_element_by_id("of_provincia-button").click()
        provincias = self.browser.find_element_by_css_selector(".ui-multiselect-checkboxes.ui-helper-reset")

        logger.debug("Find provincias")
        if provincias:
            pros = provincias.find_elements_by_tag_name("li")
            for pro in pros:
                textPro = remove_accents(pro.text)
                if textPro in self.provlist:
		    logger.debug("Hago click:"+textPro)
                    pro.find_element_by_tag_name("input").click()

        logger.debug("Palabra")
        palabra = self.browser.find_element_by_id("palabra")
        if palabra and palabra.is_displayed():
            palabra.click()
            palabra.send_keys(self.key)
            time.sleep(2)
            palabra.send_keys('\n')
        
        logger.debug("Sleep 4")
        time.sleep(4)
        logger.debug("URL:"+self.browser.current_url)
        joblist = self.getData()
        time.sleep(2)
    
        
        
        end = False
        page = 1
        while not end:
            try:
                pagination = self.browser.find_element_by_id("pagination")
            except NoSuchElementException:
                break
            
            if pagination:
                lis = pagination.find_elements_by_tag_name("li")
                find = False
                if lis:
                    for li in lis:
                        try:
                            href = li.find_elements_by_tag_name("a")
                            if href.__len__()>0:
                                try:
                                    pag = int(href[0].text)
                                except ValueError:
                                    pag = -1
                                if pag and pag-1 == page:
                                    page = int(href[0].text)
                                    find = True
                                    href[0].click
                                    self.browser.execute_script(href[0].get_attribute("href"))
                                    time.sleep(8)
                                    joblist.extend(self.getData())
                                    break
                        except Exception:
                            logger.debug("Something was wrong...")
                            pass
                        
                if not find:
                    end = True
       
        logger.debug("URL:"+self.browser.current_url)
        logger.debug("return jobs:"+str(joblist.__len__()))
        return joblist
        
    def getData(self):
        logger.debug("Get data")
        joblist = []
        try:
            lis = self.browser.find_element_by_id("main-content")
        except NoSuchElementException:
            return joblist

        logger.debug("List")
        if lis:
            try:
                lu = lis.find_element_by_tag_name("ul")
                jobs = lu.find_elements_by_tag_name("li")
            except NoSuchElementException:
                return joblist
        
            logger.debug("Jobs!")
            if jobs and jobs.__len__()>0:
                logger.debug("Job....")
                for job in jobs:
                    try:
                        divs = job.find_elements_by_tag_name("div")
                        href=None
                        title=None
                        company=None
                        description=None
                        for div in divs:
                            classname = div.get_attribute("class")
                            if classname == 'description':
                                title = div.find_element_by_tag_name("h2").text
                                href = div.find_element_by_tag_name("a").get_attribute("href")
                                company = div.find_element_by_tag_name("h3").text
                            elif classname == 'details':
                                description=div.find_element_by_tag_name("p").text
                        
                        ifj = InfojobsJob(href,title,company,description)
                        if(ifj.href!=None):
                            joblist.append(ifj)
                            logger.debug("t:"+ifj.title)
                            logger.debug( "h:"+ifj.href)
                            logger.debug( "c:"+ifj.company)
                            logger.debug( "d:"+ifj.description)
                            logger.debug( "appended::"+str(joblist.__len__()))
                    except Exception:
                        #This no matter, sometimes infojobs portal make stranges redirections, maybe anti scraping, I don't know
                        logger.debug("Something was wrong...")
                        continue
        
        logger.debug( "return part-jobs:"+str(joblist.__len__()))
        return joblist
    
class InfoJobsLogin:
    def __init__(self, user=None, passwd=None, browser=None):
        self.user = user
        self.passwd = passwd
        self.browser = browser
    
    def login(self):
        self.browser.get("http://www.infojobs.net")
        time.sleep(1)
        logger.debug("Click:")
        #self.browser.find_element_by_id("login-access").click()
        self.browser.execute_script("javascript:slideLogin();")
        time.sleep(3)
        try:
        	self.browser.find_element_by_id("email").send_keys(self.user)
        	self.browser.find_element_by_id("e-password").send_keys(self.passwd)
        except ElementNotVisibleException:
                logger.debug("Exception:")
                self.browser.find_element_by_id("login-access").click()
                self.browser.find_element_by_id("email").send_keys(self.user)
                self.browser.find_element_by_id("e-password").send_keys(self.passwd)
        
        self.browser.find_element_by_id("idSubmitButton").click()
       
	logger.debug("Logued")
	time.sleep(10)
	 
        return self.browser
    
    
class InfoJobsJoin:
    def __init__(self, url=None, browser=None):
        self.url=url
        self.browser = browser
    
    def commit(self):
        
        self.browser.get(self.url)
        time.sleep(14)
        try:
            candidate = self.browser.find_element_by_id("candidate_application")
        except NoSuchElementException:

	    time.sleep(6)
        logger.debug("Wait more")

        try:
            candidate = self.browser.find_element_by_id("candidate_application")
        except NoSuchElementException:
		#print "---------------------------------"
		#print self.browser.page_source
		#print "---------------------------------"
            logger.debug("Error no Such element: candidate_application at "+self.browser.current_url)
            return 1
        
        if candidate:
            logger.debug("Cancidate click")
            candidate.click()
        else:
            logger.debug("No Cancidate")
            return 1
        time.sleep(12)
        try:
            logger.debug("Inscribete click")
            self.browser.find_element_by_id("linkInscribete4").click() 
        except Exception:
            logger.debug("No Inscribete")
            return 2
              
        
        time.sleep(12)
        #fill the custom form
        myForm = self.browser.find_element_by_id("myForm")
        if myForm:
            myFormsOl = myForm.find_elements_by_tag_name("ol")
            if myFormsOl:
                for myFormOl in myFormsOl:
                    logger.debug("url:"+self.browser.current_url)
                    logger.debug("Find inputs")
                    inputs = myFormOl.find_elements_by_tag_name("input")
                    textareas = myFormOl.find_elements_by_tag_name("textarea")
                    if inputs:
                        logger.debug("Imputs find")
                        for inpu in inputs:
                            if inpu.is_displayed():
                                if inpu.get_attribute("id")=="opcionCarta_nocarta":
                                    inpu.click()
                                elif inpu.get_attribute("type")=="radio" and inpu.get_attribute("id")!="opcionCarta_incluir":
                                    inpu.click()
                                logger.debug("Selected:"+str(inpu.is_selected()))
                    if textareas:
                        for ttarea in textareas:
                            if ttarea.is_displayed():
                                logger.debug("Find textareas")
                                ttarea.send_keys("Error de codificaci&oacute;n con los datos del usuario, ha sido imposible recoger el formulario. Error code 0924521")
        
        #inscribe
        logger.debug("Final click")
        self.browser.find_element_by_id("botonEnviar").click()
        return 0


