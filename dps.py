import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

import summarize


class DPS():
      
  def __init__(self, URLlst, n_subm_i, n_page_i):
      self.data = {}
      URLlst = URLlst
      n_subm = n_subm_i
      n_page = n_page_i
      
      for j, baseUrl in enumerate(URLlst):
          
        subsUrl = baseUrl + "//project-gallery?page="
        count = 1
        fieldsList = []
        try:
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

                        if self.isWinner(subObj):
                            title = self.getTitle(subObj)
                            subtitle = self.getSubtitle(subObj, title)
                            description = self.getDescription(subObj)
                            images = self.getImages(subObj)
                            builtWith = self.getBuiltWith(subObj)
                            print('> Adding to fieldsList')
                            print(f'\t> {title}')
                            fieldsList.append([title.get_text().strip(), subtitle.get_text().strip(), description, images, builtWith])
                    count = count + 1
                else:
                    pass

                self.data[URLlst[j]] = fieldsList
        except:
            pass
            
            
        
          
  def getData(self):
      return self.data
              

  def getTitle(self, subObj):
      title = subObj.find('h1', {'id':'app-title'})
      print(f"> {title.get_text().strip()}")
      return title


  def getSubtitle(self, subObj, title):
      subtitle = title.parent.find('p')
      return subtitle

  # # return true if winner, else false
  def isWinner(self, subObj):
      try: 
          print("\t> Submission is winner.")
          subObj.find('span', {'class':'winner'})
          return True
      except:
          print("\t> Not winner.")
          return False

  def getDescription(self, subObj):
      div_content = subObj.find('div', {'id':'app-details-left'})
      r_sets = div_content.find_all('p', {'id': False, 'class': False})

      desc = []
      for result in r_sets:
          desc.extend(result.getText())

      desc = (''.join(desc)).replace('\n', '')


      return summarize.Summarize(10, desc).summarize(3)

  def getImages(self, subObj):
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


  def getBuiltWith(self, subObj):
      builtWithList = []
      try:
          builtWith = subObj.find('div', {'id':'built-with'}).findAll('span', {'class':'cp-tag'})
          for tool in builtWith:
              builtWithList.append(tool.get_text().strip())
      except:
          print('\t> No Tools Found')
      return builtWithList
