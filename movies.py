import get_json_data
from misc import apis

# Setting up initial URL variables
API_KEY = apis.movies()
PARTIAL_URL = "https://api.themoviedb.org/3/search/movie?api_key="
QUERY = "&query="


def prep_title(movie_name):
    """
    This function take a movie name and return the title, release date, and overview
    of the movie.

    The search string for the URL needs white spaces to contain + instead
    example: https://api.themoviedb.org/3/search/movie?api_key={API Key}&query=Jack+Reacher
    :param movie_name:
    :return: title, release date, overview
    """
    # Replacing white spaces with + symbols
    movie_search_format = movie_name.replace(" ", "+")
    url = PARTIAL_URL + API_KEY + QUERY + movie_search_format
    data = get_json_data.grab_json_data(url)
    # we only want to return title, release date, and info about the movie
    for info in data["results"]:
        return info["original_title"], info["release_date"], info["overview"]


def movie_info(movie):
    """
    This is what we call to obtain information about the movie and return the data
    :param movie:
    :return:
    """
    title, release_date, overview = prep_title(movie)
    return f"{title} ({release_date}): {overview}"
