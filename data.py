import requests
import pandas as pd


'''API DOC: https://lunarcrush.com/developers/docs# '''
KEY_API = '39o5gbbtx7n1gxkvnhf6na'


def get_coin_data(symbol, data_points=365, interval='day'):
    url = "https://api.lunarcrush.com/v2?data=assets&key={}&symbol={}&data_points={}&interval={}".format(KEY_API,
                                                                                                         symbol,
                                                                                                         data_points,
                                                                                                         interval)
    response = requests.get(url).json()
    data = response['data'][0]
    df = pd.json_normalize(data['timeSeries'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    data = pd.json_normalize(data)
    df['MA-Low'] = df.low.rolling(window=20).mean()
    df['MA-High'] = df.high.rolling(window=20).mean()
    df['MA-Volume'] = df.volume.rolling(window=20).mean()
    details = data[
        ['name', 'symbol', 'price', 'price_btc', 'market_cap', 'percent_change_24h', 'percent_change_7d',
         'percent_change_30d',
         'volume_24h', 'max_supply']]

    return (df, details.to_dict(orient='records')[0])


def get_global_information(change=6, data_points=182):
    url = "https://api.lunarcrush.com/v2?data=global&key={}&change={}m&data_points={}".format(KEY_API,
                                                                                              change, data_points)
    response = requests.get(url).json()
    df = pd.json_normalize(response['data']['timeSeries'])
    df = df[['time', 'volume', 'btc_dominance', 'btc_market_cap', 'alt_coin_market_cap', 'altcoin_dominance']]
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df


def get_n_top_coins(n=50):
    url = 'https://api.lunarcrush.com/v2?data=market&key={}&sort=acr&type=fast'.format(KEY_API)
    response = requests.get(url).json()
    df = pd.json_normalize(response['data'])
    df.rename(columns={
        's': 'Symbol',
        'n': 'Name',
        'p': 'Price',
        'v': 'Volume',
        'pc': '24 Hours',
        'pch': '1 Hour',
        'mc': 'Market Cap',
        'gs': 'Galaxy Score',
        'ss': 'Social Score',
        'acr': 'ALTRank',
        't': 'Number of tweets',
        'sd': 'Social Dominance',
        'd': 'Market Dominance'
    }, inplace=True)
    df['24 Hours'] = df['24 Hours'].div(100).round(4)
    df['1 Hour'] = df['1 Hour'].div(100).round(4)

    return df[['ALTRank', 'Galaxy Score', 'Social Score', 'Symbol', 'Name', 'Price', 'Volume', '24 Hours', '1 Hour',
               'Market Cap', 'Number of tweets', 'Social Dominance', 'Market Dominance']]


def get_social_coin_data(symbol):
    url = 'https://api.lunarcrush.com/v2?data=assets&key={}&symbol={}'.format(KEY_API, symbol)
    response = requests.get(url).json()['data']

    df = pd.json_normalize(
        response,
        record_path=['timeSeries'],
        meta=['symbol']
    )
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df[['unique_url_shares', 'url_shares', 'reddit_posts', 'tweets', 'tweet_spam', 'time', 'symbol']]
    return df


def get_feeds_information():
    url = "https://api.lunarcrush.com/v2?data=feeds&key={}&limit=20&sources=news,urls".format(KEY_API)
    response = requests.get(url).json()
    df = pd.json_normalize(response['data'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df


def get_tweets_data():
    url = "https://api.lunarcrush.com/v2?data=feeds&key=39o5gbbtx7n1gxkvnhf6na&&limit=20&sources=twitter"
    response = requests.get(url).json()
    data = response['data']
    df = pd.json_normalize(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df