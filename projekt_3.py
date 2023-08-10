"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

autor: Lucie Ihnatoliová
email: lih48279@gmail.com
discord: Lucie I#2395
"""

import argparse
import requests
from bs4 import BeautifulSoup
import csv
import sys


def fetch_html_content(url):
    """
    Fetches HTML content from the specified URL and returns it as a string.
    
    Raises:Exception: If the request to the URL fails or returns a non-200 status code.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch HTML content from {url}. Status code: {response.status_code}")

def extract_main_page_data(soup):
    """
    Extracts the data from the main page: code and location, href address to each location detail.

    Returns: list: A list of dictionaries
    """
    data_list = []  
    tables = soup.find_all("table", {"class": "table"})
    for table_tag_top in tables:
        all_tr = table_tag_top.find_all("tr")
        for tr in all_tr[2:]:
            td_on_row = tr.find_all("td")
            if len(td_on_row) >= 2:
                location_code = td_on_row[0].get_text()  
                location_name = td_on_row[1].get_text()  
                a_tag = td_on_row[0].find("a")
                if a_tag:
                    href = a_tag.get("href")
                    if href:
                        modified_href = "https://volby.cz/pls/ps2017nss/" + href
                data1 = {
                    "code": location_code,
                    "location": location_name,
                    "href_to_detail_page": modified_href
                }
                if not data1["location"].startswith("-"):
                    data_list.append(data1)
    return data_list

def parse_summary_table(first_table):
    """
    Parses the data from location detail page: registered, envelopes and valid votes. Returns a dic.
    """
    all_tr_first = first_table.find_all("tr")
    for tr in all_tr_first[1:]: 
        td_on_row = tr.find_all("td")
        if len(td_on_row) >= 8:
            registered = td_on_row[3].get_text() 
            envelopes = td_on_row[4].get_text() 
            valid = td_on_row[7].get_text() 
            parsed_data = {
                "registered": registered,
                "envelopes": envelopes,
                "valid": valid
            }
    return parsed_data

def parse_detailed_results_table(second_table):
    """
    Parses the data from location detail page: political party and number of voters. Returns a dic.
    """
    parsed_data = {}
    all_tr_second = second_table.find_all("tr")
    for tr in all_tr_second[1:]:  
        td_on_row2 = tr.find_all("td")
        if len(td_on_row2) >= 3: 
            party = td_on_row2[1].get_text() 
            party_votes = td_on_row2[2].get_text() 
            parsed_data[party] = party_votes        
    return parsed_data

def get_party_name(detail_tables):
    """
    Gets parties' names as a list. 
    """
    party_names = []
    for detail_table in detail_tables:
        all_tr_second = detail_table.find_all("tr")
        for tr in all_tr_second[1:]:  
            td_on_row2 = tr.find_all("td")
            if len(td_on_row2) >= 3: 
                party = td_on_row2[1].get_text() #party
                party_names.append(party)
    return party_names

def extract_summary_table(response):
    """
    Extracts data from detail location page as a table:registered, envelopes and valid votes. 
    """
    soup = BeautifulSoup(response, "html.parser")
    first_table = soup.find("table", {"id": "ps311_t1"})
    return first_table

def extract_detail_tables(response):
    """
    Extracts data from detail location page: party and party's votes.
    """
    tables = []
    soup = BeautifulSoup(response, "html.parser")
    divs_results = soup.find_all("div", {"class": "t2_470"})
    for second_table_div in divs_results:
        if second_table_div:
            second_table = second_table_div.find("table", {"class": "table"})
            tables.append(second_table)
    return tables

def write_results(file_name, location_list, party_names):
    """
    Writes the extracted election results to a CSV file.
    """
    field_names = ["code", "location", "registered", "envelopes", "valid"] + party_names
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for location in location_list:
            del location["href_to_detail_page"]
            writer.writerow(location)
            
def validate_user_input(args):
    """
    Validates user input arguments for the script. True if the input is valid.
    """
    if args["url_address"].startswith("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&") == False:
        return False
    return True

if __name__ == "__main__":
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    output_file_name = "output.csv"
    parser = argparse.ArgumentParser()
    # parameters:-  url_address, name of the output file
    parser.add_argument("url_address", help="url_address for scraping.")
    parser.add_argument("output_file", help="name of the output file.")
    args = parser.parse_args()
    url = args.url_address
    output_file_name = args.output_file

    if url.startswith("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&") == False:
        print("Incorrect input arguments.")
        sys.exit()

    main_page_content_html = fetch_html_content(url)    
    soup = BeautifulSoup(main_page_content_html, 'html.parser')

    location_general_info_list = extract_main_page_data(soup)
    for location in location_general_info_list:
        print("Processing obec: " + location["location"])
        response = fetch_html_content(location["href_to_detail_page"])
        summary_table = extract_summary_table(response)
        detail_tables = extract_detail_tables(response)
        summary_dict = parse_summary_table(summary_table)
        location.update(summary_dict)
        for detail_table in detail_tables:
            parsed_data = parse_detailed_results_table(detail_table)
            location.update(parsed_data)
    party_names = get_party_name(detail_tables)

    write_results(output_file_name, location_general_info_list, party_names)
