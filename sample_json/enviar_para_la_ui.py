import requests

message = open("songs_list.json").read()

payload = {
    "message": message,
    "channel": "base"
}

r=requests.post("http://localhost:8888/publish", data=payload)
print r.status_code
