import discord
import telegram_scraping as telegram

client = discord.Client()


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


def links_list_to_str(lst):
    string = ""
    for links in lst:
        string += links
        string += "\n"
    return string


@client.event
async def on_message(message):
    if str(message.channel) in channels and not message.author.name in bots:

        if "m:" == message.content[0:2]:
            movie_name = message.content.split(":")[1]
            found_link = False
            for server in servers:
                try:
                    links = telegram.get_links(movie_name, server)
                    found_link = True
                    break
                except Exception:
                    pass
            if not found_link:
                await message.channel.send("movie not found")

            else:
                string = links_list_to_str(links)
                await message.channel.send(string)

        elif not "!help" in message.content:
            await message.channel.send('תכתוב "help!" בשביל לקבל עזרה')


if __name__ == "__main__":
    channels = ["bot"]
    bots = ["MEE6", "דרייב"]
    servers = ["GDriveTv", "maagargavishahar"]
    token = read_token()
    client.run(token)