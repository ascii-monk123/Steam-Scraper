import fpdf
import pandas as pd


class PDF:
    #constructor will take a filename as an argument
    def __init__(self,file):
        self.file=file
    def readCSV(self):
        try:
            self.df=pd.read_csv('{}.csv'.format(self.file))
        except:
            print('Couldnt read the required csv file')
            exit()