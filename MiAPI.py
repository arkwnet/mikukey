import datetime
import json
import urllib.error
import urllib.request
import MiConfig
USER_AGENT = "mozilla/5.0"

def timeline(since_id):
    data = {
        "i": MiConfig.token,
        "limit": 10
    }
    return call("notes/timeline", data)

def post(text):
    url = "https://" + MiConfig.host + "/api/notes/create"
    data = {
        "i": MiConfig.token,
        "text": text
    }
    call("notes/create", data)
    return

def i():
    data = {
        "i": MiConfig.token
    }
    return call("i", data)

def call(api, data):
    url = "https://" + MiConfig.host + "/api/" + api
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT
    }
    req = urllib.request.Request(url, data = json.dumps(data).encode("utf-8"), headers = headers, method = "POST")
    res = urllib.request.urlopen(req)
    body = res.read()
    return json.loads(body)

def download(url, path):
    headers = {
        "User-Agent": USER_AGENT
    }
    req = urllib.request.Request(url, headers = headers)
    with urllib.request.urlopen(req) as file_web:
        with open(path, "wb") as file_local:
            file_local.write(file_web.read())
    return
