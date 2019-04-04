from bs4 import BeautifulSoup
from pprint import pprint
import json
import os
import requests
from selenium import webdriver

if os.path.isfile("zomato.json"):
    with open("zomato.json","r+") as data:
        file=json.load(data)
        pprint(file)
else:
    driver = webdriver.Chrome()
    driver.get('https://www.zomato.com/ncr')
    page = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    # task-1
    soup = BeautifulSoup(page,"html.parser")
    div_1 = soup.find("div",class_="ui segment row")
    a_tag =  div_1.find_all("a")

    list_for_links = []
    for i in a_tag:
        link=(i['href'])
        list_for_links.append(link)

    num=0
    for i in a_tag:
        num+=1
        s=i.find("span").get_text()
        sli=s[1:-1]

        link=(i.get_text().strip())
        a=""
        for k in link:
            if  k == "(":
                break
            else:
                a+=k
        print(str(num)+"."+" ", a)
        print("      total restaurants =>  " ,sli)

    # task-2

    user=int(input("Enter a number "))
    output_link = list_for_links[user-1]
    print(output_link)

    driver = webdriver.Chrome()
    driver.get(output_link)
    page = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    soup = BeautifulSoup(page,"html.parser")

    div_a = soup.find_all("a",class_="zred")

    restaurant_detail = []
    list_for_rating=[]
    list_for_views=[]
    list_for_resto=[]
    list_for_locality=[]
    list_for_range=[]
    for i in div_a:
        driver = webdriver.Chrome()
        driver.get(i['href'])
        page = driver.execute_script("return document.documentElement.outerHTML")
        driver.quit()
        soup = BeautifulSoup(page,"html.parser")

        var = soup.find_all("div",class_="col-s-12")
        for j in var:
            name=j.find_all("a")
            name_1=(name[-2].text.split('\n')[0])
            list_for_resto.append(name_1)
            local=(name[-1].text)
            list_for_locality.append(local)
        sp=soup.find_all("div",class_="res-cost clearfix")
        for k in sp:
            range=k.find("span",class_="col-s-11 col-m-12 pl0").text
            list_for_range.append(range)
        rating=soup.findAll("div",class_="ta-right floating search_result_rating col-s-4 clearfix")
        for x in rating:
            voting=x.find("span")
            r=x.find("div")
            if type(r)!=type(None):
                r1=(r.text).strip()
                list_for_rating.append(r1)
            else:
                list_for_rating.append('0.0')
            if type(voting)!=type(None):
                v=(voting.text)
                list_for_views.append(v)
            else:
                list_for_views.append('0 votes')

    i=1
    count=0
    while i<len(list_for_resto):
        count+=1
        detail = {}
        detail['name'] = list_for_resto[i]
        detail['id']=count
        detail['localilty'] = list_for_locality[i]
        detail['reating'] = list_for_rating[i]
        detail['review'] = list_for_views[i]
        detail['range']=list_for_range[i]
        restaurant_detail.append(detail)
        i+=1
    # pprint(restaurant_detail)
    with open("zomato.json","w")as data:
        json.dump(restaurant_detail,data)
