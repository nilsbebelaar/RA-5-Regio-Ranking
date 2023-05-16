import atletieknu

# Function for running this file standalone for testing
if __name__ == '__main__':
    from dotenv import load_dotenv
    from environs import Env

    load_dotenv()
    env = Env()
    s = atletieknu.create_session(env('ATLETIEKNU_USER'), env('ATLETIEKNU_PASS'))
    competitions = atletieknu.get_competitions(s)
    results = atletieknu.get_results(s, competitions[1]['id'])

    for r in results:
        print(r, '\n')
