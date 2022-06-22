import pandas as pd
from config import config

def NameSpli(file):
    df = pd.read_excel(file, sheet_name=1)
    oriName = df["Ori"].tolist()

    #姓名から名前を取り出す

    for name in oriName:
        spiname = name.split()
        df.iat[oriName.index(name), 1] = spiname[1]

    #同じ名前を削除
    namelist = df["Name"].tolist()
    for name in namelist:
        df.iat[namelist.index(name), 1] = name
    df = df.dropna(subset=["Name"])

    #文字の取り出し
    namelist = df["Name"].tolist()
    for name in namelist:
        df.iat[namelist.index(name), 2] = name[0]   #1文字目
        if len(name) > 1:
            df.iat[namelist.index(name), 3] = name[1]    #2文字目
        if len(name) > 2:
            df.iat[namelist.index(name), 4] = name[2]   #3文字目
    df = df.dropna(subset=["Name1"])
    df = df.fillna("0")
    df = df.reset_index(drop=True)
    print(df)
    return df

if __name__ == "__main__":  #デバッグ実験用　普通はここは使わない
    file = config()
    df = NameSpli(file["path_ori_db"])
    df.to_csv("/Users/satoushoutaakira/Documents/Database_Name.csv", encoding='cp932', index=False)
