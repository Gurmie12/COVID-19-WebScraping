import bs4
import requests
import json

class my_dictionary(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value

class Stat:
    name = ''
    value = 0

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return f'StatName: {self.name} || Value: {self.value}'

def getNumber(tag):
    total = ''
    for i in tag:
        if i.isdigit():
            total = total + i
    return int(total)


# Send a request to the website to fetch data
worldometers = requests.get("https://www.worldometers.info/coronavirus/")
responseContent = worldometers.content

# Creating a beautifulSoup object and searching for all html div tags that contain this unique class and style
soupVariable = bs4.BeautifulSoup(responseContent, features="lxml")
divs = soupVariable.findAll("div", {"class": "maincounter-number"}, {"style": "color:#aaa"})

# Separating the count for the total number of cases from the remainder of letters
cases = str(divs[0])
total_cases = Stat("Total", getNumber(cases))

# Finding the total number of deaths
divs = soupVariable.findAll("div", {"class": "maincounter-number"})
cases = str(divs[1])
total_deaths = Stat("Deaths", getNumber(cases))

# Finding the total number of recovered cases
divs = soupVariable.findAll("div", {"class": "maincounter-number"})
cases = str(divs[2])
refinedCases = ''
for i in cases:
    if i.isdigit():
        refinedCases = refinedCases + i
totalRecovered = ''
for i in refinedCases[2::]:
    totalRecovered = totalRecovered + i
total_recovered = Stat("Recovered", int(totalRecovered))

divs = soupVariable.findAll("div", {"class": "number-table-main"})
cases = str(divs[0])
active_cases = Stat("activeCases", getNumber(cases))

cases = str(divs[1])
closed_cases = Stat("closedCases", getNumber(cases))

divs = soupVariable.findAll("table", {"id": "main_table_countries_today"})

stats_arr = [total_cases, total_recovered, total_deaths, active_cases, closed_cases]
stats_dict = my_dictionary()
for stat in stats_arr:
    stats_dict.add(f"{stat.name}", stat.value)

print(stats_dict)
