import urllib.request
from bs4 import BeautifulSoup
import json
import os
import time

def fetchSpellHtmlFromDxcontent(spellNumber):
    try:
        dxContentSpellUrl ="http://www.dxcontent.com/SDB_SpellBlock.asp?SDBID="
        spellUrl = dxContentSpellUrl + str(spellNumber)
        page = urllib.request.urlopen(spellUrl)
        return page
    except():
        print("Error: can't fetch dxContent Html check if you are connected")
        quit()  # terminate programme


def findTheDurationHtml(spellDiv):
    maxRange = len(spellDiv.findAll("p", {"class": "SPDet"}) ) ;
    for i in range(0, maxRange):
        durationHtml = str.split(spellDiv.findAll("p", {"class": "SPDet"})[i].text);
        if (durationHtml[0] == "Duration"):
            return durationHtml;
    return None;

def findSpellResistanceHtml(spellDiv):
    maxRange = len(spellDiv.findAll("p", {"class": "SPDet"}));
    for i in range(0, maxRange):
        spellResistanceHtml = str.split(spellDiv.findAll("p", {"class": "SPDet"})[i].text);
        if ("Spell" in spellResistanceHtml) and ("Resistance" in spellResistanceHtml):
            return spellResistanceHtml;
    return None;

def main():
    timeStart = time.time()
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

                #===find out if the spell is instantaneous===#
                instantaneous =False;
                try:
                    durationHtml = str.split(spellDiv.findAll("p", {"class": "SPDet"})[5].text )
                    # the duration is not in an usual place, we must look for it
                    if ( durationHtml[0] != "Duration"):
                        durationHtml = findTheDurationHtml(spellDiv)
                except:
                    # the duration is not in an usual place, we must look for it
                    durationHtml = findTheDurationHtml(spellDiv)

                if (len (durationHtml) < 2):
                    # some spell don't have a duration indication set to false by default
                    print("no duration given for the spell :", i)
                elif (durationHtml[1] == "instantaneous"):
                    instantaneous = True;

                #===find if there is a spell resistance===
                spellResistance =False;
                try:
                    spellResistanceHtml = str.split(spellDiv.findAll("p", {"class": "SPDet"})[6].text )
                    #not use, but add safety mesure
                    if ( not ("Spell" in spellResistanceHtml) or  not ("Resistance" in spellResistanceHtml) ):
                        spellResistanceHtml = findSpellResistanceHtml(spellDiv);
                except(IndexError):
                    # the spell resistance is not in an usual place, we must look for it
                    spellResistanceHtml = findSpellResistanceHtml(spellDiv);
                # old spell by default we put spell resistance at false
                if ( spellResistanceHtml == None):
                    spellResistance =False;
                else :
                    indexSpellResistance = spellResistanceHtml.index("Resistance") +1;
                    if ( spellResistanceHtml[indexSpellResistance] == "yes" ):
                        spellResistance = True;

                #create the spell data for this spell
                spellData ={}
                spellData["name"] = spellName
                spellData["level"] = spellLevel
                spellData["components"] = spellComponentList
                spellData["spell_resistance"] = spellResistance
                spellData["instantaneous"] = instantaneous
                #put this data in a tab
                spellDataTab.append(spellData)
                #print(i)
        except (AttributeError):
            print("error with the spell:" ,i ,"")
            pass

    #create our json object
    jsonData = json.dumps(spellDataTab)
    # delete previous file if exist
    try:
        os.remove('jsonSpellData.json')
    except OSError:
        pass
    #create and write
    with open('jsonSpellData.json', 'w') as f:
        # Writing JSON file
        json.dump(spellDataTab, f, indent=4)
    timeEnd = time.time()
    print("Execution time :", timeEnd - timeStart, "s");

if __name__ == "__main__":
    main();
