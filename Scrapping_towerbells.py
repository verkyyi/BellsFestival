"""
Skeleton code to scrape Towerbells.

TODOs:

1. parse the content from each section into the columsn you want
2. verify that it works on all pages
3. store the data in a CSV
4. (optionally) store each scraped page
"""

from bs4 import BeautifulSoup
from dataclasses import dataclass

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


def main(
        entrypoint: str,
) -> None:
    content = fetch_page(entrypoint)

    link_queue = get_links(content)

    for link in link_queue:
        content = fetch_page(link.href)
        sections = parse_data_page(content)
        
        for section in sections:
            print(section)
            print('-'*30)
if __name__ == '__main__':
    entrypoint = "http://towerbells.org/data/IXNATRnr.html"

    main(entrypoint)
