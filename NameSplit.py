import pandas as pd
from config import config

def NameSpli(file):
    """
    Name - GenderのcsvをName1, Name2, Name3, Genderに分割する関数
    :param file: Name-Genderファイルパス
    :return: df 名前分割後のdf
    """
    df = pd.read_csv(file, encoding="cp932")

    #同じ名前を削除
    namelist = df["Name"].tolist()
    for name in namelist:
        df.at[namelist.index(name), "Name"] = name
    df = df.dropna(subset=["Name"])

    #文字の取り出し
    namelist = df["Name"].tolist()
    for name in namelist:
        df.at[namelist.index(name), "Name1"] = name[0]   #1文字目
        if len(name) > 1:
            df.at[namelist.index(name), "Name2"] = name[1]    #2文字目
        else:
            df.at[namelist.index(name), "Name2"] = "0"    #2文字目ない場合
        if len(name) > 2:
            df.at[namelist.index(name), "Name3"] = name[2]   #3文字目
        else:
            df.at[namelist.index(name), "Name3"] = "0"   #3文字目ない場合

    df = df.dropna(subset=["Name1"])
    df = df.fillna("0")
    df = df[["Name1", "Name2", "Name3", "Gender"]]
    df = df.reset_index(drop=True)
    print(df)
    return df

if __name__ == "__main__":  #デバッグ実験用　普通はここは使わない
#    file = config(0)
    df = NameSpli("/Users/satoushoutaakira/Documents/Database_test.csv")
    df.to_csv("/Users/satoushoutaakira/Documents/Database_test2.csv", encoding='cp932', index=False)
