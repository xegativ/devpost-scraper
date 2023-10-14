import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

baseUrl = 'http://hackumass-ii.devpost.com'
subsUrl = baseUrl + '//submissions?page='


def main():
    count = 1
    fieldsList = []
    while True:
        subsObj = BeautifulSoup(urlopen(subsUrl + str(count)), 'html.parser')
        submissions = subsObj.findAll('a', {'class':'block-wrapper-link fade link-to-software'})
        if len(submissions) != 0:
            for submission in submissions:
                subUrl = submission.attrs['href']
                subObj = BeautifulSoup(urlopen(subUrl), 'html.parser')

                title = getTitle(subObj)
                subtitle = getSubtitle(subObj, title)
                images = getImages(subObj)
                builtWith = getBuiltWith(subObj)
                fieldsList.append([title.get_text().strip(), subtitle.get_text().strip(), images, builtWith])
            count = count + 1
        else:
            break
    writeToCSV(fieldsList)


def getTitle(subObj):
    title = subObj.find('h1', {'id':'app-title'})
    return title


def getSubtitle(subObj, title):
    subtitle = title.parent.find('p')
    return subtitle

def getDescription():
    pass

def getImages(subObj):
    imgList = []
    try:
        images = subObj.find('div', {'id':'gallery'}).findAll('li')
        for image in images:
            try:
                imgSrc = image.find('img')['src']
                imgList.append(imgSrc)
            except:
                print('Non-Image Link Found')
    except:
        print('No Gallery Found')
    return imgList


def getBuiltWith(subObj):
    builtWithList = []
    try:
        builtWith = subObj.find('div', {'id':'built-with'}).findAll('span', {'class':'cp-tag'})
        for tool in builtWith:
            builtWithList.append(tool.get_text().strip())
    except:
        print('No Tools Found')
    return builtWithList


def writeToCSV(fieldsList):
    csvFile = open('data/data.csv', 'wt')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('Title', 'Subtitle', 'Images', 'Built With'))
        for row in fieldsList:
            writer.writerow((row[0], row[1], row[2], row[3]))
    finally:
        csvFile.close()


main()
