import datetime
import json
import urllib.error
import urllib.request
import MiConfig

def timeline(since_id):
    url = "https://" + MiConfig.host + "/api/notes/timeline"
    data = {
        "i": MiConfig.token,
        "limit": 10
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "mozilla/5.0"
    }
    req = urllib.request.Request(url, data = json.dumps(data).encode("utf-8"), headers = headers, method = "POST")
    res = urllib.request.urlopen(req)
    body = res.read()
    return json.loads(body)

def post(text):
    url = "https://" + MiConfig.host + "/api/notes/create"
    data = {
        "i": MiConfig.token,
        "text": text
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "mozilla/5.0"
    }
    req = urllib.request.Request(url, data = json.dumps(data).encode("utf-8"), headers = headers, method = "POST")
    res = urllib.request.urlopen(req)
    body = res.read()
    return

def i():
    url = "https://" + MiConfig.host + "/api/i"
    data = {
        "i": MiConfig.token
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "mozilla/5.0"
    }
    req = urllib.request.Request(url, data = json.dumps(data).encode("utf-8"), headers = headers, method = "POST")
    res = urllib.request.urlopen(req)
    body = res.read()
    return json.loads(body)
