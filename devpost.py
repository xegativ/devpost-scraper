import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

# BEAUTIFULSOUP 

baseUrl = 'http://hackthenorth2023.devpost.com'
# subsUrl = baseUrl + '//submissions?page='

subsUrl = baseUrl + "//project-gallery?page="

n_subm = int(input("# of submissions per page?\t"))
n_page = int(input("# of pages?\t"))

def main():
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
    writeToCSV(fieldsList)


def getTitle(subObj):
    title = subObj.find('h1', {'id':'app-title'})
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

    return desc

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


def writeToCSV(fieldsList):
    csvFile = open('data/data.csv', 'wt', encoding="utf-8")
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('Title', 'Subtitle', 'Description', 'Images', 'Built With'))
        for row in fieldsList:
            writer.writerow((row[0], row[1], row[2], row[3], row[4]))
    finally:
        csvFile.close()


main()
