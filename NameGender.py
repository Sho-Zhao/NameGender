import pickle

from sklearn.metrics import confusion_matrix, precision_score
from sklearn.model_selection import train_test_split

from config import config
import pandas as pd
from func import dfstrtoint, split_test
import xgboost as xgb

class NameGender:
    def __init__(self):
        self.file = config(0)
        self.param = config(1)
        self.file_pred = config(2)
        self.X_col = ["Name10", "Name11", "Name20", "Name21", "Name30", "Name31"]
        self.y_col = ["Gender"]
        self.df = None
        self.train_set = None
        self.test_set = None
        self.bst = None
        self.gender = "未判定"

    def _NameSplit(self):
        """
        self.df の名前を分割してName1, Name2, Name3, Genderにする。
        :return: self.dfが変化
        """
        # 同じ名前を削除
        namelist = self.df["Name"].tolist()
        for name in namelist:
            self.df.at[namelist.index(name), "Name"] = name
        self.df = self.df.dropna(subset=["Name"])

        # 文字の取り出し
        namelist = self.df["Name"].tolist()
        for name in namelist:
            self.df.at[namelist.index(name), "Name1"] = name[0]  # 1文字目
            if len(name) > 1:
                self.df.at[namelist.index(name), "Name2"] = name[1]  # 2文字目
            else:
                self.df.at[namelist.index(name), "Name2"] = "0"  # 2文字目ない場合
            if len(name) > 2:
                self.df.at[namelist.index(name), "Name3"] = name[2]  # 3文字目
            else:
                self.df.at[namelist.index(name), "Name3"] = "0"  # 3文字目ない場合

        #dfの整形
        self.df = self.df.dropna(subset=["Name1"])
        self.df = self.df.fillna("0")
        self.df = self.df[["Name1", "Name2", "Name3", "Gender"]]
        self.df = self.df.reset_index(drop=True)

    def _NameEncode(self):
        """
        :param df_dec: 名前をエンコードする前のdfもしくはcsvファイルパス
        :return: エンコード済みのdf
        """
        Namelist = {"Name1": ["Name10", "Name11"], "Name2": ["Name20", "Name21"],
                    "Name3": ["Name30", "Name31"]}  # 2次元のエンコードのため、1文字を2次元に変換

        for row in range(len(self.df)):
            for name in Namelist:  # Name1から3を取り出し
                encoded = dfstrtoint(self.df, row, name)
                self.df.at[row, Namelist[name][0]] = encoded[0]
                self.df.at[row, Namelist[name][1]] = encoded[1]

        col_list = ["Name10", "Name11", "Name20", "Name21", "Name30", "Name31", "Gender"]
        self.df = self.df[col_list]

    def learn(self, param, num_round):
        """
        学習メソッド
        :param param:paramの中から使用するparam名を入力
        :param num_round:学習回数を入力
        :return:self.bstを学習済モデルにする
        """
        self.df = pd.read_csv(self.file["path_db"], encoding="cp932")

        self._NameSplit()
        self._NameEncode()

        #訓練セットとテストセットの分割
        self.train_set, self.test_set = split_test(self.df)

        # データのXY分割
        X_train, y_train = self.train_set[self.X_col], self.train_set[self.y_col]
        X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.1)  # validデータの分割

        # XGBoostによる学習
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dvalid = xgb.DMatrix(X_valid, label=y_valid)
        evalist = [(dvalid, 'eval'), (dtrain, 'train')]
        self.bst = xgb.train(self.param[param], dtrain, num_round, evalist, early_stopping_rounds=5)
        print('Best Score:{0:.4f}, Iteratin:{1:d}, Ntree_Limit:{2:d}'.format(
            self.bst.best_score, self.bst.best_iteration, self.bst.best_ntree_limit))

    def test_model(self):

        # データのXY分割
        X_test, y_test = self.test_set[self.X_col], self.test_set[self.y_col]

        # テストと成績の出力
        dtest = xgb.DMatrix(X_test)
        pred = self.bst.predict(dtest, ntree_limit=self.bst.best_ntree_limit)
        conf_ma = confusion_matrix(y_test, pred)
        prec_score = precision_score(y_test, pred)
        print(conf_ma)
        print(prec_score)

    def save_model(self):
        pickle.dump(self.bst, open(self.file["path_result"] + "model.pickle", "wb"))

    def predict_gender(self, pred_name):
        """
        predictモード　入力された名前から性別をだす
        :param pred_name: 性別が知りたい名前
        :return: 性別
        """
        #入力された名前をdf化
        self.df = pd.DataFrame(data={
            "Name": [pred_name],
            "Gender": [0]
        })

        #名前の分割とエンコード
        self._NameSplit()
        self._NameEncode()

        X_pred = xgb.DMatrix(self.df[self.X_col])
        load_model = pickle.load(open(self.file["path_result"]+"model.pickle", "rb"))
        y_pred = load_model.predict(X_pred)
        if y_pred == 0:
            self.gender = "男性"
        elif y_pred == 1:
            self.gender = "女性"