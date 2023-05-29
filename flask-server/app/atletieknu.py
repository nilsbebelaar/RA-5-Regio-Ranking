import requests
from bs4 import BeautifulSoup
import csv
from io import StringIO
from time import time

MAX_RPS = 2
HEADERS = {
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


class AtletiekNu():
    __s = requests.Session()
    __last_request = time()
    competitions = []
    leaderboards = []

    def __init__(self, username: str, password: str):
        """
        Create a logged in requests.Session() using atletiek.nu credentials.
        """

        self.__s = requests.Session()
        url = 'https://www.atletiek.nu/login/'
        data = {
            'email': username,
            'password': password
        }
        self.__send_request(type="GET", url=url)                # GET login page to create a session ID in cookies
        self.__send_request(type="POST", url=url, data=data)    # POST to login page in current session
        # self.__s.get(url, headers=HEADERS)
        # self.__s.post(url, data=data, headers=HEADERS)

    def get_competitions(self):
        """
        List all competitions that the logged in user has rights to.
        """

        url = 'https://www.atletiek.nu/feeder.php'
        params = {
            'page': 'search',
            'do': 'events',
            'country': 'NL',
            'predefinedSearchTemplate': '3'
        }
        r = self.__send_request(type="GET", url=url, params=params)
        soup = BeautifulSoup(r.content, 'html5lib')

        self.competitions = [{                                       # Find all competitions that we have rigths to
            'id': c['href'].split('/')[-2],                     # Strip the ID from the url
            'name': c.select_one('.eventnaam').text.strip()     # Find the name in the '.eventnaam' class
        } for c in soup.select('.eventnaam>a')]                 # Loop through all '.eventnaam>a' links

    def accept_licence_agreement(self, competition_id: str):
        """
        For every new competition, every account has to accept the licence agreement.
        """

        url = f'https://www.atletiek.nu/wedstrijd/main/{competition_id}/'
        data = {
            'agree_event_license_voorwaarden': '1',
            'agree_age': '1'
        }
        r = self.__send_request(type="POST", url=url, data=data)

    def get_leaderboards(self, competition_id: str):
        """
        List all leaderboards for a given competition_id.
        """

        url = f'https://www.atletiek.nu/wedstrijd/uitslagenprintmenu/{competition_id}/'
        r = self.__send_request(type="GET", url=url)
        soup = BeautifulSoup(r.content, 'html5lib')

        if soup.select('[name="agree_event_license_voorwaarden"]'):
            # First time accessing this competition, need to accept the licence agreement
            self.accept_licence_agreement(competition_id)
            r = self.__send_request(type="GET", url=url)
            soup = BeautifulSoup(r.content, 'html5lib')

        self.leaderboards = [{                                       # Find all leaderboard in this competition
            'name': l.next_element.text.strip(),                # Name is stored after the checkbox
            'id': l['value']                                    # ID is the value of the checkbox
        } for l in soup.select('[name="ranglijst_ids[]"]')]     # Loop through all checkboxes with 'name=ranglijst_ids[]' attribute

    def get_results(self, competition_id: str) -> list:
        """
        Download CSV results of a given competition and convert to a list of dicts.
        """

        # https://www.atletiek.nu/feeder.php?
        # event_id=39486
        # vereniging_id=0
        # do=deelnemers
        # diplomatemplate_id=
        # ranglijst_ids%5B%5D=346139
        # onderdeel_ids%5B%5D=4009
        # onderdeel_ids%5B%5D=-1
        # onderdeel_ids%5B%5D=44
        # onderdeel_ids%5B%5D=4
        # page=txtexport


        url = 'https://www.atletiek.nu/feeder.php'

        self.get_leaderboards(competition_id)
        returnlist = []
        for l in self.leaderboards:
            params = {
                'event_id': competition_id,
                'vereniging_id': '0',
                'do': 'diploma',
                'diplomatemplate_id': '',
                'ranglijst_ids[]': l['id'],
                'page': 'txtexport'
            }
            r = self.__send_request(type="GET", url=url, params=params)

            with open(f"{competition_id}_{l['name']}.csv", "wb") as f:
                f.write(r.content)

            returnlist += [r for r in csv.DictReader(StringIO(r.content.decode()), delimiter=';')]

        # Convert CSV to list of dicts. Every list index contains a dict with the CSV column headers as keys

        return returnlist

    def __send_request(self, type: str, **kwargs):
        """
        Custom function for sending requests that keeps track of time in order to keep the amount of requests per second below the ratelimit threshold.
        """
        while time() - self.__last_request < (1 / MAX_RPS):  # Limit to MAX_RPS requests per second to avoid ratelimiter
            pass
        if type == "GET":
            self.__last_request = time()
            return self.__s.get(**kwargs, headers=HEADERS)
        if type == "POST":
            self.__last_request = time()
            return self.__s.post(**kwargs, headers=HEADERS)
