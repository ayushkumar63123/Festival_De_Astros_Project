import urllib
import urllib.request
import urllib.parse
import os
import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from gtts import gTTS
from playsound import playsound

def speak(text, filename):
    tts = gTTS(text, lang = 'en')
    filename = filename + '.mp3'
    tts.save(filename)
    playsound(filename)

print("Welcome to AK Commerce Platform! Wishing you a happy and reliable shopping.")
speak("Welcome to AK Commerce Platform! Wishing you a happy and reliable shopping.", '111')

flipkart_df = pd.read_csv("flipkart_data.csv")

def sendSMS(number, message):
    import requests

    url = "https://sms77io.p.rapidapi.com/sms"

    payload = "to={}&p=IN8ZlzzM6QJpcbhEwOCP5qc8mV5E8KFDuLnGijL3CdUqmBKgQFQDf6FsuEfBWAJ8&text={}".format(number, message)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "c9a50d71bbmsh986ce6928856767p1381e8jsn95185302faab",
        'x-rapidapi-host': "sms77io.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def amazon_search(asin):
    import requests

    url = "https://amazon-product4.p.rapidapi.com/product/reviews"

    querystring = {"asin": asin}

    headers = {
        'x-rapidapi-key': "c9a50d71bbmsh986ce6928856767p1381e8jsn95185302faab",
        'x-rapidapi-host': "amazon-product4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    text = response.text

    print(text)

def barcode_comparison(barcode):
    import requests

    url = "https://ebay-com.p.rapidapi.com/products/" + barcode

    headers = {
        'x-rapidapi-key': "c9a50d71bbmsh986ce6928856767p1381e8jsn95185302faab",
        'x-rapidapi-host': "ebay-com.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    text = response.text

    print(text)

speak('''
Press 1 to see product reviews and prices across online stores like Amazon and Ebay
Press 2 to see live deals and coupons across various shopping platforms
Press 3 to contact retail services or shop owners
Press 4 to contact for techinal issues
Press 5 to explore Amazon Prime Movies
''', '112')

command1 = int(input('''
Press 1 to see product reviews across online stores like Amazon and Ebay
Press 2 to see live deals and coupons across various shopping platforms
Press 3 to contact retail services or shop owners
Press 4 to contact for techinal issues
Press 5 to explore Amazon Prime Movies
'''))

if command1 == 1:
    speak("Please enter the preferred store number (amazon reviews - 1, multistore comparison - 2, flipkart indian store prices - 3) ", '113')
    store = int(input("Please enter the preferred store number (amazon - 1, multistore comparison - 2, flipkart indian store - 3) "))

    if store == 1:
        speak("Search for an item via asin", '114')
        asin = input("Search for an item via asin....")

        amazon_search(asin)

    elif store == 2:
        speak("Please enter the barcode", '115')
        barcode = input("Please enter the barcode....")

        barcode_comparison(barcode)

    elif store == 3:
        print("Below are some of the product examples in table format: ")
        speak("Below are some of the product examples in table format", '116')
        print(flipkart_df.head())

        speak("Please enter the unique id of the product offered by the flipkart indian store", '118')
        id1 = input("Please enter the unique id of the product offered by the flipkart indian store: ")

        hello1 = []

        for i in flipkart_df["uniq_id"]:
            hello1.append(str(i))

        if id1 in hello1:
            print("Id found")
            speak("Id found", '1001')

            id1_index = list(flipkart_df["uniq_id"]).index(id1)

            original_price = flipkart_df["retail_price"][id1_index]
            discounted_price = flipkart_df["discounted_price"][id1_index]

            print("Original Price is ", original_price)
            print("Discounted Price is ", discounted_price)

            speak("Original Price is " + str(original_price), '119')
            speak("Discounted Price is " + str(discounted_price), '120')

            speak("Do you wish to visit the page url? Press small y for yes and small n for no", '121')
            decision1 = input("Do you wish to visit the page url?(y/n) ")

            if decision1 == "y":
                driver = webdriver.Chrome("chromedriver")
                driver.get(flipkart_df["product_url"][id1_index])

            elif decision1 == "n":
                print("Thanks for using our app!")
                speak("THanks for using our app!", '122')
                input("Press any key to exit.")
                speak("PRess any key to exit", '123')

                sys.exit()

        else:
            print("Id not found")
            print("System exiting....Open again........")
            speak("Id not found", '124')
            speak("System exiting Open again", '125')

            sys.exit()

if command1 == 2:
    store_name = input("Please enter the store name you want to get coupons/deals for: ")

    def site_automation1(url):
        driver = webdriver.Chrome("chromedriver")

        driver.get(url)

        target = driver.find_element_by_name("q")

        target.clear()
        target.send_keys(store_name)
        target.send_keys(Keys.ENTER)

    site_automation1("https://couponfollow.com/site")

    confirmation = input("Did this work? (y/n): ")

    if confirmation == "y":
        print("Thank you for using our app!")

    elif confirmation == "n":
        driver = webdriver.Chrome("C:/Users/capta/Documents/chromedriver")
        driver.get("https://www.grabon.in/")

if command1 == 3:
    area = input("Please enter your area (us, uk, india): ")
    keyword = input("Please enter your search keyword: ")

    if area.lower() == "us":
        driver = webdriver.Chrome("C:/Users/capta/Documents/chromedriver")
        driver.get("https://www.justdial.com/us/")

        target = driver.find_element_by_id("srchbox")

        target.clear()
        target.send_keys(keyword)
        target.send_keys(Keys.ENTER)

        number = input("Please copy and paste the number you want to send sms to (along with the country code without '+'): ")
        name = input("Please enter your name: ")
        message = input("Please enter your message to the retailer: ")

        resp = sendSMS(number, "Sent by: " + name + "\n" + message)
        print(resp)

if command1 == 5:
    movies_df = pd.read_csv("movies_data.csv")

    x = movies_df["IMDb"]
    y = movies_df["Prime Video"]

    plt.xlabel("IMDb Rating")
    plt.ylabel("Availability on Prime Video")
    plt.bar(x, y, color = 'pink')
    plt.show()

    print("The plot shows the usual relation between IMDb rating of movies and the availability of the respective movies on Prime Video.")

    command2 = int(input("Press 1 to get random lists of movies available on Prime Video\nPress 2 to search for a movie's Rating via its id\nPress 3 to visit Prime Video's website"))

    if command2 == 1:
        list1 = movies_df["Title"]

        for i in range(5):
            print(random.choice(list1))

    if command2 == 3:
        driver = webdriver.Chrome("C:/Users/capta/Documents/chromedriver")
        driver.get("https://www.amazon.com/Amazon-Video/b/?&node=2858778011&ref=dvm_MLP_ROWNA_US_1")

    if command2 == 2:
        print("Feature under Development.")