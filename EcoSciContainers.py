import vk_api
import os.path
import time
import requests
from datetime import datetime

links_list = []

file = open("containers.txt", "r")
while True:
    line = file.readline()
    if not line:
        break
    l = line.strip()
    pos = l.find("vk.cc/")
    links_list.append(l[pos + 6:])
file.close

with open("wait_time.txt", "r") as f:
    h_wait_time = float(f.read())
    wait_time = int(h_wait_time * 3600)

bot_token = "vk1.a.KcjbrIkn3KBeErZ52vh6wzNlLUGe2zRCH2W0fN5P9owa7A__zTS4GN_I0WJ4b_teLbUHj5dOfmeyVJ08Y_fxY4MvF8S4Oy9Sh4r_hvszEqwvmTUdDsjVSH_ZQwsx7G8al5ZJyfDmTwvTGZBqh522weYDPXkCV3KKrljEmcFRKRSrgSCePlBSNOBVCV5FHe6hmODbYf_u6eQmN4AJkrl71w"
tg_token = "6010822429:AAEzHQkCrDRS39mxSFW1yOqynsmp61r3ziE"
tg_chat_id = "-1001836092876"

tg_url = "https://api.telegram.org/bot{}/".format(tg_token)
vk = vk_api.VkApi(token = bot_token)

def send_message_to_tg(content):
    req_text = tg_url + "sendMessage?text=" + content + "&chat_id=" + tg_chat_id
    req = requests.post(req_text)
    return req

def get_views(link):
    return vk.method('utils.getLinkStats', {'key': link, 'interval': "forever"})["stats"][0]["views"]

if os.path.isfile("viows.txt") != True:
    with open("viows.txt", "w") as f:
        for link in links_list:
            view = str(vk.method('utils.getLinkStats', {'key': link, 'interval': "forever"})["stats"][0]["views"])
            f.write(view + "\n")

def viewer(view_list):
    i = 1
    with open("viows.txt", "w") as f:
        for view in view_list:
            link = view[0]
            last_view = view[1]
            new_view = get_views(link)
            if new_view > last_view:
                content = f"Поступило сообщение о переполнении контейнера номер {i}.\nЭто {new_view - last_view}-e обращение по этому контейнеру за последний(е) {wait_time} час(а)"
                send_message_to_tg(content)
                print(content + "\n")
                view[1] = new_view
            f.write(str(view[1]) + "\n")
            i += 1
    print(datetime.fromtimestamp(int(time.time())), " проверка успешно проведена")

view_list = []
with open("viows.txt", "r") as f:
    for link in links_list:
        view = int(f.readline())
        view_list.append([link, view])

while True:
    viewer(view_list)
    print(f"Ожидаю {int(h_wait_time)} час(а)(ов)")
    time.sleep(wait_time)