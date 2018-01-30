import urllib.request
from bs4 import BeautifulSoup
import json
import os

def fetchSpellHtmlFromDxcontent(spellNumber):

    dxContentSpellUrl ="http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID="
    spellUrl = dxContentSpellUrl + str(spellNumber)
    page = urllib.request.urlopen(spellUrl)
    return page


def main():
    maxSpellNumber = 1975 # max possible 1975
    spellDataTab = [];
    for i in range(1, maxSpellNumber+1):
        try:
            spellHtml =fetchSpellHtmlFromDxcontent(i)
            spellSoup = BeautifulSoup(spellHtml,"html.parser")
            spellDiv = spellSoup.find("div", {"class": "SpellDiv"})

            # Find if the spell is a wizard spell
            spellSchoolList = str.split(spellDiv.findAll("p", {"class": "SPDet"})[0].text)

            if ("sorcerer/wizard" in spellSchoolList) or ("wizard" in spellSchoolList):
                # Find level of the spell
                # take the next one in the list which is the level of the spell
                if ("sorcerer/wizard" in spellSchoolList):
                    spellLevel = spellSchoolList[spellSchoolList.index("sorcerer/wizard") + 1]
                else:
                    spellLevel = spellSchoolList[spellSchoolList.index("wizard") + 1]
                # change the spellLevel string in int
                spellLevel = int(spellLevel.strip(","))

                #Find the name of the spell
                spellName = spellDiv.find("div", {"class": "heading"}).text

                #Find spell component
                spellComponentList_unrefined = str.split(spellDiv.findAll("p", {"class": "SPDet"})[2].text )
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

                #find if there is a spell resistance
                if ( len(spellDiv.findAll("p", {"class": "SPDet"}) ) == 6):
                    # old spell by default we put spell resistance at false
                    spellResistance =False;
                elif ( len(spellDiv.findAll("p", {"class": "SPDet"}) ) == 7):
                    spellResistanceHtmlDiv = spellDiv.findAll("p", {"class": "SPDet"})[6];
                    if ("<b>Spell Resistance</b> no" in spellResistanceHtmlDiv):
                        spellResistance =False
                    elif ("<b>Spell Resistance</b> yes" in spellResistanceHtmlDiv):
                        spellResistance = True
                    else: #can be improve for particular case
                        spellResistance =False; #value by default

                #create the spell data for this spell
                spellData ={}
                spellData["name"] = spellName
                spellData["level"] = spellLevel
                spellData["components"] = spellComponentList
                spellData["spell_resistance"] = spellResistance
                #put this data in a tab
                spellDataTab.append(spellData)
                #print(i)
        except (AttributeError):
            print("error with the spell:" ,i ,"")
            pass
    #create our json object
    jsonData = json.dumps(spellDataTab)
    # Writing JSON file

    # delete previous file if exist
    try:
        os.remove('jsonSpellData.json')
    except OSError:
        pass
    #create and write
    with open('jsonSpellData.json', 'w') as f:
        json.dump(spellDataTab, f)

if __name__ == "__main__":
    main();