from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import traceback
import time
import re

def scrape(driver):
    balance = 1050.88
    with open('data.csv', 'r') as f:
        last_line = f.readlines()[-1]
        csv_index = int(re.search(r'\d+', last_line).group()) + 1
        # csv_index = 0

    try:
        driver.get("https://eacct-psu-sp.transactcampus.com/PSU/AccountTransaction.aspx")
        continue_button = driver.find_element(By.ID, "MainContent_ContinueButton")
        continue_button.click()

        try:
            element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ctl00_MainContent_ResultRadGrid_ctl00"))
            )
        except Exception as e:
            print(e)

        next_page_button = driver.find_element_by_xpath("//div[@class='rgWrap rgNumPart']/a[" + str(5) + "]")
        next_page_button.click()
        time.sleep(8)

        # iterate through pages
        for n in range(5,0, -1):
            # check for table
            try:
                element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "ctl00_MainContent_ResultRadGrid_ctl00"))
                )
            except Exception as e:
                print(e)

            # iterate through table
            for i in range(15, 0, -1):
                try:
                    date = driver.find_element_by_xpath("//table[@id='ctl00_MainContent_ResultRadGrid_ctl00']/tbody/tr[" \
                    + str(i) + "]/td[1]").text
                except:
                    continue
                # if non-standard transaction
                if "eLIVING Transactions" in driver.find_element_by_xpath("//table[@id='ctl00_MainContent_ResultRadGrid_ctl00']/tbody/tr[" \
                    + str(i) + "]/td[4]").text: continue
                date = driver.find_element_by_xpath("//table[@id='ctl00_MainContent_ResultRadGrid_ctl00']/tbody/tr[" \
                    + str(i) + "]/td[1]").text
                date  = int(time.mktime(datetime.strptime(date, "%m/%d/%Y %I:%M %p").timetuple()))
                amount = re.findall("\d+\.\d+", driver.find_element_by_xpath("//table[@id='ctl00_MainContent_ResultRadGrid_ctl00']/tbody/tr[" \
                    + str(i) + "]/td[6]").text)

                balance -= float(amount[0])
                
                # print(str(date) + "\t" + str(balance))
                # print(str(csv_index) + "," + str(date) + "," + str(round(balance, 2)))
                with open('data.csv', 'a') as the_file:
                    the_file.write("\n" + str(csv_index) + "," + str(date) + "," + str(round(balance, 2)))

                csv_index += 1
            
            # click next page button
            if n  > 1:
                next_page_button = driver.find_element_by_xpath("//div[@class='rgWrap rgNumPart']/a[" + str(int(n-1)) + "]")
                next_page_button.click()
                print("clicking page " + str(n-1))
                time.sleep(8)
        
    except Exception as e:
        print(traceback.format_exc())



