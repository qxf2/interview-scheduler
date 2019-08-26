"""
DriverFactory class
Note: Change this class as you add support for:
1. SauceLabs/BrowserStack
2. More browsers like Opera
"""
import dotenv,os,sys,requests,json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome import service
from selenium.webdriver.remote.webdriver import RemoteConnection
from conf import opera_browser_conf

class DriverFactory():
    
    def __init__(self,browser='ff',browser_version=None,os_name=None):
        "Constructor for the Driver factory"
        self.browser=browser
        self.browser_version=browser_version
        self.os_name=os_name

        
    def get_web_driver(self,remote_flag,os_name,os_version,browser,browser_version):
        "Return the appropriate driver"
        if (remote_flag.lower() == 'n'):
            web_driver = self.run_local(os_name,os_version,browser,browser_version)       
        else:
            print("DriverFactory does not know the browser: ",browser)
            web_driver = None

        return web_driver   
    

    

    def run_local(self,os_name,os_version,browser,browser_version):
        "Return the local driver"
        local_driver = None
        if browser.lower() == "ff" or browser.lower() == 'firefox':
            local_driver = webdriver.Firefox()    
        elif  browser.lower() == "ie":
            local_driver = webdriver.Ie()
        elif browser.lower() == "chrome":
            local_driver = webdriver.Chrome()
        elif browser.lower() == "opera":
            opera_options = None
            try:
                opera_browser_location = opera_browser_conf.location
                options = webdriver.ChromeOptions()
                options.binary_location = opera_browser_location # path to opera executable
                local_driver = webdriver.Opera(options=options)
                    
            except Exception as e:
                print("\nException when trying to get remote webdriver:%s"%sys.modules[__name__])
                print("Python says:%s"%str(e))
                if  'no Opera binary' in str(e):
                     print("SOLUTION: It looks like you are trying to use Opera Browser. Please update Opera Browser location under conf/opera_browser_conf.\n")
        elif browser.lower() == "safari":
            local_driver = webdriver.Safari()

        return local_driver


                

    def get_firefox_driver(self):
        "Return the Firefox driver"
        driver = webdriver.Firefox(firefox_profile=self.get_firefox_profile())

        return driver 


    def get_firefox_profile(self):
        "Return a firefox profile"

        return self.set_firefox_profile()

    
    def set_firefox_profile(self):
        "Setup firefox with the right preferences and return a profile"
        try:
            self.download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','downloads'))
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
        except Exception as e:
            print("Exception when trying to set directory structure")
            print(str(e))
            
        profile = webdriver.firefox.firefox_profile.FirefoxProfile()
        set_pref = profile.set_preference
        set_pref('browser.download.folderList', 2)
        set_pref('browser.download.dir', self.download_dir)
        set_pref('browser.download.useDownloadDir', True)
        set_pref('browser.helperApps.alwaysAsk.force', False)
        set_pref('browser.helperApps.neverAsk.openFile', 'text/csv,application/octet-stream,application/pdf')
        set_pref('browser.helperApps.neverAsk.saveToDisk', 'text/csv,application/vnd.ms-excel,application/pdf,application/csv,application/octet-stream')
        set_pref('plugin.disable_full_page_plugin_for_types', 'application/pdf')
        set_pref('pdfjs.disabled',True)

        return profile

