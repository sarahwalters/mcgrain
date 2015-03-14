import pandas
import numpy as np
import scipy
import pprint
import matplotlib.pyplot as plt
import sympy.plotting as tplt
import pylab as P
import scipy.stats as stats

def parseOutCountryData(country="United States of America", fileout = "USData.csv", filein = 'Production_Crops_E_Americas_1.csv'):
    '''Parse out data for a specific country into a seprate file so the program doesn't have to craw throguh all 
    the data. 
    
    NOTE: opens file in append mode, so if you call this repetelt, you'll have the data for the country in question
    many times in the same file (unless you change the file name. This probably isn't what you want. To avoid this,
    rm the file before running this function again.'''
    FullData = open(filein, 'r')
    with open(fileout, "a") as usadata:
        for line in FullData: 
            if country in line: 
                usadata.write(line)
            if 'Country' in line:
                usadata.write(line)
        

def makeFAOSTATdf(region='short'):
    '''Make a pandas dataframe from the data in a given region (CSV file)'''
    if region=='short':
        data=open('FeedGrains.csv', 'r')
    elif region=='middle':
        data=open('FAOSTAT_Full.csv', 'r')
    elif region=='world':
        data=open('full_FAOSTAT.csv', 'r')
    elif region=='us':
        data=open('USData.csv', 'r')
    else: 
        raise Exception("Unknown data form. Please specify your data file with the data key in the function call")
    return pandas.DataFrame.from_csv(data)


def buildYearList(start = 1961, end = 2013):
    '''Constructs & returns a dictionary with Y[year] as the key and the year as the value for working with the 
    FAOSTAT dataframe.'''
    yearList = {}
    for year in range(start,end):
        yearStr='Y'+str(year)
        yearList[yearStr]= year
    return yearList


def sumYieldYears(yearList, crop='Corn'):
    '''Returns a dictionary of production data for a given crop for a given set of years.'''
    cropDenotation='Item'
    cropYear={}
    for index, row in df.iterrows():
        if (row[cropDenotation] == crop) and (row['Element']=='Production'):
            for year in yearList:
                cropYear[yearList[year]] = row[year]
    return cropYear


def getProductionCertainYear(yearList, year=2013, crop='Asparagus'):
    '''Returns a dictionary of production data for a given crop for a given  year.'''
    cropDenotation='Item'
    cropYear={}
    production = {}
    for index, row in df.iterrows():
        if row['Element'] == 'Production':
            if row['Item'] in production:
                production[row['Item']] = production[row['Item']] + row['Y'+str(year)]
            else: production[row['Item']] = row['Y'+str(year)]
#            pprint.pprint(production)
    return production
            

def cropScatterplotByYear(cropYear, crop):
    '''Makes a cscatterplot for a given dataset'''
    plt.plot(cropYear.keys(),cropYear.values(), 'r*', linewidth=4.0)
    plt.xlabel('Year', fontsize=17)
    plt.ylabel('Tonnes Produced', fontsize=17)
    plt.title(crop+' Production Over Time', fontsize=22)
    plt.show()


def makeHistogramByCrop(yearList, cropYear, crop):
    #TODO: Fix error yielded
    bins=[]
    crops=[]
    years=[]
    for year in yearList:
        years.append(yearList[year])
        crops.append(cropYear[yearList[year]])
###    for year in yearList.values():
###        if (year%5) == 0:
###            bins.append(year)
    pprint.pprint(zip(years,crops))
    years=np.array(years)
    crops=np.array(crops)
    n, bins, patches = P.hist(years, crops, normed=1, histtype='bar', rwidth=0.8)
    P.show()
    
def cropScatterplotByYearLinFit(cropYear, crop):
    #TODO: Fix error yielded
    x=cropYear.keys(); y=cropYear.values()
    plt.plot(x,y, 'r*', linewidth=4.0)
    m,b = np.polyfit(x, y, 1) 
    plt.plot(x, m*x+b, 'k',linewidth=3.0) 
    plt.xlabel('Year', fontsize=17)
    plt.ylabel('Tonnes Produced', fontsize=17)
    plt.title(crop+' Production Over Time', fontsize=22)
    plt.show()
    

    
    
def runScatterForCropsWeCareAbout():
    cropsWeCareAbout = ['Corn', 'Cotton lint', 'Soybeans', 'Wheat']
    yearList = buildYearList()
    resultsDict={}
    for crop in cropsWeCareAbout:
        cropYear = sumYieldYears(yearList, crop=crop)
        cropScatterplotByYear(cropYear, crop)
        resultsDict[crop] =cropYear
    return resultsDict


def histTest():
    '''test of histogram functionality from the interwebs!'''
    mu, sigma = 200, 25
    x = mu + sigma*P.randn(10000)
    bins = [100,125,150,160,170,180,190,200,210,220,230,240,250,275,300]
    # the histogram of the data with histtype='step'
    n, bins, patches = P.hist(x, bins, normed=1, histtype='bar', rwidth=0.8)
    # now we create a cumulative histogram of the data
    P.figure()
    P.show()
    
    
def makePMF(cropYear):
    from scipy.stats import binom
    import matplotlib.pyplot as plt2
    fig, ax = plt2.subplots(1, 1)
    n=cropYear.keys(); p=cropYear.values()
    scipy.stats.rv_discrete.pmf(n)
    #x = np.arange(binom.ppf(0.01, n, p), binom.ppf(0.99, n, p))
###    x=n; y=p;
###    ax.plot(x, binom.pmf(x, n, p), 'bo', ms=8, label='binom pmf')
###    ax.vlines(x, 0, binom.pmf(x, n, p), colors='b', lw=5, alpha=0.5)
###    plt2.show()
#    rv = binom(n, p)
#    ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1, label='frozen pmf')
#    ax.legend(loc='best', frameon=False)
#    plt2.show()
    
def getSumaryStatistics(cropYear, crop):
    var = np.var(cropYear.values()); print crop, ' production variance is: ',var, ' tonnes'
    std = np.std(cropYear.values()); print crop, ' production standard deviation is: ',std, ' tonnes'
    
#parseOutCountryData()
df = makeFAOSTATdf(region='us')
#runScatterForCropsWeCareAbout()

##cropYear = sumYieldYears(yearList, crop='Spinach')
##cropScatterplotByYear(cropYear, 'Spinach')

yearList = buildYearList()        
#cropYear = sumYieldYears(yearList, crop='Soybeans')
#makeHistogramByCrop(yearList, cropYear, 'Spinach')
#cropScatterplotByYearLinFit(cropYear,  'Spinach')
#getSumaryStatistics(cropYear, crop='Soybeans')
#makePMF(cropYear)
getProductionCertainYear(yearList)


#TODO: 
##PMF
##PDF
##CDF
##Histogram

