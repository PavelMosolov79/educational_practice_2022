import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import PySimpleGUI as sg
import os
import csv

FILE_NAME = "currencies22.csv"
SITE_URL   = "https://coinmarketcap.com"

names_crypto = []
market_cap_crypto_long = []
price_crypto = []
struct_crypto = []


def merge_information():
    for i in range(len(names_crypto)):
        struct = {
            "name": names_crypto[i],
            "market_cap": market_cap_crypto_long[i],
            "price": price_crypto[i]
        }
        struct_crypto.append(struct)


def mass_clear():
    names_crypto.clear()
    price_crypto.clear()
    market_cap_crypto_long.clear()
    struct_crypto.clear()


def find_name_crypto(crypto_information_list):
    crypto_information_list_statistics = crypto_information_list.find_all('p', class_='sc-1eb5slv-0 iworPT')
    for crypto_information in crypto_information_list_statistics:
        names_crypto.append(str(crypto_information.contents[0].text))


def find_market_cap_crypto(crypto_information_list):
    crypto_information_list_statistics = crypto_information_list.find_all('span', class_='sc-1ow4cwt-1 ieFnWP')
    for crypto_information in crypto_information_list_statistics:
        market_cap_crypto_long.append(crypto_information.contents[0].text)


def find_price_crypto(crypto_information_list):
    crypto_information_list_statistics = crypto_information_list.find_all('div', class_='sc-131di3y-0 cLgOOr')
    for crypto_information in crypto_information_list_statistics:
        price_crypto.append(crypto_information.contents[0].text)


def terminal_table_output(length):
    Table_crypto = PrettyTable()
    Table_crypto.field_names = ["№","Name","Price","Marcet Cap"]
    for i in range(length):
        Table_crypto.add_row([i+1,names_crypto[i], price_crypto[i], market_cap_crypto_long[i]])
    print(Table_crypto)


def searching_element_array():
    Table_crypto = PrettyTable()
    Table_crypto.field_names = ["№","Name","Price","Marcet Cap"]
    myLetter = str(input("Enter the search key: "))
    i =0
    for word in names_crypto:
        if myLetter.lower() in word.lower():
            i = names_crypto.index(word)
            Table_crypto.add_row([i+1,names_crypto[i], price_crypto[i], market_cap_crypto_long[i]])
    if i == 0:
        print("Eror, invalid key, try again\n")
    else:
        print(Table_crypto)
    

def Pulling_information_site():
    try:
        page = requests.get(SITE_URL)
        soup = BeautifulSoup(page.text, 'html.parser')
        crypto_information_list = soup.find('tbody')

        find_name_crypto(crypto_information_list)
        find_market_cap_crypto(crypto_information_list)
        find_price_crypto(crypto_information_list)
    except(ConnectionError, Timeout) as exp:
        print("Mistake! The reason for the error: ", exp)
        sys.exit(1)


def parsing_csv():
    try:
        with open(FILE_NAME, encoding='utf-8') as file:
            file_reader = csv.reader(file, delimiter = ";")
            count = 0
            for row in file_reader:
                names_crypto.append(f'{row[0]}')
                price_crypto.append(f'{row[1]}')
                market_cap_crypto_long.append(f'{row[2]}')
    except FileNotFound:
        print("Mistake! The file '{}' could not be opened. Check the correctness of the name, or the presence of it in the pope.".format(FILE_NAME))
        sys.exit(1)


def create_data():
    new_struct_crypto = []

    for i in struct_crypto:
        new_struct_crypto.append([i["name"], i["market_cap"], i["price"]])

    return new_struct_crypto


def gui_pars():
    sg.theme("DarkPurple")
    
 

    head = ["Name of the cryptocurrency", "   Marcet Cap   ", "Cost in dollars"]
    frame_1 = [
        [sg.Text("Select the data output mode:")],
        [sg.Button("1. FILE '{}'.".format(FILE_NAME))],
        [sg.Button("2. WEBSITE '{}'.".format(SITE_URL))],
        [sg.Text("Information:")],
        [sg.Table(values=struct_crypto, headings=head, key="TABLE", size=(500, 420))]]
   
    layout = [[sg.Column(frame_1)]]

    sg.set_options(font=("Courier New", 10))
    
    window = sg.Window("Parser", layout, size=(690, 620))
    
    gui = []
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "1. FILE 'currencies22.csv'.":
            mass_clear()
            
            parsing_csv()
            merge_information()

            gui = create_data()
        if event == "2. WEBSITE 'https://coinmarketcap.com'.":
            mass_clear()

            Pulling_information_site()
            merge_information()
            
            gui = create_data()
        window["TABLE"].update(values=gui)

    window.close()


def UI():
    os.system('cls')
    flag = 1
    flag_two = 1
    while flag == 1:
        mass_clear()
        mode = 0
        mode = input("Select the output method ('T' from terminal, 'G' using graphics,'E' - end): ")
        if mode == 'T':
            flag_two = 1
            mass_clear()
            while flag_two == 1:
                mode2 = input("Choose the parsing method ('F' from file, 'S' from the site, 'Q' - end): ")
                if mode2 == 'S':
                    mass_clear()
                    os.system('cls')
                    Pulling_information_site()
                    terminal_table_output(len(names_crypto))
                    searching_element_array()
                elif mode2 == 'F':
                    mass_clear()
                    os.system('cls')
                    parsing_csv()
                    terminal_table_output(len(names_crypto))
                    searching_element_array()
                elif mode2 == 'Q':
                    flag_two = 2
                else:
                    os.system('cls')
                    print("Invalid argument")
        elif mode == 'G':
            mass_clear()
            os.system('cls')
            gui_pars()
        elif mode == 'E':
            flag = 2
        else:
            os.system('cls')
            print("Invalid argument")
    os.system('cls') 

            
def main():
    UI()  

            
if __name__ == '__main__':
    main()
