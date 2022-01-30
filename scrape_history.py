from importlib import import_module, reload
from pathlib import Path
from selenium import webdriver

scrape_testing = import_module("scrape_testing")

options = webdriver.ChromeOptions() 
user_data_dir = Path("{}/driver/User Data".format("/Users/ethanbarclay/Library/Application Support/Google/Chrome"))
options.add_argument("--user-data-dir={}".format(user_data_dir))
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://eacct-psu-sp.transactcampus.com/PSU/AccountTransaction.aspx")

while(True):
    input("Press enter to run test: ")
    reload(scrape_testing)
    scrape_testing.scrape(driver)