from selenium import webdriver

# Set path to geckodriver.exe on your PC
driver = webdriver.Firefox(executable_path=r"/geckodriver/geckodriver.exe")
driver.get("http://www.google.com")