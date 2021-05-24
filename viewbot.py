from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import numpy
import socket
import pylint
import os
import re
import time
from selenium.webdriver.support.select import Select
import threading
import random

PATH = "C:\Program Files (x86)\chromedriver.exe"
prefs = {"profile.managed_default_content_settings.images": 2}
iplist = []
options = webdriver.ChromeOptions()
driverarray = []
nbrofChrome = 30


def get_PROXY():    #RENVOI UNE LIST DE PROXY EN 8080
    #RECUPERE UNE LISTE DE PROXY
    PROXYPATH = "https://spys.one/free-proxy-list/FR/"
    proxyDriver = webdriver.Chrome(PATH)
    proxyDriver.get(PROXYPATH)
    time.sleep(3)
    #PREPARATION DE LA PAGE POUR 500 ELEMENT PORT 8080
    portelement = Select(proxyDriver.find_element_by_name("xf4"))
    portelement.select_by_visible_text("8080")
    time.sleep(3)
    showelement = Select(proxyDriver.find_element_by_name("xpp"))
    showelement.select_by_visible_text("500")
    time.sleep(3)
    proxyDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    ipelement = proxyDriver.find_elements_by_class_name("spy14")

    i = 0
    #ON NE RECUPERE QUE LES ADRESSE DANS IPLIST
    line = ""
    r = re.compile(r'[0-9]+(?:\.[0-9]+){3}:8080')
    for line in ipelement:
        if (r.match(line.text)):
            iplist.append(line.text)


    print("FOUND "+ str(len(iplist))+ " PROXY")
    proxyDriver.close()

def clean_PROXY():

    for line in iplist:
        ip = line.split(":")[0]
        print(ip)
        response = os.system("ping -n 1 " + ip)
        if response == 0:
            print(" STATUS = OK")
        else:
            iplist.remove(line)
            print(" STATUS = REJECTED")
    print("FOUND "+ str(len(iplist))+ " GOOD PROXY")


def go_VIDEO(crDriver):
    video = "https://www.youtube.com/watch?v=x9_KhDiD_oA"
 
    while True:       
        try:
            crDriver.get(video)
            break
        except Exception as e:
            driverarray.remove(crDriver)
            crDriver.close()
            print(e)

            random.seed(a=None, version=2)
            rd = random.randint(0,len(iplist)-1)

            options.add_experimental_option("prefs", prefs)
            options.add_argument('--proxy-server=%s' % iplist[rd])
            crDriver = webdriver.Chrome(PATH, chrome_options = options) #creation du driver avec proxy
            driverarray.append(crDriver)

    return    


get_PROXY()
clean_PROXY()



i = 0
j = 0
while (i<nbrofChrome):
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--proxy-server=%s' % iplist[j])
    driver = webdriver.Chrome(PATH, chrome_options = options) #creation du driver avec proxy
    driverarray.append(driver)
    j = j+1
    if (j > len(iplist)):
        j=0
    i = i+1


time.sleep(1)


threeadlist = []

for crDriver in driverarray:
   crThread = threading.Thread(target=go_VIDEO, args=[crDriver])
   crThread.start()
   threeadlist.append(crThread)

    
time.sleep(100)