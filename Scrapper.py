import requests
from bs4 import BeautifulSoup
import xlsxwriter

houses=[]
class House:
    def __init__(self,address,features,info,overview,distances,source):
        self.address=address
        self.features=features
        self.info=info
        self.overview=overview
        self.distances=distances
        self.source=source
        self.extraData="""
Virgin High Speed Broadband (with up to 350Mbps speed) or, *where Virgin infrastructure is genuinely not available, we will install the very highest broadband speed available to that property.
Gas (where installed)
Electricity
Water
Sewerage rates
Service charges
TV Licence
Contents Insurance with Endsleigh Insurance covers up to £5,000 of your personal effects for each person in the house.
"""

def text2int(textnum, numwords={}):
    try:
        textnum=textnum.lower()
        if not numwords:
          units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
          ]

          tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

          scales = ["hundred", "thousand", "million", "billion", "trillion"]

          numwords["and"] = (1, 0)
          for idx, word in enumerate(units):    numwords[word] = (1, idx)
          for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
          for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

        current = result = 0
        for word in textnum.split():
            if word not in numwords:
              raise Exception("Illegal word: " + word)

            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return result + current
    except Exception:
        return textnum

#Get the ids
data=requests.get('https://www.sinclair-properties.com/search-results?NumberBedrooms=%3dfour&Location=%3d*UY*&PricePerPersonPerWeek=%3E0&availdate=&available=&xxorderby=%5borderbydesc%5d%3dpriceperpersonperweek&xxnum=200&xxpage=1')
idsees=BeautifulSoup(data.text,'html.parser').find_all("input", class_="turquoise")
ids=[]
for ident in idsees:
    #extract id
    #ident=BeautifulSoup(ident,'html.parser').prettify()
    if "GoToBrochure" in str(ident):
        ident=str(ident)
        ident=ident.replace("<input class=\"turquoise\" onclick=\"Javascript:GoToBrochure_OnClick('","")
        ident=ident.replace("');return false;\" type=\"submit\" value=\"Brochure\"/>","")
        ids.append(ident)

#get the data
#https://www.sinclair-properties.com/search-results/brochure?id=37ff7c31-445a-4ce3-8bcc-5386613cdad7

for ident in ids:
    source="https://www.sinclair-properties.com/search-results/brochure?id={}".format(ident)
    data=requests.get(source)
    data=BeautifulSoup(data.text,'html.parser')
    address=str(data.findAll("h1")[2].get_text())
    information=data.findAll("div", class_="col_third")
    info=information[0]
    overview=information[1]
    distances=information[2]
    features=information[3]
    infoList=[]
    overviewList=[]
    distancesList=[]
    featuresList=[]
    #infoList
    for dataInHtml in info.findAll("tr"):
        infoList.append((str(dataInHtml.findAll("td")[0].get_text()).replace(":",""), dataInHtml.findAll("td")[1].get_text()))
    #OverviewList
    for dataInHtml in overview.findAll("tr"):
        overviewList.append((str(dataInHtml.findAll("td")[0].get_text()).replace(":",""), dataInHtml.findAll("td")[1].get_text()))
    #distancesList
    for dataInHtml in distances.findAll("tr"):
        distancesList.append((dataInHtml.findAll("td")[0].get_text(), dataInHtml.findAll("td")[1].get_text()))
    #featuresList
    for dataInHtml in features.findAll("li"):
        featuresList.append(dataInHtml.getText())
    houses.append(House(address,featuresList,infoList,overviewList,distancesList,source))

workbook = xlsxwriter.Workbook('prop.xlsx')
worksheet = workbook.add_worksheet()
worksheet.name="Propeties"
worksheet.write(1,0,"Address")
col=1
for info in (houses[0].info+houses[0].overview+houses[0].distances+[["Features"]]+[["Source"]]):
        worksheet.write(1,col,str(info[0]))
        col+=1


row=2
for house in houses:
    col=0
    worksheet.write(row,col, house.address)

    for info in (house.info+house.overview+house.distances):
        col+=1
        worksheet.write(row,col,text2int(str(info[1])))
    worksheet.write(row,col+1,",".join(house.features))
    worksheet.write(row,col+2,house.source)
    row+=1
workbook.close()
