import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

def dfstrtoint(df, row, col):
    """
    Name1-3のdfを、Name10-31の2次元に変換する際に使用
    dfの文字を[int, int]にする
    :param df: Name1-3のあるdf
    :param col: 読み取り行
    :param row: 読みとる列
    :return: 文字コード10進数のリスト[int, int]
    """
    encoded = str(df.at[row, col].encode("shift-jis"))  #文字を読み取り
    if encoded == "b'0'":   #0を弾く
        return [0, 0]
    elif len(encoded) <10:
        int1 = int(encoded[4:6], 16)    #1次元めの10進数
        int2 = 67                       #x○○gの時は2次元めが67となる。
        return [int1, int2]
    else:
        int1 = int(encoded[4:6], 16)    #1次元めの10進数
        int2 = int(encoded[8:10], 16)   #2次元目の10進数
        return [int1, int2]

def split_test(df_DB):
    """
    エンコード済みのDBからテストセットを分割
    Genderが0と1が均等になるようStratified分割
    :df_DB: エンコード済DBのファイルパスかdf
    :return: train_set, test_set
    """
    if type(df_DB) == str:
        df = pd.read_csv(df_DB)
    else:
        df = df_DB

    # GenderでStratifiedテスト分割
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
    for train_index, test_index in split.split(df, df["Gender"]):
        strat_train_set = df.loc[train_index]
        strat_test_set = df.loc[test_index]

    return strat_train_set, strat_test_set