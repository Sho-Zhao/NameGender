import pandas as pd
from config import config
from NameSplit import NameSpli

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

def NameEncoding(df_dec):
    """

    :param df_dec: 名前をエンコードする前のdfもしくはcsvファイルパス
    :return: エンコード済みのdf
    """
    if type(df_dec) is str:
        df = pd.read_csv(df_dec, encoding="cp932")
    else:
        df = df_dec

    Namelist ={"Name1" : ["Name10", "Name11"], "Name2" : ["Name20", "Name21"],
               "Name3" : ["Name30", "Name31"]} #2次元のエンコードのため、1文字を2次元に変換

    for row in range(len(df)):
        for name in Namelist: #Name1から3を取り出し
            encoded = dfstrtoint(df, row, name)
            df.at[row, Namelist[name][0]] = encoded[0]
            df.at[row, Namelist[name][1]] = encoded[1]

    col_list=["Name10", "Name11", "Name20", "Name21", "Name30", "Name31", "Gender"]
    df = df[col_list]
    return df

if __name__ == "__main__":  #DBから名前を取り出してエンコードする前処理
    file = config() #設定ファイル
    df_dec = NameSpli(file["path_ori_db"]) #名前の取り出し
    df = NameEncoding(df_dec)   #名前のエンコード
    df.to_csv(file["path_to_csv"])  #前処理エンコード住みDB