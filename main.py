
mode = {"Learn":"Start learn", "main":"Start main", "exit":"fin."}

def start():
    print("モード選択")
    command = input("学習:Learn, 判定：main >>")
    try:
        mode[command]
    except KeyError:
        print("コマンドが違います。")
        start()

if __name__ == "__main__":
    start()