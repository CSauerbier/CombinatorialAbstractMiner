from pybliometrics.scopus import ScopusSearch
from tqdm import tqdm
import xlsxwriter
from datetime import datetime

class Document:

    def setAuthor(self, author):
        self.author = author
    
    def setTitle(self,title):
        self.title = title

    def setAbstract(self, abstract):
        self.abstract = abstract

    def setKeywords(self, keywords):
        self.keywords = keywords

    def setEntryNo(self, entryNo):
        self.entryNo = entryNo

    def setDOI(self, doi):
        self.doi = doi

class PermutationIterator:
    def __init__(self, *keywords):
        self.keywords = keywords
        self.maxCounters = []
        self.curCounters = []
        self.iterationIncomplete = True
        
        for kws in keywords:
            self.maxCounters.append(len(kws))
            self.curCounters.append(0)

        prod = 1        #ToDo: Replace by prod-function in math-library (starting Python 3.8)
        for multiplier in self.maxCounters:
            prod = prod * multiplier
        self.noOfIterations = prod
    
    def getNextPermutation(self):
        retValue = []
        for i, kw in enumerate(self.keywords):
            retValue.append(kw[self.curCounters[i]])
        self.increment()

        return retValue
            
    def increment(self):
        carry = 1
        for i in range(len(self.curCounters)):
            self.curCounters[i] = self.curCounters[i] + carry
            carry = 0
            if (self.curCounters[i] == self.maxCounters[i]):
                carry = 1
                self.curCounters[i] = 0
        if (carry == 1):
            self.iterationIncomplete = False

class Database:
    def __init__(self):
        self.entries = {}
    
    def addItem(self, doc):
        if(doc.doi not in self.entries):
            self.entries[doc.doi] = doc
            return True
        else: 
            return False



class ScopusMiner:

    def __init__(self):
        self.noOfResults = 3
        self.database = Database()
    
    def setNoOfResults(self,noOfResults):
        self.noOfResults = noOfResults
    
    def performSearch(self, searchWords):
        # Create Search-String
        # Searching in TITLE-ABStract-KEYwords is the default search mode on scopus
        searchString = 'TITLE-ABS-KEY('
        for i, word in enumerate(searchWords):
            searchString = searchString + word
            if (i != len(searchWords)-1):
                searchString = searchString + ' AND '
            #Last Item
            else:   
                searchString = searchString + ')'

        self.searchResult = ScopusSearch(searchString)
        self.searchWords = searchWords

        self.storeResultsInDB()
    
    def storeResultsInDB(self): 
        NoOfResultsStored = 0
        i = 0
        while(NoOfResultsStored < self.noOfResults):
            if(i >= self.searchResult.get_results_size() or self.searchResult.results == None):
                break 
            doc = Document()
            doc.setAbstract(self.searchResult.results[i][27])
            doc.setAuthor(self.searchResult.results[i][13])
            doc.setDOI(self.searchResult.results[i][1])
            doc.setEntryNo(i)
            doc.setKeywords(self.searchWords)
            doc.setTitle(self.searchResult.results[i][4])
            i = i + 1

            if(self.database.addItem(doc)):
                NoOfResultsStored = NoOfResultsStored + 1
    
    def run(self, *keywords):
        self.permIterator = PermutationIterator(*keywords)
        for i in tqdm(range(self.permIterator.noOfIterations)):
            self.performSearch(self.permIterator.getNextPermutation())
        
        self.writeToExcel()
        
    def writeToExcel(self):
        now = datetime.now()
        date_time = now.strftime("%Y%m%d_%H%M")
        workbook = xlsxwriter.Workbook('PermutationSearchResults'+date_time+'.xlsx')
        worksheet = workbook.add_worksheet()
        
        row = 0
        for key in self.database.entries:
            entry = self.database.entries.get(key)

            for i, word in enumerate(entry.keywords):
                worksheet.write(row, i, word)
            worksheet.write(row, i+1, entry.doi)
            worksheet.write(row, i+2, entry.author)
            worksheet.write(row, i+3, entry.title)
            worksheet.write(row, i+4, entry.entryNo)
            worksheet.write(row, i+5, entry.abstract)
            
            row = row + 1
            
        workbook.close()

