import sys, os
import pandas as pd
import argparse


def new_char(c):
    if c.lower() == "z":
        return chr(ord(c) - 25)
    else:
        return chr(ord(c) + 1)


def shuffle_str(s):
    return "".join([new_char(c) for c in s])


def anonymize_df(df, keys=None):
    # if no column names defined
    # all string columns are modified
    if not keys:
        keys = []
        columns = df.keys()
        for c in columns:
            if isinstance(df[c][0], str):
                keys.append(c)
    #
    for k in keys:
        df[k] = df[k].apply(lambda x: shuffle_str(x))
    return df


def anonymize_xls(file, keys=None):
    df = pd.read_excel(file, skiprows=[])
    fname, fext = os.path.splitext(file)
    anonymize_df(df, keys).to_excel(fname + "_anonymous" + fext, index=False)


def anonymize_csv(file, keys=None):
    df = pd.read_csv(file)
    fname, fext = os.path.splitext(file)
    anonymize_df(df, keys).to_csv(fname + "_anonymous" + fext, index=False)


def anonymize_json(file, keys=None):
    raise NotImplementedError()


def anonymize(file, keys=None):
    filename, file_extension = os.path.splitext(file)
    if file_extension in [".xls", ".xlsx"]:
        anonymize_xls(file, keys)
    elif file_extension == ".csv":
        anonymize_csv(file, keys)
    elif file_extension == ".json":
        anonymize_json(file, keys)
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to anonymize")
    parser.add_argument("-k", "--keys", nargs="+", help="column keys to anonymize")
    args = parser.parse_args()

    anonymize(args.file, args.keys)
