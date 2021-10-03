import json

with open('config.json', 'r') as conf:
    config = json.load(conf)

access_key = config['DEFAULT']['ACCESS_KEY'] # 'access-key-of-upbit'
secret_key = config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-upbit'