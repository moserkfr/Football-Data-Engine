import requests
import urllib.parse
import sys
import pandas as pd

from tabulate import tabulate
from bs4 import BeautifulSoup

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }

def query_player(player_query):

    query = urllib.parse.quote_plus(player_query)
    url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={query}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    players = []
    for link in soup.find_all('a', href=True):
        if '/profil/spieler' in link['href']:
            player_name = link.get('title')
            player_url = "https://www.transfermarkt.com" + link['href']

            row = link.find_parent('tr', class_=['odd','even'])
            club_name = ""

            if row:
                club_img = row.find('img', class_='tiny_wappen')
                if club_img:
                    club_name = club_img.get('title', club_name)

            players.append({"player_name": player_name, "club_name": club_name, "player_url": player_url})
    
    return players

def get_player_data(baller):
    url = baller['player_url']

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    played_data = {}

    info_div = soup.find('div', class_='info-table info-table--right-space')

    if info_div:
        keys = info_div.find_all('span', class_='info-table__content info-table__content--regular')

        for key_span in keys:
            key_name = key_span.text.strip().rstrip(':').strip()

            value_span = key_span.find_next_sibling('span', class_='info-table__content info-table__content--bold')
            if value_span:
                value = value_span.getText(strip=True)

                played_data[key_name] = value

    print(tabulate((played_data.items()), tablefmt='grid'))

    return

def get_stats():
    pass
def get_achievements():
    pass
def get_market_value():
    pass
def get_transfer_history():
    pass

def main():
    player_query = input("Enter the name of a football player: ")
    players = query_player(player_query)
    if not players:
        print("No results found")
        sys.exit()
    
    players_df = pd.DataFrame(players)
    players_df.index += 1
    print("Results:")
    print(tabulate(players_df[["player_name", "club_name"]], headers=["Index", "Player", "Club"], tablefmt="grid"))

    player_index = int(input("Enter the index of player: "))
    player = players_df.iloc[player_index - 1]
    
    while True:
        print("What do you want to know?")
        print("1. Player Data")
        print("2. Stats")
        print("3. Achievements")
        print("4. Market Value")
        print("5. Transfer History")
        print("6. Exit")    
        choice = int(input("Enter you choice: "))

        match choice:
            case 1:
                get_player_data(player)
            case 2:
                get_stats(player)
            case 3:
                get_achievements(player)
            case 4:
                get_market_value(player)
            case 5:
                get_transfer_history(player)
            case 6:
                break
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    main()