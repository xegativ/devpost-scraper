import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

import summarize


class DPS:
    def __init__(self, URLlst, n_subm_i, n_page_i, dontCheckWinner=True):
        self.data = {}
        self.URLlst = URLlst
        self.n_subm = n_subm_i
        self.n_page = n_page_i
        self.dontCheckWinner = dontCheckWinner

    def getData(self):
        for j, baseUrl in enumerate(self.URLlst):
            subsUrl = baseUrl + "//project-gallery?page="
            count = 1
            fieldsList = []
            try:
                while count <= self.n_page:
                    subsObj = BeautifulSoup(
                        urlopen(subsUrl + str(count)), "html.parser"
                    )
                    submissions = subsObj.findAll(
                        "a", {"class": "block-wrapper-link fade link-to-software"}
                    )
                    if len(submissions) != 0:
                        for i, submission in enumerate(submissions):
                            if i >= self.n_subm:
                                break

                            print("> Checking submission")

                            subUrl = submission.attrs["href"]
                            subObj = BeautifulSoup(urlopen(subUrl), "html.parser")

                            # if we are not checking winner, only dependent on isWinner check
                            if self.isWinner(subObj) or self.dontCheckWinner:
                                print("> Is a winner OR not checking for winners")
                                title = self.getTitle(subObj)
                                subtitle = self.getSubtitle(subObj, title)
                                description = self.getDescription(subObj)

                                builtWith = self.getBuiltWith(subObj)
                                print("> Adding to fieldsList")
                                print(f"\t> {title}")
                                fieldsList.append(
                                    [
                                        title.get_text().strip(),
                                        subtitle.get_text().strip(),
                                        description,
                                        builtWith,
                                    ]
                                )
                            else:
                                print("> Not a winner and checking for winners")

                            print("FINISHED")
                        count = count + 1
                    else:
                        count = count + 1

                    self.data[self.URLlst[j]] = fieldsList
            except:
                pass
        return self.data

    def getTitle(self, subObj):
        title = subObj.find("h1", {"id": "app-title"})
        print(f"> {title.get_text().strip()}")
        return title

    def getSubtitle(self, subObj, title):
        subtitle = title.parent.find("p")
        return subtitle

    # # return true if winner, else false
    def isWinner(self, subObj):
        if subObj.find_all("span", {"class": "winner"}):
            print("\t> Submission is winner.")
            subObj.find("span", {"class": "winner"})
            return True
        else:
            print("\t> Not winner.")
            return False

    def getDescription(self, subObj):
        div_content = subObj.find("div", {"id": "app-details-left"})
        r_sets = div_content.find_all("p", {"id": False, "class": False})

        desc = []
        for result in r_sets:
            desc.extend(result.getText())

        desc = ("".join(desc)).replace("\n", ".")

        return summarize.Summarize(5, desc).summarize(2)

    def getImages(self, subObj):
        imgList = []
        try:
            images = subObj.find("div", {"id": "gallery"}).findAll("li")
            for image in images:
                try:
                    imgSrc = image.find("img")["src"]
                    imgList.append(imgSrc)
                except:
                    print("\t> Non-Image Link Found")
        except:
            print("\t> No Gallery Found")
        return imgList

    def getBuiltWith(self, subObj):
        builtWithList = []
        try:
            builtWith = subObj.find("div", {"id": "built-with"}).findAll(
                "span", {"class": "cp-tag"}
            )
            for tool in builtWith:
                builtWithList.append(tool.get_text().strip())
        except:
            print("\t> No Tools Found")
        return builtWithList
