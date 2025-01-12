import requests

url = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"

querystring = {"query":"Astana"}

headers = {
  "x-rapidapi-key": "23276084b7mshee88925dd871d45p10ed7fjsn3cadfccc067c",
  "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
}
from_city = input("Enter from city: ")
to_city = input("Enter to city: ")
depart_date = input("Enter data in YYYY-MM-DD format with dashes(-): ")

response = requests.get(url, headers=headers, params={"query": from_city})
from_city_code = response.json()['data'][0]['presentation']['skyId']

response2 = requests.get(url, headers=headers, params={"query": to_city})
to_city_code = response2.json()['data'][0]['presentation']['skyId']


one_way_url = "https://sky-scanner3.p.rapidapi.com/flights/cheapest-one-way"

payload = {
  "fromEntityId": from_city_code,
  "toEntityId": to_city_code,
  "departDate": depart_date,
  "currency": "KZT"
}
response3 = requests.get(one_way_url, headers=headers, params=payload)
get_first_five = response3.json()['data'][:5]
counter = 1
for res in get_first_five:
  print(f"{counter}. Date: {res['day']}; Price: {res['price']}KZT")
  counter+=1