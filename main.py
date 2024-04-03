import itertools
import string
import requests

snusbase_key = 'YOUR_API_KEY_HERE'

proxies = []
usernames = []

with open('proxies.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        host, port = line.strip().split(":")
        
        proxies.append({
            "http": f"http://{host}:{port}",
        })

proxies = itertools.cycle(proxies)

with open('input.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        usernames.append(line.strip())

chunk_size = 25
emails_found = []

output = open('output.txt', 'a', encoding='utf-8')

while usernames:
    selected_users, usernames = usernames[:chunk_size], usernames[chunk_size:] 
    req = requests.post("https://api-experimental.snusbase.com/data/search", json={
        "terms":selected_users, "types":["username"], "wildcard": False
    }, headers={"Auth": snusbase_key})
    res = req.json()
    
    for result in res["results"].values():
        for leak in result:
            if "email" in leak:
                try:
                    output.write(f'{leak["email"]}\n')
                    print(f'appended {leak["email"]}')
                except Exception as e:
                    print(f'err with {leak["email"]}:', e)
                    continue