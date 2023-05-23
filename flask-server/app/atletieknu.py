import requests
from bs4 import BeautifulSoup
import csv
from io import StringIO

HEADERS = {
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


def create_session(username: str, password: str) -> requests.Session:
    """
    Create a logged in requests.Session() using atletiek.nu credentials.

    :param `username`: username of the Atletiek.nu account.
    :param `password`: password of the Atletiek.nu account.
    :returns: `Session()` object that is logged in.
    """

    s = requests.Session()
    url = 'https://www.atletiek.nu/login/'
    data = {
        'email': username,
        'password': password
    }
    s.get(url, headers=HEADERS)                 # GET login page to create a session ID in cookies
    s.post(url, data=data, headers=HEADERS)     # POST to login page in current session
    return s


def get_competitions(s: requests.Session) -> list:
    """
    List all competitions that the logged in user has rights to.

    :param `s`: a logged in `Session()` from `atletieknu.create_session()`.
    :returns: list of competitions: {'id': `competition_id`, 'name': `competition_name`}.
    """
    url = 'https://www.atletiek.nu/feeder.php'
    params = {
        'page': 'search',
        'do': 'events',
        'country': 'NL',
        'predefinedSearchTemplate': '3'
    }
    r = s.get(url, params=params, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html5lib')

    competitions = [{                                       # Find all competitions that we have rigths to
        'id': c['href'].split('/')[-2],                     # Strip the ID from the url
        'name': c.select_one('.eventnaam').text.strip()     # Find the name in the '.eventnaam' class
    } for c in soup.select('.eventnaam>a')]                 # Loop through all '.eventnaam>a' links
    return competitions


def get_leaderboards(s: requests.Session, competition_id: str) -> list:
    """
    List all leaderboards for a given competition_id.

    :param `s`: a logged in `Session()` from `atletieknu.create_session()`.
    :param `competition_id`: the competition id.
    :returns: list of leaderboards: {'id': `leaderboard_id`, 'name': `leaderboard_name`}.
    """
    url = f'https://www.atletiek.nu/wedstrijd/uitslagenprintmenu/{competition_id}/'
    r = s.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html5lib')

    leaderboards = [{                                       # Find all leaderboard in this competition
        'name': l.next_element.text.strip(),                # Name is stored after the checkbox
        'id': l['value']                                    # ID is the value of the checkbox
    } for l in soup.select('[name="ranglijst_ids[]"]')]     # Loop through all checkboxes with 'name=ranglijst_ids[]' attribute
    return leaderboards


def get_results(s: requests.Session, competition_id: str) -> list:
    """
    Download CSV results of a given competition and convert to a list of dicts.

    :param `s`: a logged in `Session()` from `atletieknu.create_session()`.
    :param `competition_id`: the competition id.
    :returns: list of results where every index contains a dict() with the column headers as keys.
    """
    url = 'https://www.atletiek.nu/feeder.php'
    leaderboards = [l['id'] for l in get_leaderboards(s, competition_id)]
    params = {
        'event_id': competition_id,
        'vereniging_id': '0',
        'do': 'diploma',
        'diplomatemplate_id': '',
        'ranglijst_ids[]': ','.join(leaderboards),
        'page': 'txtexport'
    }
    r = s.get(url, params=params, headers=HEADERS)

    with open("test.csv", "wb") as f:
        f.write(r.content)

    # Convert CSV to list of dicts. Every list index contains a dict with the CSV column headers as keys
    return [r for r in csv.DictReader(StringIO(r.content.decode()), delimiter=';')]
