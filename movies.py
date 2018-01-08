import get_json_data
from misc import apis

api_key = apis.movies()


def prep_title(movie_name):
    """
    This function take a movie name and return the title, release date, and overview
    of the movie.

    The search string for the URL needs white spaces to contain + instead
    example: https://api.themoviedb.org/3/search/movie?api_key={API Key}&query=Jack+Reacher
    :param movie_name:
    :return: title, release date, overview
    """
    partial_url = "https://api.themoviedb.org/3/search/movie?api_key="
    query = "&query="
    # Replacing white spaces with + symbols
    movie_search_format = movie_name.replace(" ", "+")
    url = partial_url + api_key + query + movie_search_format
    # let's read the contents of the web page, which is returned in json format
    data = get_json_data.grab_json_data(url)
    # we only want to return title, release date, and info about the movie
    for info in data["results"]:
        return info["original_title"], info["release_date"], info["overview"]


def movie_info(movie):
    title, release_date, overview = prep_title(movie)
    return "{} ({}): {}".format(title, release_date, overview)
