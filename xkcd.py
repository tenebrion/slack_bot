import get_json_data


def return_xkcd_img(comic=None):
    """
    Simple method to return current xkcd comic strip
    The user can grab the daily image or specify a comic number to read
    :param comic:
    :return: img['img']
    """
    partial_url = "http://xkcd.com/"
    end_url = "info.0.json"
    if comic is None:
        full_url = partial_url + end_url  # building url
        img = get_json_data.grab_json_data(full_url)
    else:
        comic_number = comic + "/"  # creating the comic number url
        full_comic_url = partial_url + comic_number + end_url
        img = get_json_data.grab_json_data(full_comic_url)
    return img["img"]  # only want to return image of the comic
