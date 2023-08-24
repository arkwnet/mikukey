import datetime
import MiConfig as config

def timeline(since_id):
    return config.api.notes_hybrid_timeline(
        limit = 10,
        since_id = since_id
    )

def post(text):
    config.api.notes_create(text = text)
    return
