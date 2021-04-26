import sys, os
import pandas as pd
import argparse

intelligent_list = ["ressource", "nom", "prenom", "client"]


def new_char(c):
    if (ord(c) < 65) or (ord(c) > 122):
        return c
    elif (ord(c) > 90) and (ord(c) < 97):
        return c
    if c.lower() == "z":
        return chr(ord(c) - 25)
    else:
        return chr(ord(c) + 1)


def shuffle_str(s):
    return "".join([new_char(c) for c in s])


def anonymize_df(df, keys=[], intelligent=False, whole=False):
    # if no column names defined
    # all string columns are modified
    # TODO : peut ête qu'un filtre par mot clé ("nom", "prénom")
    # serait plus pertinent. possibilité de creer une option
    if not keys and whole:
        keys = df.keys()
    elif not keys and intelligent:
        keys = []
        for k in df.keys():
            for n in intelligent_list:
                if n in k.lower():
                    keys.append(k)
    for k in keys:
        try:
            df[k] = df[k].apply(lambda x: shuffle_str(x))
        except TypeError:
            pass
    return df


def anonymize_xls(file, keys=[], intelligent=False, whole=False):
    df = pd.read_excel(file, skiprows=[])
    fname, fext = os.path.splitext(file)
    anonymize_df(df, keys, intelligent, whole).to_excel(
        fname + "_anonymous" + fext, index=False
    )


def anonymize_csv(file, keys=[], intelligent=False, whole=False):
    df = pd.read_csv(file)
    fname, fext = os.path.splitext(file)
    anonymize_df(df, keys, intelligent, whole).to_csv(
        fname + "_anonymous" + fext, index=False
    )


def anonymize_json(file, keys=[], intelligent=False, all=False):
    raise NotImplementedError()


def anonymize(file, keys=[], intelligent=False, all=False):
    filename, file_extension = os.path.splitext(file)
    if file_extension in [".xls", ".xlsx"]:
        anonymize_xls(file, keys, intelligent, all)
    elif file_extension == ".csv":
        anonymize_csv(file, keys, intelligent, all)
    elif file_extension == ".json":
        anonymize_json(file, keys, intelligent, all)
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to anonymize")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-k", "--keys", nargs="+", help="column keys to anonymize")
    group.add_argument(
        "-i",
        "--intelligent",
        action="store_true",
        dest="intelligent",
        default=False,
        help="automatic mode",
    )
    group.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        default=False,
        help="all strings",
    )
    args = parser.parse_args()
    anonymize(args.file, args.keys, args.intelligent, args.all)
