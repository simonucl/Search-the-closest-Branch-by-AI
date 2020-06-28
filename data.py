import requests
import json
import numpy as np


def save(data, path):
    with open(path, 'w') as file:
        json.dump(data, file)


def load(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def retrieve(url):
    with requests.Session() as session:
        response = session.get(url, headers={'Accept-Encoding': 'deflate'}, verify=False)
    return response.json()


def get_banks():
    apis = ['atms', 'branches', 'personal-current-accounts', 'business-current-accounts',
            'unsecured-sme-loans', 'commercial-credit-cards']
    data = retrieve(
        'https://raw.githubusercontent.com/OpenBankingUK/opendata-api-spec-compiled/master/participant_store.json')
    database = []
    for bank in data['data']:
        database.append([bank['name'], bank['baseUrl']] +
                        [retrieve(bank['baseUrl'] + '/' + bank['supportedAPIs'][api][0] + '/' + api)
                         if api in bank['supportedAPIs'] else None for api in apis])
    return database


def find(db, key):
    if isinstance(db, dict):
        for k, v in db.items():
            if key == k:
                return v
            else:
                v = find(v, key)
                if v is not None:
                    return v
    elif isinstance(db, list) or isinstance(db, np.ndarray):
        for data in db:
            v = find(data, key)
            if v is not None:
                return v
    return None


def main():
    pass


if __name__ == '__main__':
    main()
