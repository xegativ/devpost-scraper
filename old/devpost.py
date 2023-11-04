import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

import summarize

# BEAUTIFULSOUP 

fileSaveChoice = input("Save to file? (Y/N): ")
if fileSaveChoice == "Y":
    filesave = True
    filename = input("Save to which file (or create new): ")
else:
    filesave = False

# Hack the North
HTN = ['http://hackthenorth2018.devpost.com', 'http://hackthenorth2019.devpost.com', 'http://hackthenorth2020.devpost.com', 'http://hackthenorth2021.devpost.com', 'http://hackthenorth2022.devpost.com', 'http://hackthenorth2023.devpost.com']

# NWHacks
NWH = ['http://nwhacks2018.devpost.com', 'http://nwhacks2019.devpost.com', 'http://nwhacks2020.devpost.com', 'http://nwhacks2021.devpost.com', 'http://nwhacks-2022.devpost.com', 'http://nwhacks-2023.devpost.com']

# HackCamp
HKC = ['http://hackcamp2020.devpost.com', 'http://hackcamp2021.devpost.com', 'http://hackcamp-2022.devpost.com']

CUSTOM = ['http://systemshacks-2023-roothacks.devpost.com']

URLlst = [] + CUSTOM

# subsUrl = baseUrl + "//project-gallery?page="

n_subm = int(input("# of submissions per page?\t"))
n_page = int(input("# of pages?\t"))

data = {}

def main():
    for j, baseUrl in enumerate(URLlst):
        subsUrl = baseUrl + "//project-gallery?page="
        count = 1
        fieldsList = []
        while count <= n_page:
            subsObj = BeautifulSoup(urlopen(subsUrl + str(count)), 'html.parser')
            submissions = subsObj.findAll('a', {'class':'block-wrapper-link fade link-to-software'})
            if len(submissions) != 0:
                for i, submission in enumerate(submissions):

                    if i >= n_subm:
                        break

                    print("> Checking submission")

                    subUrl = submission.attrs['href']
                    subObj = BeautifulSoup(urlopen(subUrl), 'html.parser')

                    if isWinner(subObj):
                        title = getTitle(subObj)
                        subtitle = getSubtitle(subObj, title)
                        description = getDescription(subObj)
                        images = getImages(subObj)
                        builtWith = getBuiltWith(subObj)
                        fieldsList.append([title.get_text().strip(), subtitle.get_text().strip(), description, images, builtWith])
                        
                count = count + 1
            else:
                break
            
            if filesave == True:
                writeToCSV(fieldsList, j)
            print(len(fieldsList))
            data[URLlst[j]] = fieldsList
    print(data)

def getTitle(subObj):
    title = subObj.find('h1', {'id':'app-title'})
    print(f"> {title.get_text().strip()}")
    return title


def getSubtitle(subObj, title):
    subtitle = title.parent.find('p')
    return subtitle

# # return true if winner, else false
def isWinner(subObj):
    try: 
        print("\t> Submission is winner.")
        subObj.find('span', {'class':'winner'})
        return True
    except:
        print("\t> Not winner.")
        return False

def getDescription(subObj):
    div_content = subObj.find('div', {'id':'app-details-left'})
    r_sets = div_content.find_all('p', {'id': False, 'class': False})

    desc = []
    for result in r_sets:
        desc.extend(result.getText())

    desc = (''.join(desc)).replace('\n', '')


    return summarize.Summarize(10, desc).summarize(3)

def getImages(subObj):
    imgList = []
    try:
        images = subObj.find('div', {'id':'gallery'}).findAll('li')
        for image in images:
            try:
                imgSrc = image.find('img')['src']
                imgList.append(imgSrc)
            except:
                print('\t> Non-Image Link Found')
    except:
        print('\t> No Gallery Found')
    return imgList


def getBuiltWith(subObj):
    builtWithList = []
    try:
        builtWith = subObj.find('div', {'id':'built-with'}).findAll('span', {'class':'cp-tag'})
        for tool in builtWith:
            builtWithList.append(tool.get_text().strip())
    except:
        print('\t> No Tools Found')
    return builtWithList


def writeToCSV(fieldsList, index):
    csvFile = open(f'../data/{filename}.csv', 'at', encoding="utf-8")
    try:
        writer = csv.writer(csvFile)
        # writer.writerow(('Title', 'Subtitle', 'Description', 'Images', 'Built With'))
        writer.writerow([URLlst[index]])
        for row in fieldsList:
            writer.writerow((row[0], row[1], row[2], row[3], row[4]))
    finally:
        csvFile.close()


main()
