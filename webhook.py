import feedparser
import time
import requests
import json
import textwrap
import re

boturl =""

linklist = ["https://ufora.ugent.be/d2l/le/news/rss/237608/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/221698/course?token=a894nwfbntq37h5fd9e4",
            "https://ufora.ugent.be/d2l/le/news/rss/72830/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/77465/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/98740/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/120715/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/221779/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/232372/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/232374/course?token=a8hwkr1nxy74mx8d16b20",
            "https://ufora.ugent.be/d2l/le/news/rss/198624/course?token=a894nwfbntq37h5fd9e4&ou=198624",
            "https://ufora.ugent.be/d2l/le/news/rss/77068/course?token=a894nwfbntq37h5fd9e4&ou=77068",
            "https://ufora.ugent.be/d2l/le/news/rss/6606/course?token=a894nwfbntq37h5fd9e4&ou=6606"]

feed_list = []

for i in linklist:
    temp = feedparser.parse(i)
    print(temp)
    feed_list.append([temp, i, [j.id for j in temp.entries]])


def jsonpost(item):
    json_body = {}

    json_body["embeds"] = []
    embed = {}
    embed["title"] = item.title
    cleanr = re.compile('<.*?>')
    embed["description"] = "<@&765162715735916556>\n\n" + re.sub(cleanr, '', textwrap.wrap(item.summary, width=300)[0]) + "..."
    embed["url"] = item.link
    embed["color"] = 1991880
    embed["footer"] = {}
    embed["footer"]["text"] = item.published
    json_body["embeds"].append(embed)
    json_body["username"] = "Ugent"

    print(requests.post(data=json.dumps(json_body), url=boturl, headers={"Content-Type": "application/json"}))


jsonpost(feedparser.parse("https://ufora.ugent.be/d2l/le/news/rss/237608/course?token=a8hwkr1nxy74mx8d16b20").entries[0])


while True:
    for i in feed_list:
        tempfeed = i[0]
        feed_update = feedparser.parse(i[1])
        for j in feed_update.entries:
            if j.id not in i[2]:
                i[0] = feed_update
                i[2].append(j.id)
                jsonpost(j)

    time.sleep(1)
