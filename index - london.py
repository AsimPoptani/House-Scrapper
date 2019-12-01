import requests
from bs4 import BeautifulSoup
import xlsxwriter , json
houses=[]
estateAgents=[]

class EstateAgent:
    def __init__(self,name,tel,email,website):
        self.name=name
        self.tel=tel
        self.email=email
        self.website=website

class House:
    def __init__(self,address,features,info,overview,distances,source,pricePerWeek,extraData,EstateAgent):
        self.address=address
        self.features=features
        self.info=info
        self.overview=overview
        self.distances=distances
        self.source=source
        self.pricePerWeek=pricePerWeek
        self.extraData=extraData
        self.EstateAgent=EstateAgent.name


#Ask some questions
    #Number of beds
    numberOfBedrooms=int(input("How many bedrooms:"))
    #Locations which are notable
    importantLocations=[]

#Do some searching

    #Beverley Williams & Associates Ltd
    BeverleyWilliams=EstateAgent("Beverley Williams & Associates Ltd","01344 874300",None, "www.beverleywilliams.co.uk" )
    estateAgents.append(BeverleyWilliams)
    "http://www.beverleywilliams.co.uk/listings.php?sale=2&min_beds={}"



    #Chancellors
    Chancellors=EstateAgent("Chancellors","01344 876487",None, "www.chancellors.co.uk")
    #https://www.chancellors.co.uk/properties/search?area=Imperial+College+London&saleType=rent&radius=40&maxBeds=4&show=96&minBeds=1&page=1
    for i in range(1,20):
        data=requests.get('https://www.chancellors.co.uk/properties/search?area=Imperial+College+London&saleType=rent&radius=40&maxBeds={}&show=96&minBeds={}&page={}'.format(numberOfBedrooms,numberOfBedrooms,i))
        data=BeautifulSoup(data.text,'html.parser')
        property=data.find_all("div",class_="cell small-10")
        for prop in property:
            price=prop.find_all("h4",{"class","archive-property__price"})[0].get_text()
            address=prop.find_all("p",{"class","archive-property__location"})[0].get_text()
            "archive-property__description"
    estateAgents.append(Chancellors)




