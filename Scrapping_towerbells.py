"""
Skeleton code to scrape Towerbells.

TODOs:

1. parse the content from each section into the columsn you want
2. verify that it works on all pages
3. store the data in a CSV
4. (optionally) store each scraped page
"""
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime
import csv
import requests


@dataclass
class Link:
    href: str
    text: str


def fetch_page(
        url: str
) -> BeautifulSoup | None:
    response = requests.get(url)

    if response.status_code < 300 and response.status_code >= 200:
        return BeautifulSoup(response._content,features="html.parser")
    else:
        print(f"URL could not be fetched: {url}")
        return None


def get_links(
        page: BeautifulSoup,
        base: str = "http://towerbells.org/data/{page}"
) -> list[Link]:
    links = []
    for link in page.find_all("a"):
        url = link.attrs.get('href')

        # skip if empty url
        if not url.strip():
            continue

        # skip if it's a mailing link
        if url.startswith("mailto:"):
            continue

        # skip if it's a different directory
        if url.startswith(".."):
            continue

        if url.startswith("Glossary") or \
            url.startswith("NA_car_ixs") or \
            url.startswith("Data_Top") or \
            url.startswith("Cred_Disc") or \
            url.startswith("Feedback"):
            continue

        links.append(Link(href=base.format(page=url), text=link.text))
    
    return links


def parse_data_page(
        page: BeautifulSoup
) -> list[str]:
    # get the content of the first paragraph that starts with a *
    paragraphs = page.find_all("p")
    for paragraph in paragraphs:
        if paragraph.text.strip().startswith("*"):
            text = paragraph.text
            break
    if 'text' not in locals() and 'text' not in globals():
        return []
    start_index = text.find("Site locator map")
    end_index = text.find("*", start_index)
    text = text[:start_index] + text[end_index:]

    # Split the text by lines that start with "*"
    sections = []
    current_section = ""
    for line in text.splitlines():
        if line.startswith("*"):
            if current_section:
                sections.append(current_section.strip())
            current_section = line
        else:
            current_section += "\n" + line

    # Append the last section
    if current_section:
        sections.append(current_section.strip())

    return sections




def main(entrypoint: str,) -> None:
    content = fetch_page(entrypoint)
    link_queue = get_links(content)
    rows = []
    for link in link_queue:
        content = fetch_page(link.href)
        sections = parse_data_page(content)
        a_row = {}
        for section in sections:
            if(len(section)>0):
                # get section name from first line starting with *
                section_name = section.splitlines()[0].strip('*').split(':')[0]
                # lower case and replace spaces with underscore
                section_name = section_name.lower().replace(' ','_')
                # based on section name use differenct function to get fields using switch case
                function_name = 'get_fields_' + section_name
                # before calling function, check if function exists
                if function_name in globals():
                    # call function to get fields dictionary
                    fields = globals()[function_name](section)
                    # merge fields dictionary with a_row
                    a_row = {**a_row, **fields}
        # appending a_row to rows
        rows.append(a_row)
        print(a_row)
    # convert rows to csv and save it using csv library
    with open('towerbells.csv', 'w', newline='') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row_with_defaults = {field: row.get(field, 'DEFAULT') for field in fieldnames}
            writer.writerow(row_with_defaults)

# TODO: Sample of a function to get fields from a section
# 1. section name should be lower case and replace spaces with underscore
def get_fields_section_name(section_text):
    return {
        'field1': 'value1',
        'field2': 'value2'
    }

# To do

# Section Location

# Section Carillonist

# Section Past carillonist

# Section Contact
def get_fields_contact(contract_part):
    dic = {}
    address_matches = re.search(r'(?<=\()(A)(?=\))([\s\S]*?)T:', contract_part)
    if address_matches:
        address = address_matches.group(2).strip().replace('\n', ', ').replace('   ', ' ')
        dic['Address'] = address
    phone_matches = re.search(r'T: (\(\d{3}\)\d{3}-?\d{4})', contract_part)
    if phone_matches:
        phone = phone_matches.group(1)
        dic['Telephone:'] = phone
    return dic

# Section Schedule

# Section Remarks
def get_fields_remarks(text):
    result = {}
    # Extracting the date when the page was built
    match = re.search(r"Remarks: (.+)", text)
    if match:
        result['Remarks'] = match.group(1)
    return result

# Section Technical data
def get_fields_technical_data(text):
    result = {}
    
    # Extracting the number of bells
    match = re.search(r"Traditional carillon of (\d+) bells", text)
    if match:
        result['Number of Bells'] = int(match.group(1))
    
    # Extracting the pitch of the heaviest bell
    match = re.search(r"Pitch of heaviest bell is (.+) in", text)
    if match:
        result['Pitch of Heaviest Bell'] = match.group(1).strip()
    
    # Extracting transposition
    match = re.search(r"Transposition is up  (\d+) semitone\(s\)", text)
    if match:
        result['Transposition (semitones)'] = int(match.group(1))
        
    # Extracting keyboard range
    match = re.search(r"Keyboard range:     (.+)  /    (.+)", text)
    if match:
        result['Keyboard Range'] = {
            'Low': match.group(1).strip(),
            'High': match.group(2).strip()
        }
    # Extracting year of latest technical info
    match = re.search(r"Year of latest technical information source is (\d+)", text)
    if match:
        result['Year of Latest Technical Info'] = int(match.group(1))
    # Additional data like missing bass semitone, practice console, etc. can also be extracted similarly.
    return result

# Section Links
def get_fields_links(text):
    result = {}
    return result

# Section Status
def get_fields_status(text):
    result = {}
    # Extracting the date when the page was built
    match = re.search(r"This page was built from the database on  (\d+-\w+-\d+)", text)
    if match:
        date_str = match.group(1)
        result['Page Built Date'] = datetime.strptime(date_str, "%d-%b-%y").date()

    # Extracting the date when the textual data was last updated
    match = re.search(r"based on textual data last updated on (\d+/\d+/\d+)", text)
    if match:
        date_str = match.group(1)
        try:
            result['Textual Data Last Updated'] = datetime.strptime(date_str, "%Y/%m/%d").date()
        except:
            result['Textual Data Last Updated'] = None

    # Extracting the date when the technical data was last updated
    match = re.search(r"and on technical data last updated on (\d+/\d+/\d+)", text)
    if match:
        date_str = match.group(1)
        result['Technical Data Last Updated'] = datetime.strptime(date_str, "%Y/%m/%d").date()
    return result



if __name__ == '__main__':
    entrypoint = "http://towerbells.org/data/IXNATRnr.html"
    main(entrypoint)
