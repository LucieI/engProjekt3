
# engProjekt3
## Election Data Scraper

This Python script scrapes election data from a specified URL and generates a CSV file containing detailed results for each municipality.

### Prerequisites
Before using this script, you need to download the Requirements.txt and use the command "pip install -r Requirements.txt"
### Usage
    1. Clone this repository or download the script (projekt_3.py) to your local machine.
    2. Open a terminal or command prompt.
    3. Navigate to the directory containing the script.
    4. Run the script with the following command:
```
python projekt_3.py <URL> <output_file_name>
```
Replace <URL> with the URL of the election results page you want to scrape, and <output_file_name> with the desired name of the output CSV file.

For example: python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101" "jihocesky.csv"

### Functionality
The script performs the following tasks:

    1. Fetches HTML content from the specified URL.
    2. Extracts general information about municipalities from the main page.
    3. Parses the summary table containing general election statistics.
    4. Parses detailed results tables for individual parties.
    5. Writes the extracted data, including municipality information and party vote counts, to a CSV file.

![obrazek](https://github.com/LucieI/engProjekt3/assets/129436518/61173393-11df-4ed1-b05b-212208c71084)


### Author
This script was created by Lucie Ihnatoliova.

