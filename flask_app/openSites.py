import requests
import webbrowser
from bs4 import BeautifulSoup

# Opens Pinkbike based on user entered details
def pinkbikeSearch(riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country):    
    url = "https://www.pinkbike.com/buysell/list/?"

    # Enters the country code to the url
    countries = {
        "Australia": 13,
        "Canada": 35,
        "Germany": 69,
        "United Kingdom": 193,
        "United States": 194,
    }

    if country != None:    
        countryNum = countries[country]
        url += "location=" + str(countryNum) + '-*-*'
    else: 
        countryNum = countries("United States")
        url += "location=" + str(countryNum) + '-*-*'

    regions = {
        "Asia": 1,
        "Canada/USA": 3,
        "South America": 4,
        "Europe": 5,
        "Australia/NZ": 6
    }

    # Changes the category number in the url based on riding type
    if riding_type == 'Cross Country (XC)':
        url += '&category=75'
    elif riding_type == 'Downhill':
        url += '&category=1'
    elif riding_type == 'Trail':
        url += '&category=102'
    elif riding_type == 'Enduro':
        url += '&category=2'

    # Adds frame size filter based on user's height
    height_split = height.split()
    height = (12 * int(height_split[0])) + int(height_split[2])

    if height != None:
        if int(height) <= 62:
            size = '1,2,3,10,4,5,6,7,8,13,14,15'
        elif int(height) > 62 and int(height) <= 66:
            size = '9,11,12,17,18,20,21,22'
        elif int(height) > 66 and int(height) <= 69:
            size = '16,19,24,25,26,28,29'
        elif int(height) > 69 and int(height) <= 73:
            size = '23,27,34,35,36,30,31,47'
        else:
            size = '32,37,38,39,40,48,49,33,41,42,43,44,45,46,50,51,52,53,54'
        url += "&framesize=" + size

    # Adds wheel size filter based on user's preference
    if wheel_size != None:
        wheels = {
            '26"': 8,
            '27.5"': 11,
            '29"': 10
        }

        if wheel_size in wheels:
            wheel_pref = wheels[wheel_size]
        else:
            wheel_pref = '8,11,10'
    
        url += '&wheelsize=' + str(wheel_pref)

    # Enters the user's desired price range
    if min_budget != None and max_budget != None:
        url += '&price=' + str(min_budget) + '..' + str(max_budget)
    elif min_budget == None and max_budget != None:
        url += '&price=..' + max_budget
    elif min_budget != None and max_budget == None:
        url += '&price=' + str(min_budget) + '..'

    # Enters the user's suspension travels
    if rear_sus == 'Hardtail':
        if riding_type == 'Cross Country (XC)':
            fork_travel = '100,110,120'
        elif riding_type == 'Trail':
            fork_travel = '120,130,140,150'
        elif riding_type == 'Enduro':
            fork_travel = '150,160,170,175,180'
        elif riding_type == 'Downhill':
            fork_travel = '180,190,200,203,208'
        
        url += '&reartravel=1' + '&fronttravel=' + fork_travel
    # Enters suspension travel if full suspension option is picked
    else:
        if riding_type == 'Cross Country (XC)':
            fork_travel = '100,110,120'
            rear_travel = '80,100,110,120'
        elif riding_type == 'Trail':
            fork_travel = '120,130,140,150'
            rear_travel = '120,130,135,140,143,145'
        elif riding_type == 'Enduro':
            fork_travel = '150,160,170,175,180'
            rear_travel = '135,140,143,145,150,153,155,160,170,180'
        elif riding_type == 'Downhill':
            fork_travel = '180,190,200,203,208'
            rear_travel = '170,180,190,200,215,216,254,255'

        url += '&reartravel=' + rear_travel + '&fronttravel=' + fork_travel

    try:
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        bike_titles = soup.find_all("a", class_="bsitem-title")
        bike_descriptions = soup.find_all("td", class_="bsitem-description")
        for i in range(bike_descriptions):
            print(bike_titles[i])
            print(bike_descriptions[i], end="\n"*2)
        return url
    except:
        webbrowser.open(url)
        return url


# Opens TheProsCloset based on user entered details
def prosClosetSearch(riding_type, height, min_budget, max_budget, wheel_size, rear_sus, country):
    url = "https://www.theproscloset.com/collections/mountain-bikes?page=1"

    # Adds frame size filter based on user's height
    height_split = height.split()
    height = (12 * int(height_split[0])) + int(height_split[2])

    if height != None:
        if int(height) <= 61:
            size = 'xs'
        elif int(height) > 61 and int(height) <= 65:
            size = 's'
        elif int(height) > 65 and int(height) <= 69:
            size = 'm'
        elif int(height) > 69 and int(height) <= 73:
            size = 'l'
        else:
            size = 'xl'
        url += "&tags=framesize-" + size

    # Adds wheel size filter based on user's preference
    if wheel_size != None:
        wheels = {
            '26"': "26",
            '27.5"': "27.5",
            '29"': "29"
        }

        if wheel_size in wheels:
            wheel_pref = wheels[wheel_size]
            url += '%2Cwheelsize-' + wheel_pref

    # Enters the user's rear suspension travels
    if rear_sus == 'Hardtail':
        url += '%2Creartravel-hardtail'
    # Enters suspension travel if full suspension option is picked
    else:
        if riding_type == 'Cross Country (XC)':
            rear_travel = '110mm'
        elif riding_type == 'Trail':
            rear_travel = '111-130mm%2Creartravel-131-150mm'
        elif riding_type == 'Enduro':
            rear_travel = '131-150mm%2Creartravel-151-170mm'
        elif riding_type == 'Downhill':
            rear_travel = '171mm'

        url += '%2Creartravel-' + rear_travel

    # Enters the user's desired price range
    if min_budget != "" and max_budget != "":
        url += '&minPrice=' + str(min_budget) + '&maxPrice=' + str(max_budget)
    elif min_budget == "" and max_budget != "":
        url += '&maxPrice=' + str(max_budget)
    elif min_budget != "" and max_budget == "":
        url += '&minPrice=' + str(min_budget)

    try:
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)
        return url
    except:
        webbrowser.open(url)
        return url