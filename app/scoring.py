from environs import Env
import requests
from bs4 import BeautifulSoup

headers = {
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def create_session():
    env = Env()

    s = requests.Session()

    url = 'https://www.atletiek.nu/login/'
    data = {
        'email': env('ATLETIEKNU_USER'),        # Login username and password stored as Environment variables
        'password': env('ATLETIEKNU_PASS')
    }
    s.get(url, headers=headers)                 # GET login page to create a session ID in cookies
    s.post(url, data=data, headers=headers)     # POST to login page in current session

    return s


def get_competitions(s: requests.Session):
    url = 'https://www.atletiek.nu/feeder.php'
    params = {
        'page': 'search',
        'do': 'events',
        'country': 'NL',
        'predefinedSearchTemplate': '3'
    }
    r = s.get(url, params=params, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')

    competitions = [{                                       # Find all competitions that we have rigths to
        'id': c['href'].split('/')[-2],                     # Strip the ID from the url
        'name': c.select_one('.eventnaam').text.strip()     # Find the name in the '.eventnaam' class
    } for c in soup.select('.eventnaam>a')]                 # Loop through all '.eventnaam>a' links

    return competitions


def get_leaderboards(s: requests.Session, id: int):
    url = f'https://www.atletiek.nu/wedstrijd/uitslagenprintmenu/{id}/'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')

    leaderboards = [{                                       # Find all leaderboard in this competition
        'name': l.next_element.text.strip(),                # Name is stored after the checkbox
        'id': l['value']                                    # ID is the value of the checkbox
    } for l in soup.select('[name="ranglijst_ids[]"]')]     # Loop through all checkboxes with 'name=ranglijst_ids[]' attribute

    return leaderboards

    # Get CSV for given event_id and ranglijst_ids[]. Still need to implement as function
    params = {
        'event_id': '38541',
        'vereniging_id': '0',
        'do': 'diploma',
        'diplomatemplate_id': '',
        'ranglijst_ids[]': '345143',
        'page': 'txtexport'
    }

    r = s.get(url, params=params, headers=headers)

    with open("test.csv", "wb") as f:
        f.write(r.content)
    with open("test.csv", "wb") as f:
        f.write(r.content)
    return


# Function for running this file standalone for testing
if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    s = create_session()
    competitions = get_competitions(s)
    print(competitions[1])
    leaderboards = get_leaderboards(s, competitions[1]['id'])

    print(leaderboards)
