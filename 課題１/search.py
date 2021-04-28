import csv


def search(path):
    word = input("鬼滅の刃の登場人物の名前を入力してください >>>")
    source = []

    with open(path, encoding="utf_8") as f:
        source = f.read().split(",")

    if word in source:
        print(f"{word}が見つかりました")
    else:
        source.append(word)
        with open(path, "w") as wf:
            writer = csv.writer(wf)
            writer.writerow(source)

        print(f"{word}を追加しました")


if __name__ == "__main__":

    path = "課題１/data.csv"

    search(path)
