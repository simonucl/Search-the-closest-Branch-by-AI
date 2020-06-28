import mpu
import numpy as np
import postcodes_io_api
import hack
import data
import requests
api  = postcodes_io_api.Api(debug_http=False)
dataset = np.array(data.load("db"))
from tqdm import tqdm_notebook as tqdm
db = data.load("db")

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

branches = np.array([[find(brand, 'BrandName'), find(bank, 'Identification'),
                          find(bank, 'PostalAddress'), find(bank, 'Availability')]
                         for brand in dataset[:, 3] if find(brand, 'Branch') is not None for bank in
                         find(brand, 'Branch')])
branches_LL = []
for i in range (len(branches)):
    try: 
        branches_LL.append([branches[i][2]['GeoLocation']['GeographicCoordinates']['Latitude'],branches[i][2]['GeoLocation']['GeographicCoordinates']['Longitude'],branches[i][0],branches[i][2]['PostCode']]) 
    except:
        pass

atms = [find(bank, 'PostCode') for brand in dataset if find(brand, 'ATM') is not None for bank in find(brand, 'ATM')]
latitudes = [find(bank, 'Latitude') for brand in dataset if find(brand, 'ATM') is not None for bank in find(brand, 'ATM')]
longitudes = [find(bank, 'Longitude') for brand in dataset if find(brand, 'ATM') is not None for bank in find(brand, 'ATM')]
brandnames = [find(brand, 'BrandName') for brand in dataset if find(brand, 'ATM') is not None for bank in find(brand, 'ATM')]
ids = [find(bank, 'Identification') for brand in dataset if find(brand, 'ATM') is not None for bank in find(brand, 'ATM')]
allatms = []
for i in range (len(ids)):
    allatms.append([atms[i], latitudes[i], longitudes[i], brandnames[i], ids[i]])

def getMeATM(postcode):
    atm_data = np.array(allatms)
    location = api.get_postcode(postcode)
    latitude = location['result']['latitude']
    longitude = location['result']['longitude']
    data = [latitude, longitude]
    dist_list = []
    for i in range (len(atm_data)):
        dist_list.append(mpu.haversine_distance((float(atm_data[i][1]), float(atm_data[i][2])), (data[0], data[1])))
    nearest_atm_list = atm_data[np.argsort(dist_list)]
    return ("The nearest ATM is in " + nearest_atm_list[0][0]+ "." + "(" + nearest_atm_list[0][3] +")")

def getMeBranches(postcode):
    branches_data = np.array(branches_LL)
    location = api.get_postcode(postcode)
    latitude = location['result']['latitude']
    longitude = location['result']['longitude']
    data = [latitude, longitude]
    dist_list = []
    for i in range (len(branches_data)):
        dist_list.append(mpu.haversine_distance((float(branches_LL[i][0]), float(branches_LL[i][1])), (data[0], data[1])))
    nearest_branch_list = branches_data[np.argsort(dist_list)]
    return("The nearest branch is in " + nearest_branch_list[0][2] + "(" + nearest_branch_list[0][3] +")" + ".")

def getMeBranchesLL(postcode):
    branches_data = np.array(branches_LL)
    print(postcode)
    location = api.get_postcode(postcode)
    if 'result' not in location:
        print(location)
    latitude = location['result']['latitude']
    longitude = location['result']['longitude']
    data = [latitude, longitude]
    dist_list = []
    for i in range (len(branches_data)):
        dist_list.append(mpu.haversine_distance((float(branches_LL[i][0]), float(branches_LL[i][1])), (data[0], data[1])))
    nearest_branch_list = branches_data[np.argsort(dist_list)]
    return [nearest_branch_list[0][0],nearest_branch_list[0][1]]

def getMeATMLL(postcode):
    atm_data = np.array(allatms)
    location = api.get_postcode(postcode)
    latitude = location['result']['latitude']
    longitude = location['result']['longitude']
    data = [latitude, longitude]
    dist_list = []
    for i in range (len(atm_data)):
        dist_list.append(mpu.haversine_distance((float(atm_data[i][1]), float(atm_data[i][2])), (data[0], data[1])))
    nearest_atm_list = atm_data[np.argsort(dist_list)]
    return [nearest_atm_list[0][1], nearest_atm_list[0][2]]

def getMeBranchesForSpecificBank(postcode, bank):
    branches_data = np.array(branches_LL)
    location = api.get_postcode(postcode)
    latitude = location['result']['latitude']
    longitude = location['result']['longitude']
    data = [latitude, longitude]
    dist_list = []
    banklist = []
    for i in range (len(branches_data)):
        if bank in branches_LL[i][2]:
             banklist.append(branches_LL[i])
#     print(banklist)
    for i in range (len(banklist)):
        dist_list.append(mpu.haversine_distance((float(banklist[i][0]), float(banklist[i][1])), (data[0], data[1])))
    banklist = np.array(banklist)
    nearest_branch_list = banklist[np.argsort(dist_list)]
    return("The nearest branch is in " + nearest_branch_list[0][3] + "(" + nearest_branch_list[0][2] +")" + ".")

def getMeBranchesForSpecificBankLL(postcode, bank):
    branches_data = np.array(branches_LL)
    location = api.get_postcode(postcode)
    latitude = location['result']['latitude']
    longitude = location['result']['longitude']
    data = [latitude, longitude]
    dist_list = []
    banklist = []
    for i in range (len(branches_data)):
        if bank in branches_LL[i][2]:
             banklist.append(branches_LL[i])
#     print(banklist)
    for i in range (len(banklist)):
        dist_list.append(mpu.haversine_distance((float(banklist[i][0]), float(banklist[i][1])), (data[0], data[1])))
    banklist = np.array(banklist)
    nearest_branch_list = banklist[np.argsort(dist_list)]
    return [nearest_branch_list[0][0] ,nearest_branch_list[0][1]]

def atms(data):
    return np.array([[atm['Identification'],
                      atm['Location']['PostalAddress']['PostCode'],
                      atm['Location']['PostalAddress']['GeoLocation']['GeographicCoordinates']['Latitude'],
                      atm['Location']['PostalAddress']['GeoLocation']['GeographicCoordinates']['Longitude']]
                     for atm in data['data'][0]['Brand'][0]['ATM']])


def branches(data):
    return np.array([[branch['Identification'],
                      branch['PostalAddress']['PostCode'],
                      branch['PostalAddress']['GeoLocation']['GeographicCoordinates']['Latitude'],
                      branch['PostalAddress']['GeoLocation']['GeographicCoordinates']['Longitude']]
                     for branch in data['data'][0]['Brand'][0]['Branch']])



url = 'https://atlas.api.barclays/open-banking/v2.2/'
headers = {'cache-control': 'no-cache'}

with requests.Session() as session:
    data_atms = atms(session.get(url + 'atms', headers=headers).json())
    data_branches = branches(session.get(url + 'branches', headers=headers).json())
    old_college = ['55.9475', '-3.1865']

#print(getMeATM("EH8 9YL"))
print(getMeBranches("EH8 9YL"))