from config import config
from Learn import learn, split_test, test_model, save_model
import pickle

if __name__ == "__main__":
    #設定読み込み
    file = config(0)
    param = config(1)

    #CUI
    print("モード選択")
    command = input("学習:Learn, 判定：main >>")

    if command == "Learn":
        train_set, test_set = split_test(file["path_to_csv"])  # テストセットを分割

        #学習　モデル作成
        num_round = 100  # 学習回数を3通り
        parname = "param6"
        model = learn(train_set, param[parname], num_round)
        save_model(model, file["path_result"])

    elif command == "main":
        print("判定を作成中")
        load_model = pickle.load(open(file["path_result"]+"model.pickle", "rb"))


    else:
        print("Command error!")