from hidden.hidden import Twitter
import twitter
import yweather
import json
import os.path as path

from utils.baseutils import get_filepath, make_db, print_list_of_dicts, unhashtagify
from utils.w2vutils import distance_pair_with_entities
from utils.tokenizer_utils import tokenize_and_normalize_sentences

from api.google_api import detect_language_code, translate_text

t_secrets = Twitter()
consumer_key = t_secrets.consumer_key
consumer_secret = t_secrets.consumer_secret
access_token_key = t_secrets.access_token_key
access_token_secret = t_secrets.access_token_secret

# sleep on rate limit=True allows the api to continue and wait till
# the rate limit is lifted, instead of failing
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret,
                  sleep_on_rate_limit=True)



# TIME FORMATTING
time_format_full_with_timezone = '%Y-%m-%d %H:%M:%S %Z'
time_format_full_no_timezone = '%Y-%m-%d %H:%M:%S'
time_format_day = '%Y-%m-%d'
time_format_hour = '%Y-%m-%d %H'

db_dir = "/db"
cache_filename = "cache.json"

db_dict_structure = {
    "content": {
        "label": [],
        "score": 0
    }
}


cache_db_filepath = get_filepath(path.join(db_dir, cache_filename))
make_db(db_dict_structure, cache_db_filepath)


def get_hashtags_from_query_list(query_dict_list_in):
    trends_query = [x['query'] for x in query_dict_list_in]

    # get posts, grab hashtags from post
    # todo


    # todo
    # for now, return name
    output_list = [x['name'] for x in query_dict_list_in]

    return output_list


# calculate distance pairs
def calculate_pairwise_distance(keyword='大坂', list_of_entities=['日本', '錦糸町最高', '秋葉原の喫茶店', '地震'], method='average', debug=False):
    # translate everything into target language (japanese)
    # this is designed to support future languages (word2vec currently only for japanese
    # todo: train english word2vec
    if debug: print('keyword: {}'.format(keyword))

    target_language_code = detect_language_code(keyword)

    output_score = []
    for entity in list_of_entities:
        if debug: print('hashtag: {}'.format(entity))

        # remove hashtags
        entity = unhashtagify(entity)

        # tokenize
        tokens = tokenize_and_normalize_sentences(entity, language=detect_language_code(entity))
        if debug: print('original tokens: {}'.format(tokens))

        # translate into target language to be able to properly perform word2vec
        tokens = [translate_text(e, target=target_language_code) for e in tokens]
        if debug: print('translated tokens: {}'.format(tokens))

        # for each token, calculate w2v
        token_similarities = distance_pair_with_entities((keyword, tokens))
        # filter out 9999 (NaNs)
        token_similarities = [x for x in token_similarities if x != 9999]
        # but leave one
        if len(token_similarities) == 0:
            token_similarities = [9999]

        if debug: print('w2v similarity: {}'.format(token_similarities))

        # then return average / closest
        if method == 'average':
            score = sum(token_similarities) / len(token_similarities)
        elif method == 'closest':
            score = min(token_similarities)
        else:
            score = min(token_similarities)

        if debug:
            print('score ({}): {}'.format(method, score))
            print('-'*100)

        output_score.append(score)
    return output_score


# calculates the similarity of trending topics globally and in japan to the supplied keyword
def calculate_trend_similarity(keyword='大坂', country='Japan'):
    # set country of interest
    country_of_interest = country

    # this stupid WOEID requires yweather to get (a library), because YAHOO itself has stopped supporting it
    # WOEID
    woeid_client = yweather.Client()
    woeid = woeid_client.fetch_woeid(location=country_of_interest)

    # 1. call twitter to return trends
    # get trends global. each trend is a dictionary
    current_trends_global = api.GetTrendsCurrent()
    current_trends_global = [c.AsDict() for c in current_trends_global]

    # get trends by WOEID
    current_trends_country = api.GetTrendsWoeid(woeid=woeid)
    current_trends_country = [c.AsDict() for c in current_trends_country]

    print_list_of_dicts(current_trends_country)
    print_list_of_dicts(current_trends_global)

    # optional: get additional hashtags
    # global_hashtags_from_trends_list = get_hashtags_from_query_list(current_trends_global)
    # country_hashtags_from_trends_list = get_hashtags_from_query_list(current_trends_country)

    # turn them both into lists
    current_trends_global_list = [x['name'] for x in current_trends_global]
    current_trends_country_list = [x['name'] for x in current_trends_country]

    # calculate pairwise distance here
    global_relevance = calculate_pairwise_distance(keyword=keyword, list_of_entities=current_trends_global_list, debug=True)
    country_relevance = calculate_pairwise_distance(keyword=keyword, list_of_entities=current_trends_country_list, debug=True)

    output = {
        "global": global_relevance,
        "country": country_relevance
    }

    return output



# 3. filter for disaster keywords or for sudden spikes in interest
# todo

# 4. when triggered, get top posts and return images and photos


# 5. get friends from twitter, and check their latest replies (how long since the disaster before they replied?)


if __name__ == '__main__':
    print(calculate_trend_similarity())