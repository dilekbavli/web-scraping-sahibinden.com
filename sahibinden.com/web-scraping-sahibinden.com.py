import copy
import json
import time 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
# !pip install selenium
# !pip install webdriver-manager


class Automobile: 

    
    def __init__(self):
        self.model= []
        self.yil = []
        self.km = []
        self.renk = []
        self.fiyat = []
        self.tarih = []
        self.sehir = []
        self.jsonObj = []   


    s=Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s)
    browser.get("https://www.sahibinden.com/")
    browser.maximize_window()


          
    def findCategory(self, categoryName, subCategoryName):
        try:         
            self.start = time.time()
            self.categoryName = categoryName
            self.subCategoryName = subCategoryName
            categoryList = self.browser.find_element(By.CLASS_NAME, "category-3517")        
            categoryUL = copy.copy(categoryList.find_element(By.TAG_NAME, "ul"))
            categoryLI = copy.copy(categoryUL.find_elements(By.TAG_NAME, "li"))
        
            for row in categoryLI:
                aTag = copy.copy(row.find_element(By.TAG_NAME, "a"))
                title = aTag.get_attribute("title")
                if title == self.categoryName:
                    href = aTag.get_attribute("href")
                    self.browser.get(href)
                    self.saveSuccessLog(categoryName + " category found.")
                    self.findSubCategory(self.subCategoryName)
                    break
        except Exception as e:
            self.saveErrorLog(categoryName + "An error occurred while finding the category." + " && " + str(e))

                
    def findSubCategory(self, subCategoryName):
        try:
            self.subCategoryName = subCategoryName
            subCategoryList = self.browser.find_element(By.CLASS_NAME, "categoryList")
            subcategoryLI = copy.copy(subCategoryList.find_elements(By.TAG_NAME, "li"))
            _counter = 0
            
            for row in subcategoryLI:
                aTag = copy.copy(row.find_element(By.TAG_NAME, "a"))
                title = aTag.get_attribute("title")
                if title == self.subCategoryName:
                    href = aTag.get_attribute("href")
                    self.browser.get(href)
                    self.saveSuccessLog(subCategoryName + " subcategory found.")
                    self.pageCount = self.checkPageCount()
                    if(self.pageCount == 0):
                        _counter = self.findCarDesc(_counter, subCategoryName)
                        break
                    else:
                        
                        self.pageCountList = self.browser.find_element(By.CLASS_NAME, "pageNaviButtons") 
                        self.pageList = copy.copy(self.pageCountList.find_elements(By.TAG_NAME, "li"))
                        aTag = copy.copy(self.pageList[1].find_element(By.TAG_NAME, "a"))
                        href = aTag.get_attribute("href").replace("20", "")
                        for i in range(0, self.pageCount):                  
                            _counter = self.findCarDesc(_counter, subCategoryName)
                            self.browser.get(href + str(_counter))
                    break      
                                                                       
            self.saveSuccessLog(str(_counter) + " vehicles found.")        
            self.saveSuccessLog("Writing to file started.")
            with open('web_scraping.json', 'w', encoding='utf-8') as f:
                json.dump((self.jsonObj), f, ensure_ascii=False, indent=2)
            self.saveSuccessLog("Write to file completed.")
            runTime = time.time() - self.start
            self.saveSuccessLog("All transactions completed successfully. The passing time : " + str(runTime))

        except Exception as e:
            self.saveErrorLog(subCategoryName + " An error occurred while finding the subcategory." + " && " + str(e))
                    
     
    def checkPageCount(self):        
        try:   
            self.pageCount = 0
            self.pageCountList = self.browser.find_element(By.CLASS_NAME, "pageNaviButtons") 
            self.pageList = copy.copy(self.pageCountList.find_elements(By.TAG_NAME, "li"))
            for row in self.pageList:
                try:
                    aTagText = row.find_element(By.TAG_NAME, "a").text
                    if(aTagText != "Sonraki"):
                        self.pageCount = int(aTagText)
                except Exception as e:
                    self.saveErrorLog("An error occurred while retrieving the page count." + " && " + str(e))
                
            return self.pageCount
        except:
            return 0
        
        
        
            
    def findCarDesc(self, counter, subCategoryName):
        try:     
            carBodyElement = self.browser.find_element(By.CLASS_NAME, "searchResultsRowClass")
            carList = copy.copy(carBodyElement.find_elements(By.TAG_NAME, "tr"))
            for row in carList:
                obj = {}
                tdList = copy.copy(row.find_elements(By.TAG_NAME, "td"))
                if len(tdList) == 10:
                    self.model = tdList[1].text
                    self.yil = tdList[3].text
                    self.km = tdList[4].text
                    self.renk = tdList[5].text
                    self.fiyat = copy.copy(tdList[6].find_element(By.TAG_NAME, "div")).text
                    tarihElement = copy.copy(tdList[7].find_elements(By.TAG_NAME, "span"))
                    self.tarih = ""
                    for tarihRow in tarihElement:
                        self.tarih = self.tarih + tarihRow.text + " "
                    self.sehir = tdList[8].text
                
                    obj["marka"] = subCategoryName + " " + self.model
                    obj["model"] = self.model
                    obj["yil"] = self.yil
                    obj["km"] = self.km
                    obj["renk"] = self.renk
                    obj["fiyat"] = self.fiyat
                    obj["tarih"] = self.tarih
                    obj["sehir"] = self.sehir.replace("\n", " ")
                    counter = counter + 1
                    self.jsonObj.append(copy.copy(obj))
                elif len(tdList) == 11:
                    self.seri = tdList[1].text
                    self.model = tdList[2].text
                    self.yil = tdList[4].text
                    self.km = tdList[5].text
                    self.renk = tdList[6].text
                    self.fiyat = copy.copy(tdList[7].find_element(By.TAG_NAME, "div")).text
                    tarihElement = copy.copy(tdList[8].find_elements(By.TAG_NAME, "span"))
                    self.tarih = ""
                    for tarihRow in tarihElement:
                        self.tarih = self.tarih + tarihRow.text + " "
                    self.sehir = tdList[9].text
                
                    obj["marka"] = subCategoryName + " " + self.seri
                    obj["seri"] = self.seri
                    obj["model"] = self.model
                    obj["yil"] = self.yil
                    obj["km"] = self.km
                    obj["renk"] = self.renk         
                    obj["fiyat"] = self.fiyat
                    obj["tarih"] = self.tarih
                    obj["sehir"] = self.sehir.replace("\n", " ")
                    counter = counter + 1

                    self.jsonObj.append(copy.copy(obj))
            return counter
        except Exception as e:
            self.saveErrorLog("An error occurred while retrieving vehicle information." + " && " + str(e))


    def saveSuccessLog(self, message):
        try:
            
            f = open("successLog.txt", "a")
            messageFormat = "{0} -- {1}\n"
            f.write(messageFormat.format(datetime.now().strftime("%d.%m.%Y %H:%M"), message))
            f.close()
            
        except Exception as e:
              print(str(e))
        
            
    def saveErrorLog(self, message):
        try:
                    
            f = open("errorLog.txt", "a")
            messageFormat = "{0} -- {1}\n"
            f.write(messageFormat.format(datetime.now().strftime("%d.%m.%Y %H:%M"), message))
            f.close()
                    
        except Exception as e:
            print(str(e))
   
    
automobile = Automobile()
automobile.findCategory("Otomobil", "Aion")



# if __name__ == '__main__':
#       automobile = Automobile()
#       parser=argparse.ArgumentParser()
#       parser.add_argument('--cat_name', type = str, required = True, help = "enter cat name")
#       parser.add_argument('--car_name', type = str, required = True, help = "enter car name")
#       args=parser.parse_args()

      
#       automobile.findCategory(args.cat_name, args.car_name)
                           








               
     

    
  
    



    




















    
  

                           








               
     

    
  
    



    




















    
  
    


    
      




