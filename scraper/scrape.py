from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import os 
from pdfConverter import PDF


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
    def makeCSVFromResults(self,filename=os.path.join(os.path.dirname(os.getcwd()),'outputs','data.csv'))->bool:
        #creating a dataframe from dictionary
        prodDict={
            'titles':self.title,
            'prices':self.prices,
            'platforms':self.platforms,
            'image_url':self.images
        }
        df=pd.DataFrame(prodDict)
        try:
            df.to_csv('{}'.format(filename))
        except:
            return False
        
        return True


if __name__=='__main__':
    print('Welcome to steam scraper\n')
    print('#####################################')
    scraper=Scrape()
    url=input('Enter the steam url: ')
    if len(url)>=1:
        scraped=scraper.getNewAndTrending(url)
        if scraped:
            filePath=input('\nEnter the path to  the csv file you want to dump the data into.Default is outputs folder :  ')
            if len(filePath)>=1:
                print('\nDumping data into a csv file please wait...\n')
                dumped=scraper.makeCSVFromResults(filePath)
                
            else:
                print('\nInvalid filename.')
                print('\nUsing outputs directory\n')
                dumped=scraper.makeCSVFromResults()
            if dumped:
                    print('File genereated successfully....\n')
            else:
                    print('Sorry the file cannot be generated...\n')
                    exit()
        else:
            print('Couldn\'t scrape the webpage. Exiting.....')
            exit()


    else:
        print('No url entered. Exiting....')
        exit()
    print('#################################')
    choice=input('Do you want to create a pdf for the previous modified csv file ? [Y/N] ')
    #yes 
    if choice.lower()=='y':
        filePath=input('Enter the path to the csv file. By default outputs folder will be used.: ')
        if filePath:
            pdfHandler=PDF(filePath)
            
        else:
            pdfHandler=PDF()
        pdfHandler.readCSV()
        filename=input('Enter the name by which you want to save the pdf file : ')
        if filename:
            filePath=input('Enter the path where you want to save the pdf file : ')
            if filePath:
                #both filename and filepath specified
                pdfHandler.createPDF(filename=filename,filePath=filePath)
            else:
                #filename specified path not specified
                pdfHandler.createPDF(filename=filename)
                print('\n## File will is  outputted to the outputs directory\n')
        else:
            #name not specified
            pdfHandler.createPDF()
            print('\n## File will is outputted to the outputs directory\n')


        

    #no
    elif choice.lower()=='n' or not choice:
        pass
    print('\n###################################\n')
    print('Done\n')