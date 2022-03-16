import requests
import csv
from bs4 import BeautifulSoup
directory_url = "https://www.bbb.org/us/category/"
categories = ["financial-services", "bank", "banking-services"]
data = []

def get_content(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    content = BeautifulSoup(r.content, 'html5lib') 
    # get main content
    info = content.find("div", attrs={'class':'Main-sc-f9kltc-0 jIndWh'})

    for row in info.findAll('div', attrs={'class':'result-item-ab'}):
        lead = {}
        lead['businessName'] = row.find('h3', attrs={'class': 'result-item-ab__name'}).span.text
        lead['location'] = row.find('p', attrs={'result-item-ab__address'}).text

        # check if phone number is provided
        phone_no = row.find('p', attrs={'class': 'result-item-ab__phone'})
        if phone_no is None:
            lead['phone'] = "n/a"
        else:
                lead['phone'] = phone_no.text
        data.append(lead)

    next_button = content.find('a', attrs={'class': 'search-pagination__next-page'})
    if next_button is None: # is last page?
        return data
    get_content(next_button['href'])

def writeToFile(): # change to write new file if one exists instead of overwriting
    with open('LEADS_FROM_BBB.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["businessName", "location", "phone"])
        writer.writeheader()
        writer.writerows(data)

def main():
    x = str(input("search all businesses? (will take a long time) ")).lower().strip()
    if x[0] == 'y':
        get_content("https://www.bbb.org/search?find_country=USA&find_text=businesses") # for some reason, gets less results? maybe refactor to scrape related categories instead
    if x[0] == 'n':
        for category in categories:
            get_content(directory_url + category)
    
    writeToFile()
    print("finished with ", len(data), " businesses found")

main()