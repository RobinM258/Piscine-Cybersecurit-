
import requests
import os
import time
from bs4 import BeautifulSoup 
from pathlib import Path
import sys
from urllib.parse import urljoin


dir_name = "data/"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
def GetPage(Url):
    try:
        response = requests.get(Url, headers=headers, timeout=5)
        return response.text
    except requests.exceptions.RequestException as e:    
        print(f"La requête vers l'url donné n'as pas fonctionné.\n Code d'erreur {e}")

def CheckExtexion(Url):
    extention = os.path.splitext(Url)
    if (extention[1] == ".jpg" or extention[1] == ".jpeg" or extention[1] == ".png" or extention[1] == ".gif"  or extention[1] == ".bmp" ):
        return True
    else:
        return False
    
def DlimgFromLink(soup):
    global dir_name
    for link in soup.find_all('img'):
        File_name = dir_name + Path(link.get('src')).name
        if (CheckExtexion(Path(link.get('src')).name) == True):
            try:
                ##print(f"Tentative de connexion sur {File_name}")
                response = requests.get(link.get('src'), headers=headers, timeout=5)
                with open(File_name, "wb") as file:
                    file.write(response.content)
            except requests.exceptions.RequestException as e:    
                print(f"La requête vers l'url donné n'as pas fonctionné.\n Code d'erreur {e}")
                continue;

def Core(Url, recursion):
    Example = "https"
    soup = BeautifulSoup (GetPage(Url), 'html.parser')
    DlimgFromLink(soup)
    if (recursion > 1):
        for link in soup.find_all('a'):
            href = urljoin(Example, str(link.get('href')))
            print(href)
            ##href = str(link.get('href'))
            if GetPage(href) != None:
                print("J'ouvre la page ", href, "recursion ", recursion - 1)
                Core(href, recursion - 1)
            else:
                print ("lien nul ", href)
    

def main(Url):
    recursion = 1
    global dir_name
    for i in range(len(sys.argv)):
        if (sys.argv[i] == "-p"):
            dir_name = sys.argv[i + 1]
        if (sys.argv[i] == "-r"):
            if sys.argv[i + 1] == "-l":
                recursion = int(sys.argv[i + 2] )
            else:
                recursion = 5
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    Core(Url, recursion)

if len(sys.argv) < 2:
    print("Please use: ./spider [-rlp] URL")

URL = sys.argv[len(sys.argv) - 1]
main(URL)
