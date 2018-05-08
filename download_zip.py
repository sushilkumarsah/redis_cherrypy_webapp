import os
import sys
import wget
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

def download(folder_location):
    try:
        os.system("mkdir -p " + folder_location + "old")
        os.system("mv " + folder_location + "*.ZIP " + folder_location + "old")
        os.system("mv " + folder_location + "*.CSV " + folder_location + "old")
    except  Exception as e:
        print "exception raised in os work"
        print str(e)
        sys.exit(1)
    
    geckodriver_path = folder_location + 'geckodriver'
    
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=opts, executable_path=geckodriver_path)

    browser.get("https://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx")
    link = ""
    iframe = browser.find_elements_by_tag_name('iframe')

    iframe2 = iframe[2]
    try:
        browser.switch_to_frame(iframe2)
        link = browser.find_element_by_partial_link_text("Equity - ").get_attribute('href')
    #    print "link = ", link
    except Exception as e:
        print "exception raised in iframe"
        print str(e)
        sys.exit(1)

    zip_name = wget.download(link, out=folder_location)
    #print "zip_name = ", zip_name

    browser.close()
    
    os.system("killall -9 firefox")
    os.system("killall -9 geckodriver")
    
    return zip_name
    
if __name__ == "__main__":
    download("/home/ubuntu/web_app/")