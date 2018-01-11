import get_json_data

PARTIAL_URL = "http://xkcd.com/"
END_URL = "info.0.json"


def return_xkcd_img(comic=None):
    """
    Simple method to return current xkcd comic strip
    The user can grab the daily image or specify a comic number to read
    :param comic:
    :return:
    """
    if comic is None:
        full_url = PARTIAL_URL + END_URL  # building url
        img = get_json_data.grab_json_data(full_url)
    else:
        comic_number = comic + "/"  # creating the comic number url
        full_comic_url = PARTIAL_URL + comic_number + END_URL
        img = get_json_data.grab_json_data(full_comic_url)
    return img["img"]  # only want to return image of the comic
