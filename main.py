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
        nage.learn("param6", 100)
        nage.test_model()
        nage.save_model()

    elif command == "main":
        pred_name = input("あなたのお名前は？")
        nage.predict_gender(pred_name)
        print(pred_name)
        print(nage.gender)

    elif command == "test": #100回テスト用
        pred_name = "将太朗"
        for i in range(100):
            nage.predict_gender(pred_name)
            print(nage.gender)
    else:
        print("Command error!")