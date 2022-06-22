import pickle
import pandas as pd
from NameSplit import NameSpli
from config import config
from NameEncode import NameEncoding
import xgboost as xgb


def predict_gender(path_model):
    """
    名前から性別をpredictする関数
    :param path_model: model.pickleのpath
    :return: string 男性 or 女性
    """
    file = config(2)    #Pred用設定

    pred_name = input("あなたのお名前漢字3文字:")
    df = pd.DataFrame(data={
        "Name":[pred_name],
        "Gender":[0]
    })
    df.to_csv(file["path_db_pred"], encoding="cp932")
    df = NameSpli(file["path_db_pred"])
    df_encoded = NameEncoding(df)

    X_col = ["Name10", "Name11", "Name20", "Name21", "Name30", "Name31"]
    X_pred = xgb.DMatrix(df_encoded[X_col])
    load_model = pickle.load(open(path_model, "rb"))
    y_pred = load_model.predict(X_pred)
    if y_pred == 0:
        return "男性"
    elif y_pred == 1:
        return "女性"

if __name__ == "__main__":  #実験用
    file = config(0)
    gender = predict_gender(file["path_result"]+"model.pickle")
    print(gender)