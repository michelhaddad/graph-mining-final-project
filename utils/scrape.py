import requests
from datetime import date

SPOTIFY_DAILY_CHART_URL = 'https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-daily/%s'


def global_daily_chart_response(date, headers, cookies):
    response = requests.get(SPOTIFY_DAILY_CHART_URL % date.strftime('%Y-%m-%d'), headers=headers, cookies=cookies)
    if not response.ok:
        raise Exception('Error while fetching data: Response code %d' % response.status_code)

    return response.json()


# Bearer token should be extracted manually from session
headers = {
    'authorization': 'Bearer blablabla',
}
cookies = {}

res = global_daily_chart_response(date(2019, 1, 1), headers, cookies)
print(res['displayChart'])
print('Number of entries: %d' % len(res['entries']))
