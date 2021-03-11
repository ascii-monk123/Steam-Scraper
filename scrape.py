from bs4 import BeautifulSoup
import pandas as pd 
from selenium import webdriver


class Scrape:
    #constructor function
    def __init__(self):
        self.names=[]
        self.title=[]
        self.prices=[]
        self.platforms=[]
        self.images=[]

    '''
    Method : Scrape new and trending games from the web page 
    Format : 
    in: self,url:string =>from which url string to scrape
    out:BOOL->SUCCESS OR NOT
    '''
    def getNewAndTrending(self,url:str)->bool:
        #create a firefox session
        driver=webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get(url)

        #get html page from the given url
        webpage=BeautifulSoup(driver.page_source,'lxml')
        new_release=webpage.find(id="NewReleasesTable")

        for div in new_release.find_all('a',class_='tab_item'):
            #appending image
            image=div.find('div',class_='tab_item_cap').find('img',class_='tab_item_cap_img')['src']
            self.images.append(image)
            #appending discount price
            disc_price=div.find('div',class_='discount_block').find('div',class_='discount_prices').find('div',class_='discount_final_price').text
            self.prices.append(disc_price)
            #appending product title
            title=div.find('div',class_='tab_item_content').find('div',class_='tab_item_name').text
            self.title.append(title)
            #appending product platforms
            platforms=''
            for platformDiv in div.find('div',class_='tab_item_content').find('div',class_='tab_item_details').find('div',class_='tab_item_top_tags').find_all('span'):
                platforms+="{} ".format(platformDiv.text)
            self.platforms.append(platforms)
        #closing current firefox-session made by the selenium web-driver
        driver.quit()
        
        return True

    '''
    Method: Create a dataframe from the scraped results 
    Format:
    in:self,filename:string=>Name of the csv file to be made
    out:Bool->SUCCESS OR NOT

    '''
    def makeCSVFromResults(self,fileName:str)->bool:
        #creating a dataframe from dictionary
        prodDict={
            'titles':self.images,
            'prices':self.prices,
            'platforms':self.platforms,
            'image_url':self.images
        }
        df=pd.DataFrame(prodDict)
        try:
            df.to_csv('{}.csv'.format(filename))
        except:
            return False
        
        return True


if __name__=='__main__':
    print('Welcome to steam scraper\n')
    print('#####################################')
    scraper=Scrape()
    url=input('Enter the  url from which you want to scrape: ')
    if len(url)>=1:
        scraped=scraper.getNewAndTrending(url)
        if scraped:
            filename=input('\nEnter the name of the csv file you want to dump the data into: ')
            if len(filename)>=1:
                print('\nDumping data into a csv file please wait\n')
                dumped=scraper.makeCSVFromResults(filename)
                if dumped:
                    print('File genereated successfully\n')
                else:
                    print('Sorry the file cannot be generated\n')
                    exit()
            else:
                print('\nInvalid filename. Exiting......')
                exit()
        else:
            print('Couldn\'t scrape the webpage. Exiting.....')

    else:
        print('No url entered. Exiting....')
        exit()
