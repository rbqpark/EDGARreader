"""
BASIC DESCRIPTION

EDGAR Reader is a web scraping program dedicated to collecting relevant information about corporations from their SEC filings.
Its ultimate purpose is to look through 10Ks and 10Qs to monitor changes over the course of two years or a couple quarters respectively.

This program is written in Python 3 and requires additional modules to successfully function, including primarily BeautifulSoup4 and Requests.
"""

"""
MEMO ABOUT LINKS

Link to daily 10K and 10K/A: http://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=*
Link to daily 10Q: http://www.sec.gov/cgi-bin/current?q1=0&q2=1&q3=*

*this can easily be maniupulated to check filings by timeframe by changing the necessary variable. q1 refers to time, q2 refers to formtype, q3 is left blank.
"""

from bs4 import BeautifulSoup
import time
import datetime
import os
import requests
import urllib.request

url_dict = {'SEC': 'http://www.sec.gov', '10K': 'http://www.sec.gov/cgi-bin/current?q1=0&q2=0&q3=', '10Q': 'http://www.sec.gov/cgi-bin/current?q1=0&q2=1&q3='}
"""Simple dictionary to store the original urls"""

link_dict = {}
dl_dict = {}
names_dict = {}

def find_date():
    curr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return str(curr)

def select_url(formtype, t):
"""Takes in an integer T as an input and returns the appropriate url for given FORMTYPE and T days elapsed."""
    indicator = "q1=" + str(t)
    return url_dict[formtype].replace("q1=0", indicator)

def find_links(formtype, t, link_dict={}):
"""Returns a filled LINK_DICT dictionary with # of link as its key and the download link as its value for the inputted FORMTYPE."""
"""This needs some fixing so that all the links stored inside the link_dict are actual download links, not just the name."""
    def soupify(formtype):
    """Creates a BeautifulSoup object for given FORMTYPE using its sec filing url."""
        if type(formtype) != str or not(formtype in url_dict):
            raise Error
        return BeautifulSoup(requests.get(select_url(formtype, t)).content, "html.parser")
    soup_form = soupify(formtype)
    links = soup_form.find_all("a")
    index, skip, counter = 0, "skip", 0
    for link in links:
        if type(index) == int:
            link_dict[index] = link.get("href")
            index = skip
            counter += 1
        elif type(index) == str:
            index = counter
    del link_dict[len(link_dict) - 1]
    return link_dict

def reset(dictionary):
    dictionary.clear()

def find_files(link_dict, dl_dict={}):
    for i in range(len(link_dict)):
        soup_form = BeautifulSoup(requests.get(url_dict['SEC'] + link_dict[i]).content, "html.parser")
        links = soup_form.find_all("a")
        dl_dict[i] = links[9].get("href")
    return dl_dict

def retrieve_names(formtype, t):
    if type(formtype) != str or not(formtype in url_dict):
        raise Error
    soup_form = BeautifulSoup(requests.get(select_url(formtype, t)).content, "html.parser")
    temp_names = soup_form.get_text("|")[239:].replace(" ", "").split("|")
    i = 0
    for name in temp_names:
         if name == "\n" or name == "10-Q" or name == "" or "googletagmanager.com" in name or "Generatedat" in name:
                 pass
         else:
                 if "\n" in name:
                     names_dict[i] = name.split("\n")[0].replace("/", "")
                     i += 1
    return names_dict

def dl_files(formtype, t):
"""This procedure is used to download all the files of a particular FORMTYPE uploaded within the past T days on SEC.gov/cgi-bin.
T is an integer of 0 to 5."""
"""Current code is done in a particular format for future use and implementation. THere are more efficient ways of executing this."""
    state_time = time.time()
    if not(0 <= t <= 5):
        raise Error
    link_dict = find_links(formtype, t)
    dl_dict = find_files(link_dict)
    names_dict = retrieve_names(formtype, t)
    date = find_date()
    desired_path = "C:\Python34\ " + date
    desired_path.replace(" ", "")
    if not os.path.exists(desired_path):
        os.makedirs(desired_path)
    os.chdir(desired_path)
    for i in range(len(dl_dict)):
        requested = urllib.request.Request(url_dict['SEC'] + dl_dict[i])
        response = urllib.request.urlopen(requested)
        company = names_dict[i]
        file_name = company + ".htm"
        new_file = open(file_name, 'wb')
        new_file.write(response.read())
        new_file.close()
    reset(dl_dict)
    print("Runtime: %s seconds" % (time.time() - state_time))
    print("Finished downloading, check Python directory.")

def extract_tables(_____):
    os.chdir(desired_path)
    new_file = ("filename", "wb")
    for i in range(len(tables)): #where tables is a list returned by executing soup.find_all("table")
        table = str(tables[i])
        new_file.write(bytes(table, "UTF-8"))
    new_file.close()

def get_data(file):
"""This goes through already downloaded files from directory and returns desired data."""
