import NameGender
from config import config
from Learn import learn, split_test, test_model, save_model
import pickle
from NameGender import NameGender

if __name__ == "__main__":
    #インスタンス
    nage = NameGender()

    #CUI
    print("モード選択")
    command = input("学習:Learn, 判定：main >>")

    if command == "Learn":
        nage.NameSplit()
        nage.NameEncode()
        nage.learn("param6", 100)
        nage.test_model()
        nage.save_model()

    elif command == "main":
        print("判定を作成中")
        #load_model = pickle.load(open(file["path_result"]+"model.pickle", "rb"))

    else:
        print("Command error!")