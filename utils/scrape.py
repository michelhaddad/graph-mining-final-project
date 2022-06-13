import requests
from datetime import date, timedelta
import pandas as pd

SPOTIFY_DAILY_CHART_URL = 'https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-global-daily/%s'


def global_daily_chart_response(chart_date: date, headers: dict, cookies: dict):
    response = requests.get(SPOTIFY_DAILY_CHART_URL % chart_date.strftime('%Y-%m-%d'), headers=headers, cookies=cookies)
    if not response.ok:
        raise RuntimeError('Error while fetching data for %s: Response code %d' % (
            chart_date.strftime('%Y-%m-%d'), response.status_code))

    return response.json()


def convert_chart_response_to_df(chart_response):
    df = pd.DataFrame()
    date = chart_response['displayChart']['date']
    entries = chart_response['entries']

    for track in entries:
        artists = []
        for artist in track['trackMetadata']['artists']:
            artists.append({'id': artist['spotifyUri'][16:], 'name': artist['name'] if 'name' in artist else ''})

        row = {
            'date': date,
            'name': track['trackMetadata']['trackName'] if 'trackName' in track['trackMetadata'] else '',
            'id': track['trackMetadata']['trackUri'][15:],
            'artists': artists
        }

        df = pd.concat([df, pd.DataFrame(row)], ignore_index=True)

    return df


def daily_chart_in_range(start, end, headers, cookies):
    streams = pd.DataFrame()

    while start < end:
        if start.day == 1:
            print('Fetching songs for %d/%d...' % (start.month, start.year))
        try:
            response = global_daily_chart_response(start, headers, cookies)
            streams = pd.concat([streams, convert_chart_response_to_df(response)], ignore_index=True)
        except RuntimeError as e:
            print(e)

        start += timedelta(1)

    return streams


# Bearer token should be extracted manually from session
headers = {
    'authorization': 'Bearer BQCP_srwT_V5Vj9rGk8TH6WukJmL5833j_yAsexoBpgcM-J3MHjCfTtU9wMIzq_x38kACeWFnSjG1BEHReNeT62jgY-WtMPaiEDxObwJzqXMAhm5H-9MUoAFZ4dZBvBiqC1OiEPFTu-k-Ka3AVWG-J-9z7K-eworOzu2tM9pYjVWSk2ADqxxMy_4VcBW1iEwYEoUSXDePUMWyxjvLaXSRtj2Vg',
}
cookies = {}
start = date(2018, 1, 1)
end = date(2022, 6, 12)

daily_chart_in_range(start, end, headers, cookies).to_csv('../data/daily_charts.csv')
