'''
    Python script to scrape the comments for competition entries.
    Personally, I would have specified that everyone made their
    guess in kg at the start of the comment, followed by say a
    period (.) or something. This would have made processing a lot
    easier and more efficient.

    Feel free to modify to suit your needs.

    Shane Frost
    20210212
'''

import time
import pandas as pd
import re
import csv
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

commentors=[]
data=[]

def BMP(s):
    # This will remove emojis (why do people insist?)
    return "".join((i if ord(i) < 10000 else '\ufffd' for i in s))

with Chrome(executable_path=r'C:\Program Files\chromedriver.exe') as driver:
    wait = WebDriverWait(driver,15)
    driver.get("https://www.youtube.com/watch?v=F4TLRzyUXjA")

    for item in range(30): # Scroll down 30 times. If there's more comments than that, increase this number
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(15)

    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        m = re.search(r"\d", BMP(comment.text)) # Search for the first digit in the string
        if m: #Only process if there's a digit in the comment.
            data.append(BMP(comment.text)[m.start():m.start()+20])
        
    for commentor in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#header-author"))): 
        commentors.append(BMP(commentor.text[:commentor.text.find('\n')]))

# Write the output to the shell.
for i in range(len(data)-1):
    print(commentors[i] + ' - ' + data[i])


# Write the output to a CSV file 
with open('C:\Python\Comments Scraped.csv', 'w', encoding="utf-8") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Name', 'Comment'])
    for i in range(len(data)-1):
        filewriter.writerow([commentors[i],data[i]])




    
