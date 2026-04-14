
import requests
import os
from bs4 import BeautifulSoup 
from pathlib import Path
import sys


dir_name = "data/"
lst_ = []


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
def GetPage(Url):
    try:
        response = requests.get(Url, headers=headers, timeout=5)
        return response.text
    except requests.exceptions.RequestException as e:    
        print(f"La requête vers l'url donné n'as pas fonctionné.\n Code d'erreur {e}")
        return None

def CheckExtexion(Url):
    extention = os.path.splitext(Url)
    if (extention[1] == ".jpg" or extention[1] == ".jpeg" or extention[1] == ".png" or extention[1] == ".gif"  or extention[1] == ".bmp" ):
        return True
    else:
        return False
    
def CheckLst(Url):
    global lst_
    for link in lst_:
        if (link == Url):
            return False
    return True

def PrintLst():
    global lst_
    print("-------------------------------")
    for link in lst_:
        print(link)
    print("-------------------------------")
    
def DlimgFromLink(soup):
    global dir_name
    forbidden_chars = "?&%=$"
    for link in soup.find_all('img'):
        src = link.get('src')
        if (src != None):
            File_name = dir_name + Path(link.get('src')).name
            for char in forbidden_chars:
                File_name = File_name.replace(char, "_")
            if (CheckExtexion(Path(link.get('src')).name) == True):
                try:
                    response = requests.get(link.get('src'), headers=headers, timeout=5)
                    with open(File_name, "wb") as file:
                        file.write(response.content)
                except requests.exceptions.RequestException as e:    
                    continue;

def Core(Url, recursion):
    global lst_
    if GetPage(Url) == None:
        return
    soup = BeautifulSoup (GetPage(Url), 'html.parser')
    DlimgFromLink(soup)
    print(recursion, Url)
    if (recursion > 1):
        for link in soup.find_all('a'):
            href = str(link.get('href'))

            if href.startswith(('http://', 'https://')):
                if GetPage(href) != None and recursion > 1 and CheckLst(href) == True:
                    lst_.append(href)
                    Core(href, recursion - 1)
    
def main(Url):
    recursion = 1
    global dir_name
    global lst_
    for i in range(len(sys.argv)):
        if (sys.argv[i] == "-p" and len(sys.argv) > i + 1):
            dir_name = sys.argv[i + 1]
        if (sys.argv[i] == "-r" and len(sys.argv) > i + 1):
            if len(sys.argv) > i + 1 and sys.argv[i + 1] == "-l":
                recursion = int(sys.argv[i + 2] )
            else:
                recursion = 5
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    lst_.append(Url)
    Core(Url, recursion)

if len(sys.argv) < 2:
    print("Please use: ./spider [-rlp] URL")
    sys.exit(1)

URL = sys.argv[len(sys.argv) - 1]
main(URL)
PrintLst()
