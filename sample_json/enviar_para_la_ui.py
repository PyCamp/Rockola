import requests

message = open("songs_list.json").read()

payload = {
    "message": message,
    "channel": "base"
}

r=requests.post("http://192.168.10.90:8888/publish", data=payload)
print r.status_code
