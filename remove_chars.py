def clean_text(content):
    """
    This function will take text and strip out excess characters
    :param content:
    :return:
    """
    bad_chars = [
        "<i>",
        "</i>",
        "<br />",
        "<b>",
        "</b>",
        "<",
        ">",
        "\\"
    ]

    for char in bad_chars:
        if char in content:
            content = content.replace(char, "")
    return content
