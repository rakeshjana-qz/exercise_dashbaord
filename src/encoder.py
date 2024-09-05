import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

EXERCISE_DASH_KEY = os.getenv("EXERCISE_DASH_KEY")

def encode_url(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr(((ord(clear[i]) + ord(key_c)) % 126))
        enc.append(enc_c)
    return urllib.parse.quote("".join(enc), safe="")

def decode_url(key, enc):
    dec = []
    enc = urllib.parse.unquote(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((126 + ord(enc[i]) - ord(key_c)) % 126)
        dec.append(dec_c)
    return "".join(dec)

def generate_encoded_query_string(search_fields):
    search_fields_str = ""
    for k, v in search_fields.items():
        if v:
            search_fields_str += "&%s=%s" % (k, str(v).replace("&", "%26"))
    encoded_query_string_contributor = encode_url(EXERCISE_DASH_KEY, search_fields_str)
    return encoded_query_string_contributor
