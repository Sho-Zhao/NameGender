from config import config
from Learn import learn, split_test
import xgboost as xgb

if __name__ == "__main__":
    #設定読み込み
    file = config(0)
    param = config(1)

    #CUI
    print("モード選択")
    command = input("学習:Learn, 判定：main >>")

    if command == "Learn":
        train_set, test_set = split_test(file["path_to_csv"])  # テストセットを分割

        num_round = 100  # 学習回数を3通り
        parname = "param6"
        mat, score = learn(train_set, test_set, param[parname], num_round)
        filename = parname + "_" + str(num_round) + ".txt"
        with open("/Users/satoushoutaakira/Documents/Result/" + filename, "w") as f:
            f.write("学習回数:" + str(num_round) + "¥n")
            f.write(str(mat) + "¥n")
            f.write("適合率:" + str(score))

    elif command == "main":
        print("判定を作成中")

    else:
        print("Command error!")