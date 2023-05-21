from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from timeit import default_timer as timer
import pandas as pd
import time


def LCscrape(storeName, itemType, itemTypeLink):
    dataList = []
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(itemTypeLink)
    time.sleep(15)
    #click cookies button to stop obstruction
    cookiesButton = driver.find_element(by=By.XPATH, value='//*[@id="privacy-policy"]/div/div/button')
    cookiesButton.click()
    time.sleep(1)

    #click to load 48 more products
    start = timer()
    while True:
        end = timer()
        timeelapsed = end - start
        try:
            wait = WebDriverWait(driver, 100)
            waitelement1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class = "load-more-button"]')))
            click48 = driver.find_element(By.CSS_SELECTOR, '[class = "load-more-button"]')
            click48.click()
            if timeelapsed > 1800.0:
                break
        except Exception:
            print('all items are loaded')
            break
    time.sleep(10)

    #get the link for all items
    productGrid = driver.find_elements(by=By.XPATH, value='/html/body/div[2]/div/div[2]/main/div/div/div[5]/div/div[2]/div[4]/div/ul/*')
    wait = WebDriverWait(driver, 2)
    numOfP = 1
    for i in productGrid:
        try:
            waitelement2 = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/div/div[2]/main/div/div/div[5]/div/div[2]/div[4]/div/ul/li[{numOfP}]/div/div/div[3]/div[1]/h3/a')))
            productPackage = driver.find_element(by=By.XPATH, value=f'/html/body/div[2]/div/div[2]/main/div/div/div[5]/div/div[2]/div[4]/div/ul/li[{numOfP}]/div/div/div[3]/div[1]/h3/a')
            productName = driver.find_element(by=By.XPATH, value=f'/html/body/div[2]/div/div[2]/main/div/div/div[5]/div/div[2]/div[4]/div/ul/li[{numOfP}]/div/div/div[3]/div[1]/h3/a').text
            productLink = productPackage.get_attribute('href')
            csvData = {
                'Name' : productName,
                'Link' : productLink
                    }
            dataList.append(csvData)            
        except Exception:
            waitelement2 = wait.until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[2]/div/div[2]/main/div/div/div[5]/div/div[2]/div[4]/div/ul/li[{numOfP}]/div/div/div[3]/div[2]/h3/a')))
            productPackage = driver.find_element(by=By.XPATH, value=f'/html/body/div[2]/div/div[2]/main/div/div/div[5]/div/div[2]/div[4]/div/ul/li[{numOfP}]/div/div/div[3]/div[2]/h3/a')
            productName = driver.find_element(by=By.XPATH, value=f'/html/body/div[2]/div/div[2]/main/div/div/div[5]/div/div[2]/div[4]/div/ul/li[{numOfP}]/div/div/div[3]/div[2]/h3/a').text
            productLink = productPackage.get_attribute('href')
            csvData = {
                'Name' : productName,
                'Link' : productLink
                    }
            dataList.append(csvData)

        numOfP += 1

    CSV_PATH = f'{storeName}{itemType}.csv'
    data = pd.DataFrame(dataList)
    data.to_csv(CSV_PATH, index=False, encoding='utf-8')

    #driver.close()

#LCscrape('nofrills','Meats', 'https://www.nofrills.ca/food/meat/c/27998' )


#make a function that gets the storename, itemtype, and itemtypelink


def getallLCitems(nestedList):
    for i in nestedLinkStoreList:
        storeName = i[0]
        storeLink = i[1]

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.get(storeLink)
        time.sleep(5)
        #click cookies button to stop obstruction
        cookiesButton = driver.find_element(by=By.XPATH, value='//*[@id="privacy-policy"]/div/div/button')
        cookiesButton.click()
        time.sleep(1)

        zipperType = []
        zipperLink = []
        zippertypeLink = []
        allItemTypes = driver.find_elements(By.CSS_SELECTOR, '[class = "category-filter-item"]')
        for i in allItemTypes:
            itemType = i.text
            zipperType.append(itemType)

        allTypeLink = driver.find_elements(By.CSS_SELECTOR, '[class = "category-filter-item__link"]')
        for i in allTypeLink:
            typeLink = i.get_attribute('href')
            zipperLink.append(typeLink)

        for i in range(len(zipperType)):
            zippertypeLink.append(zipperType[i])
            zippertypeLink.append(zipperLink[i])

        driver.close()

        #take the elements from the zippertypelink and insert them into the LCscrape function to get all product data
        j = 0
        k = 0
        for i in range(len(zippertypeLink)//2):
            k = j + 1
            itemType = str(zippertypeLink[j])
            itemType.replace(' ','')
            itemTypeLink = str(zippertypeLink[k])
            j = k + 1
        

            #call the LCscrape function
            LCscrape(storeName, itemType, itemTypeLink)


nestedLinkStoreList = [['nofrills', 'https://www.nofrills.ca/food/c/27985'], ['superstore', 'https://www.realcanadiansuperstore.ca/food/c/27985'],['loblaws', 'https://www.loblaws.ca/food/c/27985']]
#getallLCitems(nestedLinkStoreList)

LCscrape('loblaws', 'Pantry', 'https://www.loblaws.ca/food/pantry/c/28006')
