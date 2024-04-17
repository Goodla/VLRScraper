import requests
from bs4 import BeautifulSoup
import re
import csv

api_url = "https://vlrggapi.vercel.app/match/results"
match_url = ""

# Send GET request to the API endpoint
response = requests.get(api_url)

# Check if request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the URL of the match
    match_url = "https://vlr.gg" + data['data']['segments'][0]['match_page']

    print("URL of the match:", match_url)
else:
    print("Error:", response.status_code)

match = requests.get(match_url)

start = match_url.find(".gg/")
slash = match_url.find('/', start + 4)
soup = BeautifulSoup(match.content, 'html.parser')
matchID = match_url[start + 4:slash]
print("MatchID: " + matchID)

result = []

wrapper = soup.find(id='wrapper')
colMod = wrapper.find("div", {"class": "col mod-3"})
card = colMod.find("div", {"class": "wf-card", "style": "overflow: visible;"})

vmStats = card.find("div", {"class": "vm-stats"})
vmClassContainer = vmStats.find("div", {"class": "vm-stats-container"})
tables = vmClassContainer.find("div", {
    "class": "vm-stats-game mod-active"
}).findAll("table", {"class": "wf-table-inset mod-overview"})

for i in range(0, 2):
    table = tables[i]

    tbody = table.find("tbody")

    for i in tbody.findAll("tr"):
        player = i.find("td", {
            "class": "mod-player"
        }).find("div", {
            "class": "text-of"
        }).text
        stats = i.findAll("td", {"class": "mod-stat"})

        rating = stats[0].find("span", {
            "class": "side mod-side mod-both"
        }).text
        acs = stats[1].find("span", {"class": "side mod-side mod-both"}).text
        kills = stats[2].find("span", {"class": "side mod-side mod-both"}).text
        assists = stats[3].find("span", {"class": "side mod-both"}).text
        deaths = stats[4].find("span", {"class": "side mod-both"}).text

        KDDiff = stats[5].find("span").find("span").text

        kast = stats[6].find("span", {"class": "side mod-both"}).text
        adr = stats[7].find("span", {"class": "side mod-both"}).text
        hs = stats[8].find("span", {"class": "side mod-both"}).text
        fk = stats[9].find("span", {"class": "side mod-both"}).text
        fd = stats[10].find("span", {"class": "side mod-both"}).text

        FKFDDiff = stats[11].find("span").find("span").text

        result.append({
            "player": player.strip(),
            "rating": rating,
            "acs": acs,
            "kills": kills,
            "assists": assists,
            "deaths": deaths,
            "KAST": kast,
            "ADR": adr,
            "hs": hs,
            "fk": fk,
            "fd": fd,
            "FKFDDiff": FKFDDiff
        })

match_url = match_url + "/?game=all&tab=performance"

match = requests.get(match_url)
soup = BeautifulSoup(match.content, 'html.parser')

wrapper = soup.find(id='wrapper')

colMod = wrapper.find("div", {"class": "col mod-3"})

card = colMod.find("div", {"style": "overflow: visible;"})

vmstats = card.find("div", {"class": "vm-stats"})

contain = vmstats.find("div", {"class": "vm-stats-container"})

stats = contain.find("div", {"class": "vm-stats-game mod-active"})

tables = stats.findAll("table", {"class": "wf-table-inset mod-adv-stats"})
table = tables[0]

trs = table.findAll("tr")

for i in range(1, len(trs)):
    tr = trs[i]

    tds = tr.findAll("td")
    player = tds[0].text.strip()[:13].strip()

    twoK = tds[2].text.strip()
    threeK = tds[3].text.strip()
    fourK = tds[4].text.strip()
    fiveK = tds[5].text.strip()
    oneVOne = tds[6].text.strip()
    oneVTwo = tds[7].text.strip()
    oneVThree = tds[8].text.strip()
    oneVFour = tds[9].text.strip()
    oneVFive = tds[10].text.strip()
    econ = tds[11].text.strip()
    plants = tds[12].text.strip()
    defuses = tds[13].text.strip()

    if twoK == "":
        twoK = 0
    if threeK == "":
        threeK = 0
    if fourK == "":
        fourK = 0
    if fiveK == "":
        fiveK = 0
    if oneVOne == "":
        oneVOne = 0
    if oneVTwo == "":
        oneVTwo = 0
    if oneVThree == "":
        oneVThree = 0
    if oneVFour == "":
        oneVFour = 0
    if oneVFive == "":
        oneVFive = 0

    for i in range(len(result)):
        if result[i]['player'] == player:
            result[i].update({
                "2ks": twoK,
                "3ks": threeK,
                "4ks": fourK,
                "5ks": fiveK,
                "1v1s": oneVOne,
                "1v2s": oneVTwo,
                "1v3s": oneVThree,
                "1v4s": oneVFour,
                "1v5s": oneVFive,
                "econ": econ,
                "plants": plants,
                "defuses": defuses
            })

print(result)
