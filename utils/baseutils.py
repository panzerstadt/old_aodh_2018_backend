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


def get_directory(directory, debug=False):
    d = lambda x: os.path.isdir(x)
    if debug: print(directory)
    if d(directory):
        return directory
    else:
        dir0 = '.' + directory
        if d(dir0):
            print('returning: ', dir0)
            return dir0
        else:
            dir1 = '..' + directory
            if d(dir1):
                print('returning: ', dir1)
                return dir1
            else:
                dir2 = '../..' + directory
                if d(dir2):
                    print('returning: ', dir2)
                    return dir2
                else:
                    dir3 = '../../..' + directory
                    if d(dir3):
                        print('returning: ', dir3)
                        return dir3
                    else:
                        raise SystemError("directory not found by traversing 3 folders backwards")


def print_list_of_dicts(input_list):
    [print(json.dumps(c, indent=4, ensure_ascii=False)) for c in input_list]


def unhashtagify(text):
    # unhashtagify
    if '#' in text[0]:
        text = text[1:]
        return text
    return text


