from fpdf import FPDF
import pandas as pd
import numpy as np
import tempfile
import urllib.request as req
import os

#main runner class
class PDF:
    #constructor will take a filename as an argument
    def __init__(self,file=os.path.join(os.path.dirname(os.getcwd()),'outputs','data.csv')):
        self.file=file
    #read the required csv file
    def readCSV(self):
        try:
            self.df=pd.read_csv('{}'.format(self.file))
            self.items=[row for row in self.df[['image_url','prices','titles','platforms']].to_numpy()]
            
        except:
            print('Couldnt read the required csv file/invalid csv format')
            exit()
    #create the pdf file
    def createPDF(self,filename="data",filePath=os.path.join(os.path.dirname(os.getcwd()),'outputs')):
        pdf=FPDF()
        #create new pdf page
        pdf.add_page()

        #set font
        pdf.set_font('Times',size=40,style='B')

        #header cell
        pdf.cell(200,40,txt="Steam New Games",align='C',ln=2)

        pdf.set_font('Times',size=26,style='B')

        pdf.cell(200,50,ln=2)
        pdf.cell(200,20,txt='Top deals for today are:',align='C',ln=2)
        print('#############################################')
        print('Dumping data to {}.pdf\n\n'.format(self.file))
        #download images to temp folder and dump them into the pdf file
        with tempfile.TemporaryDirectory() as images:
            for url,price,title,platform in self.items:
                opener=req.URLopener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                file_name,_=opener.retrieve(url)
                pdf.set_font('Times',size=20,style='B')
                pdf.cell(200,10,ln=2)
                try:
                    pdf.add_page()
                    pdf.cell(200,20,txt=title,align='C',ln=2)
                    pdf.cell(200,5,ln=2)
                    pdf.image(file_name,x=80,w=40,h=40)
                    pdf.cell(200,5,ln=2)
                    pdf.set_font('Times',size=16)
                    price=price.encode('latin-1','replace').decode('latin-1').replace('?','USD')
                    pdf.cell(200,20,txt='Price : {}'.format(str(price)),ln=2,align='C')
                    pdf.cell(200,5,ln=2)
                    pdf.cell(200,20,txt='Platforms: {}'.format(platform),ln=2,align='C')
                except:
                    pass

        #output the pdf
        try:
            pdf.output("{}".format(os.path.join(filePath,"{}.pdf".format(filename))))
            print('######################################################')
            print('\nData successfully dumped to pdf\n')
        
        except:
            print('Sorry cannot dump data to pdf. Some error occured')
    
           