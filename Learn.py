from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
from sklearn.metrics import confusion_matrix, precision_score
from config import config
import pandas as pd
import xgboost as xgb

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

    #GenderでStratifiedテスト分割
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
    for train_index, test_index in split.split(df, df["Gender"]):
        strat_train_set = df.loc[train_index]
        strat_test_set = df.loc[test_index]

    return strat_train_set, strat_test_set

def learn(train_set, test_set, param, num_round):
    """
    学習する関数
    :param train_set: 訓練セット
    :param test_set: テストセット
    :return: 学習済みモデル
    """
    #データのXY分割
    X_col = ["Name10", "Name11", "Name20", "Name21", "Name30", "Name31"]
    y_col = ["Gender"]
    X_train, X_test, y_train, y_test = train_set[X_col], test_set[X_col], train_set[y_col], test_set[y_col]
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.1) #validデータの分割

    #XGBoostによる学習
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dvalid = xgb.DMatrix(X_valid, label=y_valid)
    evalist = [(dvalid, 'eval'), (dtrain, 'train')]
    bst = xgb.train(param, dtrain, num_round, evalist, early_stopping_rounds=5)
    print('Best Score:{0:.4f}, Iteratin:{1:d}, Ntree_Limit:{2:d}'.format(
     bst.best_score, bst.best_iteration, bst.best_ntree_limit))

    #テスト
    dtest = xgb.DMatrix(X_test)
    pred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)
    conf_ma = confusion_matrix(y_test, pred)
    prec_score = precision_score(y_test, pred)
    return conf_ma, prec_score

if __name__ == "__main__":
    file = config(0)    #設定
    param = config(1)   #学習パラメータ

    train_set, test_set = split_test(file["path_to_csv"])   #テストセットを分割

    num_rounds = [100, 1000, 10000] #学習回数を3通り
    for num_round in num_rounds:
        for parname in param:
            print(parname)
            mat, score = learn(train_set, test_set, param[parname], num_round)
            filename = parname+"_"+str(num_round)+".txt"
            with open("/Users/satoushoutaakira/Documents/Result/"+filename, "w") as f:
                f.write("学習回数:"+str(num_round)+"/n")
                f.write(str(mat)+"/n")
                f.write("適合率:"+str(score))