import requests

from bs4 import BeautifulSoup

city = input("enter city name: ")
country = input("enter conutry name: ")

city_formatted = city.lower().replace(" ", "")
country_formatted = country.lower().replace(" ", "")

url = f"https://www.timeanddate.com/weather/{country_formatted}/{city_formatted}"


response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

try:
    temperature = soup.find("div", class_ = "h2").get_text(strip=True)
    description = soup.find("div", class_ = "h2").find_next("p").get_text(strip=True)

    print(f"Weather in {city}:")
    print(f"Temperature: {temperature}")
    print(f"Condition: {description}")

except AttributeError:
    print("Please check the city name and try again!")