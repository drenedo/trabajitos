# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from utils import remove_accents

import time

class InfojobsJob:
    def __init__(self, href=None, title=None, company=None, description=None):
        self.title=title
        self.href=href
        self.company=company
        self.description=description

class InfojobsSearch:
    def __init__(self, key=None, provlist=None, browser=None):
        self.key = key
        self.provlist = provlist
        self.browser = browser
    
    def find(self):
        joblist = []
        
        if not self.browser:
            return joblist
        
	print "Get infojobs"    
        self.browser.get("http://www.infojobs.net")

	print "Sleep 2"
        time.sleep(2)

	print "Provincia"
        self.browser.find_element_by_id("of_provincia-button").click()
        provincias = self.browser.find_element_by_css_selector(".ui-multiselect-checkboxes.ui-helper-reset")

	print "Find provincias"
        if provincias:
            pros = provincias.find_elements_by_tag_name("li")
            for pro in pros:
                textPro = remove_accents(pro.text)
                if textPro in self.provlist:
		    print "Hago click:"+textPro
                    pro.find_element_by_tag_name("input").click()

	print "Palabra"
        palabra = self.browser.find_element_by_id("palabra")
        if palabra and palabra.is_displayed():
            palabra.click()
            palabra.send_keys(self.key)
            time.sleep(2)
            palabra.send_keys('\n')
        
	print "Sleep 4"
        time.sleep(4)
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
                            print "Something was wrong..."
                            pass
                        
                if not find:
                    end = True
        
        print "return jobs:"+str(joblist.__len__())
        return joblist
        
    def getData(self):
	print "Get data"
        joblist = []
        try:
            lis = self.browser.find_element_by_id("main-content")
        except NoSuchElementException:
            return joblist
	print "List"
        if lis:
            try:
                lu = lis.find_element_by_tag_name("ul")
                jobs = lu.find_elements_by_tag_name("li")
            except NoSuchElementException:
                return joblist
        
	    print "Jobs!"
            if jobs and jobs.__len__()>0:
		print "Job...."
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
                            print "t:"+ifj.title
                            print "h:"+ifj.href
                            print "c:"+ifj.company
                            print "d:"+ifj.description
                            print "appended::"+str(joblist.__len__())
                    except Exception:
                        #This no matter, sometimes infojobs portal make stranges redirections, maybe anti scraping, I don't know
                        print "Something was wrong..."
                        continue
        
        print "return part-jobs:"+str(joblist.__len__())
        return joblist
    
class InfoJobsLogin:
    def __init__(self, user=None, passwd=None, browser=None):
        self.user = user
        self.passwd = passwd
        self.browser = browser
    
    def login(self):
        self.browser.get("http://www.infojobs.net")
        time.sleep(1)
        print "Click:"
        #self.browser.find_element_by_id("login-access").click()
        self.browser.execute_script("javascript:slideLogin();")
        time.sleep(3)
        try:
        	self.browser.find_element_by_id("email").send_keys(self.user)
        	self.browser.find_element_by_id("e-password").send_keys(self.passwd)
        except ElementNotVisibleException:
                print "Exception:"
                self.browser.find_element_by_id("login-access").click()
                self.browser.find_element_by_id("email").send_keys(self.user)
                self.browser.find_element_by_id("e-password").send_keys(self.passwd)
        
        self.browser.find_element_by_id("idSubmitButton").click()
        
        return self.browser
    
    
class InfoJobsJoin:
    def __init__(self, url=None, browser=None):
        self.url=url
        self.browser = browser
    
    def commit(self):
        
        #self.browser.get("http://www.infojobs.net")
        #self.browser.find_element_by_id("login-access").click()
        #time.sleep(1)
        #self.browser.find_element_by_id("email").send_keys(self.user)
        #self.browser.find_element_by_id("e-password").send_keys(self.passwd)
        #self.browser.find_element_by_id("idSubmitButton").click()
        
        self.browser.get(self.url)
        time.sleep(12)
        try:
            candidate = self.browser.find_element_by_id("candidate_application")
        except NoSuchElementException:
            print "Error no Such element: candidate_application"
            return 1
        
        if candidate:
            print "Cancidate click"
            candidate.click()
        else:
            print "No Cancidate"
            return 1
        time.sleep(2)
        try:
            print "Inscribete click"
            self.browser.find_element_by_id("linkInscribete4").click() 
        except Exception:
            print "No Inscribete"
            return 2
              
        
        time.sleep(4)
        #fill the custom form
        myForm = self.browser.find_element_by_id("myForm")
        if myForm:
            myFormsOl = myForm.find_elements_by_tag_name("ol")
            if myFormsOl:
                for myFormOl in myFormsOl:
                    inputs = myFormOl.find_elements_by_tag_name("input")
                    textareas = myFormOl.find_elements_by_tag_name("textarea")
                    if inputs:
                        for inpu in inputs:
                            if inpu.is_displayed():
                                if inpu.get_attribute("id")=="opcionCarta_nocarta":
                                    inpu.click()
                                elif inpu.get_attribute("type")=="radio" and inpu.get_attribute("id")!="opcionCarta_incluir":
                                    inpu.click()
                                print inpu.get_attribute("outerHTML")
                    if textareas:
                        for ttarea in textareas:
                            if ttarea.is_displayed():
                                ttarea.send_keys("Error de codificaci&oacute;n con los datos del usuario, ha sido imposible recoger el formulario. Error code 0924521")
        
        #inscribe
        self.browser.find_element_by_id("botonEnviar").click()
        return 0


