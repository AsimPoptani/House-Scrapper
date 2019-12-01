from contextlib import redirect_stderr

import requests
from bs4 import BeautifulSoup
import xlsxwriter , json
houses=[]
class House:
    def __init__(self,address,features,info,overview,distances,source):
        self.address=address
        self.features=features
        self.info=info
        self.overview=overview
        self.distances=distances
        self.source=source
        self.extraData=""

def text2int(textnum, numwords={}):
    try:
        textnum=textnum.lower()
        if (textnum=="none"):
            return 0
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


cookies = {
    'PHPSESSID': 'hbaqfhl0vpgu1q6mc359bs4p13',
    'CSRF_TOKEN': '2936fbbd157798682e2f425af16e98839af0c130a8604314333518136b2904642f6ff11299472d4e',
    '__utma': '31147887.1347027106.1548351185.1548351185.1548351185.1',
    '__utmc': '31147887',
    '__utmz': '31147887.1548351185.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '__utmt': '1',
    '__utmb': '31147887.47.0.1548351779898',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.adambennett.co.uk/property/studentlist',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,fr-FR;q=0.7,fr;q=0.6',
}

params = (
    ('isForSale', '0'),
    ('Property_page', '0'),
)

data = {
  'PropertySearchForm[minBeds]': '4',
  'PropertySearchForm[maxBeds]': '4'
}


responses=[]
for i in range(1,10):
    responses.append( requests.get('https://www.adambennett.co.uk/student-properties.html?isForSale=0&Property_page='+str(i), data=data, headers=headers, cookies=cookies))


propUrls=[]
for response in responses:
    for beautiful in BeautifulSoup(response.text,'html.parser').find_all("a", class_="btn btn-default more-info"):
        propUrls.append((beautiful['href']))



for url in propUrls:
    #address,features,info,overview,distances,source
    page=requests.get(url).text
    pageBeautiful=BeautifulSoup(page,'html.parser')
    address=pageBeautiful.find_all("h3", class_="panel-title")[1].text
    features=pageBeautiful.find_all("div",class_="pull-right")[4]
    featureList=""
    for feature in features:
        try:
            featureList+="Has a "+ feature.find_all("img")[0]["alt"]+"\n"
        except Exception:
            pass
    info=BeautifulSoup(requests.get(url+'?getTabData=description').text,'html.parser').find_all("p")[0].text
    overview=pageBeautiful.find_all("i")[5].text
    source=url
    houses.append(House(address,featureList,info,overview,None,source))


workbook = xlsxwriter.Workbook('adamBennett.xlsx')
worksheet = workbook.add_worksheet()
worksheet.name="Properties"


col=0
for info in ([["Address"]+["Info"]+["Overview"]+["Distance to comp sci and law"],["Distance to physics"],["Walking duration to comp sci and law"],["Walking duration to physics"],["Bus travel to Comp sci and law"],["Bus travel to physics"],["Features"],["Source"],["Any questions?"]]):
        worksheet.write(1,col,str(info[0]))
        col+=1


row=2
counter=0
for house in houses:
    col=0
    worksheet.write(row,col, house.address)
    counter+=1
    print(str((counter/len(houses))*100)+"% Looked up maps")


    for info in [house.info,house.overview]:
        col+=1
        worksheet.write(row,col,info)

    #Find time to get to Comp sci and Law and phy
    phy="Physics and Electronic Engineering Buildings, Heslington, York YO10 5EZ".replace(" ","+")
    compSciAndLaw="Department of Computer Science, Deramore Ln, Heslington YO10 5GH".replace(" ","+")


    phyWalkData=requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=' + str(house.address).replace(" ", "+") + '&mode=walking&destination=' + phy + '&key=AIzaSyC6P_8fzVlH0jHTtlHeemKj8n2zv60wyFk').text
    compSciAndLawWalkData=requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=' + str(house.address).replace(" ", "+") + '&mode=walking&destination=' + compSciAndLaw + '&key=AIzaSyC6P_8fzVlH0jHTtlHeemKj8n2zv60wyFk').text
    phyBusData=requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=' + str(house.address).replace(" ", "+") + '&mode=transit&destination=' + phy + '&key=AIzaSyC6P_8fzVlH0jHTtlHeemKj8n2zv60wyFk').text
    compSciAndLawBusData=requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=' + str(house.address).replace(" ", "+") + '&mode=transit&destination=' + compSciAndLaw + '&key=AIzaSyC6P_8fzVlH0jHTtlHeemKj8n2zv60wyFk').text


    durationWalkPhy=""
    durationBusPhy=""
    distancePhy=""

    durationWalkCompSciAndLawData=""
    durationBusCompSciAndLawData=""
    distanceCompSciAndLawData=""

    try:
        durationWalkPhy=json.loads(phyWalkData)["routes"][0]["legs"][0]["duration"]["text"]
        durationBusPhy=json.loads(phyBusData)["routes"][0]["legs"][0]["duration"]["text"]
        distancePhy=json.loads(phyWalkData)["routes"][0]["legs"][0]["distance"]["text"]
        durationWalkCompSciAndLawData=json.loads(compSciAndLawWalkData)["routes"][0]["legs"][0]["duration"]["text"]
        durationBusCompSciAndLawData=json.loads(compSciAndLawBusData)["routes"][0]["legs"][0]["duration"]["text"]
        distanceCompSciAndLawData=json.loads(compSciAndLawWalkData)["routes"][0]["legs"][0]["distance"]["text"]
    except Exception as e:
        continue




    col+=1
    worksheet.write(row,col,distanceCompSciAndLawData)
    col+=1
    worksheet.write(row,col,distancePhy)
    col+=1
    worksheet.write(row, col, durationWalkCompSciAndLawData)
    col+=1
    worksheet.write(row, col, durationWalkPhy)
    col+=1
    worksheet.write(row, col, durationBusCompSciAndLawData)
    col+=1
    worksheet.write(row, col, durationBusPhy)
    col+=1
    worksheet.write(row,col,house.source)
    col+=1
    worksheet.write(row,col,",".join(house.features))
    row+=1
workbook.close()
