import get_xml_data
from misc import apis

API_KEY = apis.books()
# This is called later - they are characters we need to remove from the book synopsis
BAD_CHARS = ["<i>", "</i>", "<br />", "<b>", "</b>"]


def get_book_info(book):
    """
    This will call the get_xml_data function to grab XML data for user book
    :param book:
    :return:
    """
    goodreads_url = "https://www.goodreads.com/book/title.xml?key="
    title_prep = "&title="
    book_name = book.lower().replace(" ", "+")  # no spaces allowed. Spaces in name must be changed to a '+'
    full_url = goodreads_url + API_KEY + title_prep + book_name

    # I use the XML parser here, which is why this isn't tied to the get_json_data method
    root = get_xml_data.return_xml_data(full_url)
    return root


def book_info(book):
    """
    This will work through our XML data to extract the fields we care about
    :param book:
    :return:
    """
    # calling get_book_info to grab XML data
    book_data = get_book_info(book)

    # This will provide us the root of the xml file
    items = book_data.findall("book")

    # Looping through the XML file to grab details from the book search
    for item in items:
        book_title = item.find("title").text
        book_synopsis = item.find("description").text
        book_pub_date = item.find('publication_year').text
        num_pages = item.find('num_pages').text
        book_author = item.find('authors/author/name').text

        # This will clear out all the additional formatting characters from the book synopsis
        for char in BAD_CHARS:
            if char in book_synopsis:
                book_synopsis = book_synopsis.replace(char, "")

        return book_title, book_synopsis, book_pub_date, num_pages, book_author


def return_book_details(book):
    """
    This will return the info on the book for the user
    :param book:
    :return:
    """
    book_title, book_synopsis, book_pub_date, num_pages, book_author = book_info(book)

    return f"Title: {book_title}\n" \
           f"Number of Pages: {num_pages}\n" \
           f"Author: {book_author}\n" \
           f"Publication Date: {book_pub_date}\n\n" \
           f"Synopsis: {book_synopsis}"
