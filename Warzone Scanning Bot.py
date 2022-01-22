# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 03:57:47 2021

@author: Marcos Maciel

Description: 
This is basically a bot created for Warzone that reads the screen and detects the people you kill/get killed by 
and it webscrapes their stats from cod.tracker.gg. This can be used to help you identify a cheater.
"""

import pyautogui
import time
import cv2
from pytesseract import *
from PIL import Image
#import cloudscraper
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(executable_path=r"C:/Users/.../chromedriver.exe")
from selenium.webdriver.common.by import By
import mss
import mss.tools

pytesseract.tesseract_cmd = r'C:\Users\...\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def webscrape(username):
    t = time.time()
    pcent = username.index('%')
    username = username[:pcent+1] + '23' + username[pcent+1:]
    print(username)
    
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome()
    driver.get(f'https://cod.tracker.gg/warzone/profile/atvi/{username}/overview')
    #print(driver.content)
    page_title = driver.find_elements(By.CLASS_NAME, 'lead')
    
    if not page_title or page_title[0] == "WARZONE STATS NOT FOUND":
        print("WARZONE STATS NOT FOUND - Private profile")
    
    else:
        search = driver.find_elements(By.CLASS_NAME, 'value')
        if len(search) > 4:
            print("Wins:", search[0].text)
            print("Win %:", search[1].text)
            print("Kills:", search[2].text)
            print("K/D:", search[3].text)
            print("Score/min:", search[4].text)
        else:
            print("Incorrect name or private profile")
    elapsed = time.time() - t
    print(elapsed, "Time to webscrape")
    
    #time.sleep(1)
    driver.close() 
    runCrappyCode()

def runCrappyCode():
        
    found = False
    time.sleep(1)
    while not found:
        #Marcos, you might have to compare to different examples to get more accuracy and make this headless
        t = time.time()
        coords = pyautogui.locateOnScreen('1ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))
        coords1 = pyautogui.locateOnScreen('2ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))
        coords2 = pyautogui.locateOnScreen('3ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))
        coords3 = pyautogui.locateOnScreen('6ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))

        
        elapsed = time.time() - t
        #print(elapsed)
        if coords or coords1 or coords2 or coords3:
            t = time.time()
            with mss.mss() as sct:
                # The screen part to capture
                region = {'top': 938, 'left': 696, 'width': 339, 'height': 35}
            
                # Grab the data
                img = sct.grab(region)
            
                # Save to the picture file
                mss.tools.to_png(img.rgb, img.size, output='screenshot2.png')
            
            #im2 = pyautogui.screenshot(region = (700, 937, 263, 33))
            elapsed = time.time() - t
            #print(elapsed)
            print('found something')
            #im2.save(r"screenshot2.png")
            
            img = cv2.imread('screenshot2.png')
            img = cv2.resize(img, dsize=(526, 66), interpolation=cv2.INTER_CUBIC)
            '''
            dsize = (526, 66)

            # resize image
            output = cv2.resize('screenshot2.png', dsize)
            cv2.imwrite('gray1.png',output)
            
            '''
            cv2.imwrite('screenshot2.png', img)
            #img = Image.open('screenshot2.png')
            result = pytesseract.image_to_string(img)
            result = result.rstrip()
            
            if result == '' or '#' not in result:
                print("No string found")
                runCrappyCode()
                
            if ']' in result:
                slicing = result.find(']')
                newResult = result[slicing+1:]
                newResult = newResult.replace('#', '%')
                print(newResult)
                
                webscrape(newResult)
                
            elif ']' not in result: 
                newResult = result.replace('#', '%')
                print(newResult)
                webscrape(newResult)
                
        else:
            #print('ImageNotFound exception')
            runCrappyCode()
        found = True

runCrappyCode()