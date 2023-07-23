import codecs
import json
import pwn
from base64 import b64decode

r = pwn.remote('socket.cryptohack.org', 13377)

received_decoded = {
    "decoded": "changeme"
}


def json_recv():
    tmp = r.recvline()
    return json.loads(tmp.decode())


def json_send(json_obj):
    req = json.dumps(json_obj).encode()
    r.sendline(req)


def base64Decoder(encoded_txt):
    decoded_txt = b64decode(encoded_txt).decode()
    return decoded_txt


def hexDecoder(encoded_txt):
    decoded_txt = bytes.fromhex(encoded_txt).decode("utf-8")
    return decoded_txt


def rot13Decoder(encoded_txt):
    decoded_txt = codecs.decode(encoded_txt, 'rot13')
    return decoded_txt


def bigIntDecoder(encoded_txt):
    decoded_txt = hexDecoder(encoded_txt[2:])
    return decoded_txt


def utf8Decoder(encoded_txt):
    decoded_txt = "".join([chr(num) for num in encoded_txt])
    return decoded_txt


def start():
    for i in range(101):
        received = json_recv()
        print(received)

        if list(received)[0] == "type":
            if received["type"] == "base64":
                received_decoded["decoded"] = base64Decoder(received["encoded"])
            elif received["type"] == "hex":
                received_decoded["decoded"] = hexDecoder(received["encoded"])
            elif received["type"] == "rot13":
                received_decoded["decoded"] = rot13Decoder(received["encoded"])
            elif received["type"] == "bigint":
                received_decoded["decoded"] = bigIntDecoder(received["encoded"])
            elif received["type"] == "utf-8":
                received_decoded["decoded"] = utf8Decoder(received["encoded"])
            print(received_decoded)
            json_send(received_decoded)
        elif list(received)[0] == "flag":
            print("Here's the flag: {}".format(received["flag"]))
        else:
            print("There was an error")


start()
