from html.parser import HTMLParser
import urllib.request
from bs4 import BeautifulSoup

def fetchSpellHtmlFromDxcontent(spellNumber):

    dxContentSpellUrl ="http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID="
    spellUrl = dxContentSpellUrl + str(spellNumber)
    page = urllib.request.urlopen(spellUrl)
    return page


def main():
    maxSpellNumber = 10
    for i in range(1, maxSpellNumber+1):
        spellHtml =fetchSpellHtmlFromDxcontent(i)
        spellSoup = BeautifulSoup(spellHtml,"html.parser")
        spellDiv = spellSoup.find("div", {"class": "SpellDiv"})

        # Find if the spell is a wizard spell
        spellSchoolList = str.split(spellDiv.findAll("p", {"class": "SPDet"})[0].text)

        if ("sorcerer/wizard" in spellSchoolList) or ("wizard" in spellSchoolList):
            # Find level of the spell
            # take the next one in the list which is the level of the spell
            spellLevel = spellSchoolList[spellSchoolList.index("sorcerer/wizard") + 1]
            # change the spellLevel string in int
            spellLevel = int(spellLevel.strip(","))

            #Find the name of the spell
            spellName = spellDiv.find("div", {"class": "heading"}).text
            print(spellName)


            #Find spell component
            spellComponentList_unrefined = str.split( spellDiv.findAll("p", {"class": "SPDet"})[2].text )
            spellComponentList =[]
            #refined the list
            insideBraket =False
            for y in range(1, len(spellComponentList_unrefined) ):#no need to test the first element
                spellComponentList_unrefined[y] =spellComponentList_unrefined[y].strip(",")
                if ( "(" in spellComponentList_unrefined[y] ):
                    insideBraket = True
                elif ( ")" in spellComponentList_unrefined[y] ):
                    insideBraket = False
                elif (not insideBraket):
                    spellComponentList.append(spellComponentList_unrefined[y])
            print(spellComponentList)
            #find if there is a spell resistance

            
        #else:
            #not a wizar spell

if __name__ == "__main__":
    main();