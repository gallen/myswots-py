import bs4


def remove_tags(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    return soup.text