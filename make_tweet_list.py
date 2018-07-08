from api.twitter_api import get_posts_from_trending_hashtags, search_tweets_by_location_name
from api.google_api import analyze_sentiment, get_geocode

from api.resas_api import get_prefectures_list

from utils.cache_utils import kw_cache_wrapper

import json


def process_posts(posts={}, location=''):
    output = []
    for v in posts:
        output_single = {}
        output_single['tweet'] = v['text']
        output_single['time'] = v['created_at']
        output_single['location'] = location['location']  #todo: grab location from post if not supplied
        output_single['sentiment'] = analyze_sentiment(v['text']).score

        output.append(output_single)

        # logic for selecting geolocation
    print(output)
    return output


def get_tweet_list_from_trends():
    posts = get_posts_from_trending_hashtags()[:2]

    for k, v_list in posts.items():
        print('')
        print('for hashtag {}'.format(k))

        geo_check = []
        coords_check = []
        place_check = []
        user_loc_check = []
        time_check = []

        location = []
        for v in v_list['statuses']:
            geo_check.append(v['geo'])
            coords_check.append(v['coordinates'])
            place_check.append(v['place'])
            user_loc_check.append(v['user']['location'])
            time_check.append(v['created_at'])

            # logic for selecting geolocation

        print('{} geo: {}'.format(len(geo_check), geo_check))
        print('{} coords: {}'.format(len(coords_check), coords_check))
        print('{} place: {}'.format(len(place_check), place_check))
        print('{} user_loc: {}'.format(len(user_loc_check), user_loc_check))
        print('{} time: {}'.format(len(time_check), time_check))

    # location as coordinates

    # sentiment
    #sentiments = analyze_sentiment()

    # time

    pass


def get_tweet_list_from_location_name(query=''):
    posts =  search_tweets_by_location_name(query=query)
    geocode = get_geocode(query=query)
    t = process_posts(posts=posts, location=geocode)
    return t

if __name__ == '__main__':
    prefecture = get_prefectures_list()[0]['prefName']
    print(prefecture)

    t = get_tweet_list_from_location_name(query=prefecture)
    [print(json.dumps(x, indent=4, ensure_ascii=False)) for x in t]