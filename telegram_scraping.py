from bs4 import BeautifulSoup
import requests


def remove_duplication(lst):
    return list(dict.fromkeys(lst))


def find_the_message(messages, movie_name):
    try:
        message = messages[0]
        message.find("div", class_="tgme_widget_message_text js-message_text").text
    except AttributeError:
        raise Exception("movie not found")

    for message in messages:
        message_text = message.find("div", class_="tgme_widget_message_text js-message_text").text
        if movie_name in message_text[0:100]:
            return message


def find_the_messages(soup):
    soup = soup.find('section', class_="tgme_channel_history js-message_history")
    messages = soup.find_all("div", class_=["tgme_widget_message_wrap","js-widget_message_wrap date_visible"])
    return messages


def red_message_get_links(message):
    link_list = []
    for a in message.find_all("a"):
        if "https://drive.google.com" in a.get("href"):
            link_list.append(a.get("href"))
    return link_list


def get_links(movie_name, server):

    web_html = requests.get(f"https://t.me/s/{server}?q={movie_name}").text
    soup = BeautifulSoup(web_html, "lxml")

    messages = find_the_messages(soup)

    links = find_the_message(messages, movie_name)

    link_list = red_message_get_links(links)

    if len(links) == 0:
        raise Exception("movie not found")

    return remove_duplication(link_list)


if __name__ == "__main__":
    movie_name = "דרגון בול"
    print(get_links(movie_name, "GDriveTv"))