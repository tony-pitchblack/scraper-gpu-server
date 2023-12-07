import re
from bs4 import BeautifulSoup

# URL: https://www.reg.ru/dedicated/
with open("./servers-data.html", encoding='utf-8', mode='r') as file:
    servers_data = file.read().replace('\n', '')

soup = BeautifulSoup(servers_data, "html.parser")


servers_list = soup.find_all("div", "b-dedicated-servers-list-item")
servers_list = list(filter(
    lambda server: int(server["data-gpucount"]) > 0,
    servers_list
    ))

servers_parsed = []
for server in servers_list:
    parsed_data = {
        'name': server["data-server-id"],
        'gpu': server["data-gpu"].upper(),
        'ram': server["data-ram"],
        'cpu-freq': server["data-slider-freq"].replace('.', ','),
        'cpu-cores': server["data-cores"],
        'price': server["data-slider-price"]
    }

    hdd_ssd_string = server.find("p", class_="b-dedicated-servers-list-item__hdds").text
    hdd_ssd = hdd_ssd_string.split("<br>")
    def get_disks_volume(disks_str):
        regex = r"(\d) x (\d*).*"
        match = re.search(regex, disks_str)
        disks_count = match.group(1)
        disk_volume = match.group(2)
        return int(disks_count) * int(disk_volume)

    ssd_volume = get_disks_volume(hdd_ssd[-1])
    parsed_data.update({'ssd-volume': ssd_volume})

    hdd_volume = 0
    if len(hdd_ssd) == 2:
        hdd_volume = get_disks_volume(hdd_ssd[-2])
    parsed_data.update({'hdd-volume': hdd_volume})
    
    servers_parsed.append(parsed_data)

for server in servers_parsed:
    print(*list(server.values())[:-1])
