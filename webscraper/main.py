# https://www.carwale.com/used/cars-for-sale/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd

start_time = time.time()
#  FUNCTIONS

#to convert to csv
def to_csv(df):
    with open('cars_wale.csv','a',encoding='utf-8') as cw:
        df.to_csv(cw, sep=',', index=False, encoding='utf-8')


#close loc tab
def close_loc():
    time.sleep(5)
    try:
        loc_tab=driver.find_element(By.XPATH,"//*[@id='closeLocIcon']")
    except Exception:
        loc_tab=driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div[2]/div[1]/span")
    loc_tab.click()
    
    # try:
    #     loc_div=driver.find_element(By.CLASS_NAME,"globalLocBlackOut")
    # except:
    #     loc_div=driver.find_element(By.CLASS_NAME,"")
    # x_offset = 1 
    # y_offset = 1
    # action.move_to_element_with_offset(loc_div, x_offset, y_offset)
    # action.click()
    # action.perform() 

def scroll():

    # Scroll to load all items
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(20)  # Allow time for new items to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

def scrape():
    scroll()
    #results[0].click()
    driver.execute_script("window.scrollTo(0, 0);")
    results=driver.find_elements(By.CLASS_NAME, "spancarname.card-detail-block__title-text-with-year")#"used-search__car-media-container")#"card-detail-block")
    print(len(results))
    # ul=driver.find_element(By.ID,"listingsData")
    # results=ul.find_elements(By.CSS_SELECTOR,"li")
    #print(results)

    i=0
    data_list = []
    target_strings = ['Price', 'Kilometer', 'Transmission', 'Fuel type', 'No. of owners', 'Manufacturing year','Car Available at','Engine','Max Power (bhp@rpm)','Mileage (ARAI)','Seating Capacity']         


    for result in results:
        time.sleep(1)
        #driver.execute_script("arguments[0].scrollIntoView();", result)
        # x_offset = 1 
        # y_offset = 1
        result.click()
        time.sleep(0.5)
        #action.move_to_element_with_offset(result, x_offset, y_offset).click().perform()
        # result.click()
        driver.switch_to.window(driver.window_handles[1])
        driver.refresh()

        name=driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[1]/div[1]/h1').text
        #print(name)

        attr=driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div')
        attr_list=[]
        for a in attr:
            aa=a.text.split('\n')
            for aaa in aa:
                        attr_list.append(aaa)
        
        # appending engcc,power and seats
        eng_div=driver.find_element(By.ID,"specifications")
        arrows=driver.find_elements(By.CLASS_NAME,"o-cpnuEd.o-dsiSgT.o-bJvRsk.o-bUlUGg.o-fzoTnS.o-fzoTzs.o-fzpimR.o-fzoTpk.o-eemiLE.o-cpNAVm")
        capacity=arrows[2]
        capacity.click()
        attr_list2=[]
        attr_list2=eng_div.text.split("\n")
        attr_list.extend(attr_list2)

        # Initialize a dictionary to store the extracted data
        extracted_data = {}

        for item in target_strings:
                    if item in attr_list:
                        key=item
                        extracted_data[key]=attr_list[attr_list.index(item)+1]
                    else:
                        key=item
                        extracted_data[key]=""

        # seller comments
        try:
            seller_comments=driver.find_element(By.CLASS_NAME,"o-fznJzb.o-fznJPp.o-fznVqX.o-fznVsN.o-eNbQSA.o-ItVGT.o-bIMsfE.o-clpMoH.o-YCHtV.o-cpNAVm.o-bkmzIL.o-fyWCgU").text #"o-fznJzu.o-fznJPk")
        except Exception:
            seller_comments=""

        # dent report
        dent_text=" "

        try:     
            dent_div=driver.find_element(By.CLASS_NAME,"o-YCHtV.o-bIMsfE.o-ItVGT.o-eKWNKE.o-bCRRBE")#"o-bfyaNx.o-cpnuEd")
            max_dents=int(dent_div.find_elements(By.CSS_SELECTOR,"span span")[1].text.strip('/'))

            for dents in range(max_dents):
                dent_text += dent_div.find_element(By.CLASS_NAME,"o-fzptUA.o-eqqVmt.o-bkmzIL.o-eZTujG.o-fzptOP.o-bUVylL.o-cpnuEd").text
                dent_text+=", "
                dent_arrow=dent_div.find_element(By.CSS_SELECTOR,"svg")
                dent_arrow.click()
            seller_comments+=dent_text
        except Exception:
            seller_comments+=dent_text
        

        #closing tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


        dic={'Name': name,'Location':extracted_data['Car Available at'] ,'Year': extracted_data['Manufacturing year'],'Kilometers_Driven':extracted_data['Kilometer'],'Fuel_type':extracted_data['Fuel type'],'Transmission':extracted_data['Transmission'],'Owner_Type':extracted_data['No. of owners'],'Mileage':extracted_data['Mileage (ARAI)'],'Engine':extracted_data['Engine'],'Power':extracted_data['Max Power (bhp@rpm)'],'Seats':extracted_data['Seating Capacity'],'Price':extracted_data['Price'],'Seller Comments':seller_comments}
        #print(dic)
        data_list.append(dic)

        #print(data_list)
        print(i,data_list[i])
        i+=1
        # if i==15:
        #     break
        #driver.execute_script("arguments[0].scrollIntoView();", result)

    # Create a DataFrame
    df = pd.DataFrame(data_list)

    # convert to csv
    to_csv(df)

    # Print and/or save the DataFrame
    print(df)


#variables
# item=input("Enter car name : ")
# #item="Kia sonet"

#driver
driver = webdriver.Firefox()
action=ActionChains(driver)

#opening the website // "https://www.carwale.com/used/cars-for-sale/#sc=-1&so=-1&pn=1"
#link="https://www.carwale.com/used/cars-for-sale/#sc=-1&so=-1&car=10.160+10.152+10.308+10.179+10.347"
#link="https://www.carwale.com/used/cars-for-sale/#sc=-1&so=-1&car=10.423&pn=1" #brezza - 
# link="https://www.carwale.com/used/cars-for-sale/#sc=-1&so=-1&car=10.442&pn=1" #alto 
#link="https://www.carwale.com/used/cars-for-sale/#sc=-1&so=-1&car=12" #mitsubishi
link="https://www.carwale.com/used/cars-for-sale/#sc=-1&so=-1&car=16.386" #tata bolt
driver.get(link)
driver.refresh()
driver.implicitly_wait(10)


close_loc()

# try:
#     search_bar=driver.find_element(By.XPATH,"//*[@id='globalSearch']")
# except Exception:
#     search_bar=driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/header/div/div[2]/div[1]/div/div/div[1]/div/input")#ID,"globalSearch")
# search_bar.send_keys("Used ") 
# search_bar.send_keys(item) 
# search_bar.click()
# time.sleep(1)
# search_bar.send_keys(Keys.ENTER)
# time.sleep(1)
# close_loc()

# try:
scrape()
# except Exception:
#     print("NO RESULTS!!")

'''
scroll()
#results[0].click()
driver.execute_script("window.scrollTo(0, 0);")
results=driver.find_elements(By.CLASS_NAME, "card-detail-block__title")#"used-search__car-media-container")#"card-detail-block")
print(len(results))
results[len(results)-1].click()
'''

# Quit the WebDriver
time.sleep(5)

end_time = time.time()
# Calculate the time difference in seconds
elapsed_time = end_time - start_time

# Print the current time
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"Current time: {current_time}")

# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

driver.quit()
