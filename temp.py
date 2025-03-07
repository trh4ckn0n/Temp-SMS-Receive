#!/usr/bin/env python
# coding: utf-8
# By trhacknon: https://github.com/trh4ckn0n, https://t.me/trhacknon
# Version interactive modifiée

import os
import subprocess
import random
import time
import sys
import base64
from banner import banner
from colorama import Fore, Back, Style, init

init(autoreset=True)

# Fonctions d'affichage d'avertissements et d'infos
def warn(message: str) -> None:
    print(f"\x1b[1m\x1b[31m[!] {message}".center(os.get_terminal_size().columns))

def info(message: str) -> None:
    print(f"\x1b[1m\x1b[92m[+] {message}".center(os.get_terminal_size().columns))

# Vérification des dépendances
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    import requests
    import colorama
    import pyfiglet
    import pyperclip
except ModuleNotFoundError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"])
    except subprocess.CalledProcessError:
        warn("Erreur lors de l'installation des dépendances")
        warn("Vérifiez que pip est installé et que le fichier requirements.txt est présent")
        exit()
    else:
        info("Dépendances installées")
        info("Relancez le programme")
        exit()

# Initialisation des couleurs et polices
BLU = colorama.Style.BRIGHT + colorama.Fore.BLUE
CYA = colorama.Style.BRIGHT + colorama.Fore.CYAN
GRE = colorama.Style.BRIGHT + colorama.Fore.GREEN
YEL = colorama.Style.BRIGHT + colorama.Fore.YELLOW
RED = colorama.Style.BRIGHT + colorama.Fore.RED
MAG = colorama.Style.BRIGHT + colorama.Fore.MAGENTA
LIYEL = colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX
LIRED = colorama.Style.BRIGHT + colorama.Fore.LIGHTRED_EX
LIMAG = colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX
LIBLU = colorama.Style.BRIGHT + colorama.Fore.LIGHTBLUE_EX
LICYA = colorama.Style.BRIGHT + colorama.Fore.LIGHTCYAN_EX
LIGRE = colorama.Style.BRIGHT + colorama.Fore.LIGHTGREEN_EX
BOLD = colorama.Style.BRIGHT
CLEAR = "cls" if os.name == "nt" else "clear"
COLORS = (BLU, CYA, GRE, YEL, RED, MAG, LIYEL, LIRED, LIMAG, LIBLU, LICYA, LIGRE)
# FONTS = ("basic", "o8", "cosmic", "graffiti", "chunky", "epic", "doom", "avatar")
FONTS = [
    "basic", "o8", "cosmic", "graffiti", "chunky", "epic", "doom", "avatar",
    "starwars", "block", "slant", "3x5", "lean", "mini", "puffy", "alligator",
    "dancing", "banner", "contessa", "fancy", "roman", "script", "small", "twisted"
]
colorama.init(autoreset=True)
global font
font = random.choice(FONTS)

# Affichage du logo
def logo() -> None:
    os.system(CLEAR)  # Effacer l'écran
    color1 = random.choice(COLORS)
    color2 = random.choice(COLORS)

    while color1 == color2:
        color2 = random.choice(COLORS)

    # Définir une police aléatoire
    font = random.choice(FONTS)

    # Obtenir la largeur du terminal
    term_width = os.get_terminal_size().columns

    # Affichage du séparateur supérieur
    print(color1 + "_" * term_width, end="\n\n")

    # Affichage du logo avec une police aléatoire
    banner_text = pyfiglet.figlet_format("TRHACKNON\nTemp\nSMS", font=font, justify="center")
    print(color2 + banner_text, end="")

    # Affichage du message "[+] By TRHACKNON [+]"
    msg = "[+] By TRHACKNON [+]"
    pad = (term_width - len(msg)) // 2
    print(color1 + "_" * pad + LIYEL + msg + color1 + "_" * pad + "\n")

    # Animation pour le slogan
    slogan = " 🚀 Service de réception de SMS by TRHACKNON 🚀 "
    for char in slogan:
        print(random.choice(COLORS) + char, end="", flush=True)
        time.sleep(0.05)  # Animation plus fluide
    print("\n")


# Récupération et décryptage de la clé d'authentification
def fetch_authkey() -> str:
    url = "https://api-1.online/post/"
    params = {"action": "get_encrypted_api_key", "type": "user"}
    json_data = {"api": "111"}
    rq = requests.post(url, params=params, headers={"accept-encoding": "gzip", "user-agent": "okhttp/4.9.2"}, json=json_data)
    return rq.json()["api_key"]

def decrypt_key(encrypted_str: str) -> str:
    decoded = base64.b64decode(encrypted_str)
    iv = decoded[:16]
    encrypted_data = decoded[16:]
    cipher = AES.new("9e8986a75ffa32aa187b7f34394c70ea".encode(), AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode()

AUTH_KEY = decrypt_key(fetch_authkey())

# Copier dans le presse-papier
def copy_clipboard(text: str) -> tuple:
    """Codes d'erreur:
       1: termux api de apt non installé
       2: app termux api non installée
       3: environnement non termux"""
    try:
        pyperclip.copy(text)
    except Exception:
        try:
            if subprocess.check_output(["uname", "-o"]).strip() == b"Android":
                try:
                    if subprocess.call(["termux-clipboard-set", text], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, timeout=4) == 0:
                        return True, None
                except FileNotFoundError:
                    return False, 'Échec du copie-presse-papier ! Installez termux-api ("apt install termux-api")'
                except subprocess.TimeoutExpired:
                    return False, 'Échec du copie-presse-papier ! Installez l\'application termux-api'
        except FileNotFoundError:
            return False, "Échec du copie-presse-papier ! Environnement inconnu"
    else:
        return True, None

# Récupérer la liste des pays
def fetch_countries() -> list:
    url = "https://api-1.online/get/"
    params = {"action": "country"}
    return requests.post(url, params=params, headers={"accept-encoding": "gzip", "user-agent": "okhttp/4.9.2"}).json()["records"]

# Récupérer les numéros pour un pays et une page donnée
def fetch_numbers(country: str, page: int) -> dict:
    url = "https://api-1.online/post/"
    params = {"action": "GetFreeNumbers", "type": "user"}
    headers = {"accept-encoding": "gzip", "user-agent": "okhttp/4.9.2", "authorization": "Bearer " + AUTH_KEY}
    json_data = {"country_name": country, "limit": 10, "page": page}
    return requests.post(url, params=params, headers=headers, json=json_data).json()

# Récupérer les SMS pour un numéro
def fetch_sms(number: str) -> list:
    url = "https://api-1.online/post/getFreeMessages"
    json_data = {"no": number, "page": "1"}
    headers = {"accept-encoding": "gzip", "user-agent": "okhttp/4.9.2", "authorization": "Bearer " + AUTH_KEY}
    return requests.post(url, headers=headers, json=json_data).json()["messages"]

def print_sms(number: str) -> None:
    sms_list = fetch_sms(number)
    for sms in sms_list:
        print(f"{random.choice(COLORS)}{sms['FromNumber']} {repr(sms['Messagebody'])} {sms['message_time']}")
        print("_" * os.get_terminal_size().columns)

# Vérifier et appliquer une mise à jour
def check_update() -> tuple:
    latest = requests.get("https://raw.githubusercontent.com/trh4ckn0n/Temp-SMS-Receive/main/.version").text.strip()
    try:
        with open(".version", "r") as version_file:
            current = version_file.read().strip()
    except FileNotFoundError:
        current = "0"
    if current != latest:
        return True, latest
    else:
        return False, "0"

def update():
    if ".git" in os.listdir():
        subprocess.run(["git", "stash"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "pull"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Variables globales pour l'état
selected_country = None
country_list = []
list_numbers = []
selected_number = None

# Menu interactif principal
def main_menu():
    global selected_country, country_list, list_numbers, selected_number
    while True:
        color1 = random.choice(COLORS)
        color2 = random.choice(COLORS)
        color3 = random.choice(COLORS)
        logo()
        print(BOLD + color1 + "\n=== Menu Principal ===".center(os.get_terminal_size().columns))
        print(BOLD + "[1] Afficher la liste des pays")
        print(BOLD + color2 + "[2] Sélectionner un pays")
        print(BOLD + "[3] Récupérer les numéros disponibles")
        print(BOLD + color3 + "[4] Sélectionner un numéro (ou aléatoire)")
        print(BOLD + "[5] Afficher les SMS du numéro sélectionné")
        print(BOLD + color1 + "[6] Copier le numéro sélectionné dans le presse-papier")
        print(BOLD + "[7] Rafraîchir (Retour au menu principal)")
        print(BOLD + color2 + "[8] Quitter")
        choice = input(BOLD + "\nEntrez votre choix : ").strip()

        if choice == "1":
            # Afficher les pays
            country_list = fetch_countries()
            print("\nListe des pays disponibles :")
            for idx, c in enumerate(country_list, start=1):
                print(f"{idx}. {c['country_code']} - {c['Country_Name']}".center(os.get_terminal_size().columns))
            input(BOLD + "\nAppuyez sur <Entrée> pour revenir au menu...")
        elif choice == "2":
            # Sélectionner un pays
            if not country_list:
                country_list = fetch_countries()
            try:
                sel = int(input(BOLD + "\nEntrez le numéro du pays désiré : "))
                if sel < 1 or sel > len(country_list):
                    warn("Choix incorrect")
                    time.sleep(1)
                else:
                    selected_country = country_list[sel - 1]["Country_Name"]
                    info(f"Pays sélectionné : {selected_country}")
                    time.sleep(1)
            except ValueError:
                warn("Entrée invalide")
                time.sleep(1)
        elif choice == "3":
            # Récupérer les numéros pour le pays sélectionné
            if not selected_country:
                warn("Veuillez sélectionner un pays d'abord")
                time.sleep(1)
            else:
                list_numbers = []
                page_data = fetch_numbers(selected_country, 1)
                list_numbers.extend(page_data["Available_numbers"])
                total_pages = page_data["Total_Pages"]
                if total_pages == 0:
                    warn("Aucun numéro disponible pour ce pays")
                    time.sleep(1)
                else:
                    for i in range(2, total_pages + 1):
                        list_numbers.extend(fetch_numbers(selected_country, i)["Available_numbers"])
                        if len(list_numbers) > 149:
                            break
                    info(f"{len(list_numbers)} numéros récupérés")
                    # Affichage de quelques numéros
                    for idx, num in enumerate(list_numbers[:10], start=1):
                        print(f"{idx}. {num['E.164']} ({num['time']})".center(os.get_terminal_size().columns))
                    input(BOLD + "\nAppuyez sur <Entrée> pour revenir au menu...")
        elif choice == "4":
            # Sélectionner un numéro
            if not list_numbers:
                warn("Aucun numéro récupéré. Récupérez d'abord les numéros.")
                time.sleep(1)
            else:
                choix = input(BOLD + 'Entrez le numéro désiré (ou "R" pour aléatoire) : ').strip()
                if choix.upper() == "R":
                    # Sélection aléatoire pondérée : 20% de chance pour les 20% premiers
                    per = int(len(list_numbers) * 0.2)
                    weights = [2] * per + [1] * (len(list_numbers) - per)
                    selected_number = random.choices(list_numbers, weights=weights, k=1)[0]["E.164"]
                    info(f"Numéro sélectionné aléatoirement : {selected_number}")
                else:
                    try:
                        idx = int(choix)
                        if idx < 1 or idx > len(list_numbers):
                            warn("Choix incorrect")
                        else:
                            selected_number = list_numbers[idx - 1]["E.164"]
                            info(f"Numéro sélectionné : {selected_number}")
                    except ValueError:
                        warn("Entrée invalide")
                time.sleep(1)
        elif choice == "5":
            # Afficher les SMS du numéro sélectionné
            if not selected_number:
                warn("Aucun numéro sélectionné")
                time.sleep(1)
            else:
                print(f"\nSMS pour le numéro : {selected_number}".center(os.get_terminal_size().columns))
                print_sms(selected_number)
                input(BOLD + "\nAppuyez sur <Entrée> pour rafraîchir ou revenir au menu...")
        elif choice == "6":
            # Copier le numéro sélectionné dans le presse-papier
            if not selected_number:
                warn("Aucun numéro sélectionné")
                time.sleep(1)
            else:
                result, msg = copy_clipboard(selected_number)
                if result:
                    info("Numéro copié dans le presse-papier")
                else:
                    warn(msg)
                time.sleep(1)
        elif choice == "7":
            # Rafraîchir : réafficher le menu
            continue
        elif choice == "8":
            info("Merci d'avoir utilisé Temp SMS. stay free in your mind")
            exit(0)
        else:
            warn("Choix invalide")
            time.sleep(1)

def main():
    try:
        # Vérification de mise à jour
        update_available, latest = check_update()
        if update_available:
            warn("Mise à jour disponible")
            info("Mise à jour en cours...")
            update()
            info("Mise à jour réussie. Relancez le programme.")
            exit()
        # Lancer le menu interactif
        main_menu()
    except KeyboardInterrupt:
        info("Arrêt du programme.")
        exit()

if __name__ == "__main__":
    main()
