import json, os


db_file = "./db/db.json"


# ---------
# BAD HACKS
# ---------
# todo: holy shit this is some real crappy hack
def get_filepath(filepath_with_extension, debug=False):
    test = filepath_with_extension[0]
    if not test == '/':
        filepath_with_extension = '/' + filepath_with_extension
    if test == '.':
        filepath_with_extension = filepath_with_extension[2:]
    if debug: print('starting filepath', filepath_with_extension)

    try:
        with open(filepath_with_extension): pass
        return filepath_with_extension
    except FileNotFoundError:
        try:
            fp0 = '.' + filepath_with_extension
            if debug: print('fp0', fp0)
            with open(fp0): pass
            return fp0
        except FileNotFoundError:
            try:
                fp1 = '..' + filepath_with_extension
                if debug: print('fp1', fp1)
                with open(fp1): pass
                return fp1
            except FileNotFoundError:
                try:
                    fp2 = '../..' + filepath_with_extension
                    if debug: print('fp2', fp2)
                    with open(fp2): pass
                    return fp2
                except FileNotFoundError:
                    try:
                        fp3 = '../../..' + filepath_with_extension
                        if debug: print('fp3', fp3)
                        with open(fp3): pass
                        return fp3
                    except:
                        print('current workingdir: ', os.getcwd())
                        raise SystemError("file not found by traversing backwards 3 folders")


def load_db(database_path=db_file, debug=False):
    database_path = get_filepath(database_path)
    with open(database_path) as json_db:
        return json.loads(json_db.read())


def update_db(dict_in, database_path=db_file, debug=False):
    with open(database_path, 'r') as json_db:
        state_str = json_db.read()
        state = json.loads(state_str)
        if debug:
            print('current state')
            print(json.dumps(state, indent=4, ensure_ascii=False))
            print('replacing state (this is not redux yet)')

        for k, v in dict_in.items():
            state[k] = dict_in[k]

    with open(database_path, 'w') as json_db:
        if debug:
            print('saving state')
        json.dump(state, json_db, ensure_ascii=False)


def make_db(dict_in, database_path, debug=False):
    with open(database_path, 'w') as json_db:
        json.dump(dict_in, json_db, ensure_ascii=False)



def print_list_of_dicts(input_list):
    [print(json.dumps(c, indent=4, ensure_ascii=False)) for c in input_list]


def unhashtagify(text):
    # unhashtagify
    if '#' in text[0]:
        text = text[1:]
        return text
    return text

