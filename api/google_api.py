import json, six, os
import os.path as path
# Imports the Google Cloud client library
from google.cloud import translate, language
from google.cloud.language import enums, types


def translate_text_api(text='', target='ja', debug=False):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    if debug:
        try:
            print(u'Text: {}'.format(result['input']))
            print(u'Translation: {}'.format(result['translatedText']))
            print(u'Detected source language: {}'.format(
                result['detectedSourceLanguage']))
        except:
            pass

    return result


def translate_text(text='', target='ja', debug=False):
    from utils.baseutils import load_db, update_db, get_filepath
    db_dir = "/db"
    db_filename = "translation-cache.json"

    db_filepath = get_filepath(path.join(db_dir, db_filename))

    db_keyword_pair = load_db(database_path=db_filepath, debug=debug)
    try:
        output = db_keyword_pair[text]
        if debug: print('local keyword pair found!')
        return output
    except KeyError:
        if debug: print('calling google translate to translate (will only happen once per word)')
        response = translate_text_api(text=text, target=target, debug=debug)
        output = response['translatedText']
        db_keyword_pair[text] = output
        update_db(db_keyword_pair, database_path=db_filepath)
        return output


def detect_language_api(text, debug=False):
    """Detects the text's language.
    :returns ISO compatible language
    """
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    if debug:
        print('Text: {}'.format(text))
        print('Confidence: {}'.format(result['confidence']))
        print('Language: {}'.format(result['language']))
    return result


def detect_language_code(text):
    return detect_language_api(text)['language']


def analyze_entities_api(text='', verbose=False):
    """
    ref: https://cloud.google.com/natural-language/docs/reference/rpc/google.cloud.language.v1#google.cloud.language.v1.AnalyzeEntitiesResponse
    name:
          The representative name for the entity.
    type:
          The entity type.
    metadata:
          Metadata associated with the entity.  Currently, Wikipedia
          URLs and Knowledge Graph MIDs are provided, if available. The
          associated keys are "wikipedia\_url" and "mid", respectively.
    salience:
          The salience score associated with the entity in the [0, 1.0]
          range.  The salience score for an entity provides information
          about the importance or centrality of that entity to the
          entire document text. Scores closer to 0 are less salient,
          while scores closer to 1.0 are highly salient.
    mentions:
          The mentions of this entity in the input document. The API
          currently supports proper noun mentions.
    sentiment:
          For calls to [AnalyzeEntitySentiment][] or if [AnnotateTextReq
          uest.Features.extract\_entity\_sentiment][google.cloud.languag
          e.v1.AnnotateTextRequest.Features.extract\_entity\_sentiment]
          is set to true, this field will contain the aggregate
          sentiment expressed for this entity in the provided document.

    :param document:
    :param verbose:
    :return: (entity.name, entity.type)
    """
    """Detects entities in the text."""
    text = text.lower()  #apparently entity search fails if there are capitals

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    # TODO: specify only entities that we are interested in finding?
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    # is it a full name, or a common noun?
    entity_mention_type = ('TYPE_UNKNOWN', 'PROPER', 'COMMON')

    list_of_entities = []
    # todo: key entry by relevance or by entity name!?
    for entity in entities:
        list_of_entities.append({
            entity.name: {
                "entity salience": entity.salience,
                "entity type": entity_type[entity.type]
            }
        })
        #list_of_entities.append((entity.name, entity_type[entity.type], '{:.2f}'.format(entity.salience)))

    return list_of_entities


def parse_entities(text='', debug=False):
    """
    entity level parsing
    :param text:
    :param debug:
    :return:
    """
    from utils.baseutils import load_db, update_db, get_filepath
    db_dir = "/db"
    db_filename = "entity-cache.json"

    db_filepath = get_filepath(path.join(db_dir, db_filename))

    db_keyword_pair = load_db(database_path=db_filepath, debug=debug)
    try:
        output = db_keyword_pair[text]
        if debug: print('local keyword pair found!')
        return output
    except KeyError:
        if debug: print('calling google translate to translate (will only happen once per word)')
        response = analyze_entities_api(text)
        print(response)
        raise
        response = translate_text_api(text=text, target=target, verbose=debug)
        output = response['translatedText']
        db_keyword_pair[text] = output
        update_db(db_keyword_pair, database_path=db_filepath)
        return output


def identify_entities(text):
    """
    sentence level parsing
    :param text:
    :return:
    """
    # 1. check if any of the entities in the cache is in the text

    # 2. if not inside, run something to get entities
    # todo: i thought google nlp would

    output_dict = []

    for i in range(10):
        dict_item = {
            "label": "",
            "position": 3,
            "is_entity": True
        }

        output_dict.append(dict_item)

    raise
    return output_dict



if __name__ == '__main__':
    translate_text("fathers day", debug=True)
    translate_text("japan", debug=True)
    detect_language_api('弟')
    parse_entities("wakeupamerica")
    parse_entities("america makes us strong like teeth")