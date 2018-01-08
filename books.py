import urllib.request
from misc import apis
from xml.etree import ElementTree as ET


def book_info(book):
    """
    This function takes a book name and return all information about the book
    :param book:
    :return: book_title, num_pages, book_author, book_pub_date, book_synopsis
    """
    api_key = apis.books()
    goodreads_url = "https://www.goodreads.com/book/title.xml?key="
    title_prep = "&title="
    book_name = book.lower().replace(" ", "+")
    url = goodreads_url + api_key + title_prep + book_name

    # I use the XML parser here, which is why this isn't tied to the get_json_data method
    with urllib.request.urlopen(url) as url_xml:
        root = ET.parse(url_xml).getroot()

    # This will provide us the root of the xml file
    items = root.findall("book")

    # XML is super easy to loop through
    for item in items:
        book_title = item.find("title").text  # title of user book
        book_synopsis = item.find("description").text  # Synopsis for user book
        # Not sure if there is a better way to strip excess formatting out from the xml file
        book_synopsis = book_synopsis.replace("<i>", "")  # stripping off <i>
        book_synopsis = book_synopsis.replace("</i>", "")  # stripping off </i>
        book_synopsis = book_synopsis.replace("<br />", " ")  # stripping off <br />
        book_pub_date = item.find('publication_year').text  # year of book publication
        num_pages = item.find('num_pages').text  # number of pages
        book_author = item.find('authors/author/name').text  # author of the book

    return f"Title: {book_title}\n" \
           f"Number of Pages: {num_pages}\n" \
           f"Author: {book_author}\n" \
           f"Publication Date: {book_pub_date}\n\n" \
           f"Synopsis: {book_synopsis}"
