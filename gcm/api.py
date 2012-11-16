# -*- encoding: utf-8 -*-
import urllib
import urllib2
import json

def send_gcm_message(api_key, reg_ids, data, collapse_key=None):

    values = {
        "registration_ids": reg_ids,
        "collapse_key": collapse_key,
        "data": data
    }

    data = json.dumps(values)

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + api_key,
        'Content-Length': str(len(data))
    }

    request = urllib2.Request("https://android.googleapis.com/gcm/send", data, headers)
    response = urllib2.urlopen(request)
    result = response.read()

    return result