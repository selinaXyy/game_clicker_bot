from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

#get cookie
cookie = driver.find_element(By.ID, value="cookie")

start_time = time.time() #time now
buy_time = start_time + 5 #buy item every 5 sec
end_time = start_time + 5*60 #time after 5 min

while True:
    if time.time() > end_time:
        #get cps
        cookies_per_sec = driver.find_element(By.ID, value="cps").text
        print(cookies_per_sec)
        break

    cookie.click()
    
    if time.time() > buy_time:
        #get id
        #add current prices
        tools = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        id_list = []
        price_list = []

        for tool in tools:
            item = tool.text
            if item != "":
                item_info = item.split("\n")[0].split(" - ")
                item_id = f"buy{item_info[0]}"
                item_price = int(item_info[-1].replace(",", ""))
                id_list.append(item_id)
                price_list.append(item_price)

        #get my money
        my_money = driver.find_element(By.ID, value="money").text
        if "," in my_money:
            my_money = my_money.replace(",", "")
        my_money = int(my_money)

        #check the most expensive item I can buy
        affordable_item_indices = []
        for i in range(len(price_list)-1):
            if my_money >= price_list[i]:
                affordable_item_indices.append(i)

        affordable_item_id = id_list[affordable_item_indices[-1]]
        #click item
        driver.find_element(By.ID, value=affordable_item_id).click()
        
        buy_time = time.time() + 5

driver.close()