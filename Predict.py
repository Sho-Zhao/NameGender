import pickle

def predict_gender(df_encoded, path_model):
    """
    名前から性別をpredictする関数
    :param df_encoded: 名前df Encode済のもの
    :param path_model: model.pickleのpath
    :return: string 男性 or 女性
    """
    X_col = ["Name10", "Name11", "Name20", "Name21", "Name30", "Name31"]
    X_pred = df_encoded[X_col]
    load_model = pickle.load(open(path_model, "rb"))
    y_pred = load_model.predict(X_pred)
    if y_pred == 0:
        return "男性"
    elif y_pred == 1:
        return "女性"