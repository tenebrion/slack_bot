import requests
from xml.etree import ElementTree as ET


def return_xml_data(url):
    """
    Simple method to return the root XML content from various APIs
    :param url:
    :return:
    """
    r = requests.get(url)  # grabbing XML data from remote API
    return ET.fromstring(r.content)  # returning root XML
