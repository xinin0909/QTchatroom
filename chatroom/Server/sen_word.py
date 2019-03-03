def filter_words(path):
    words = set()
    try:
        f = open(path, 'rt', encoding="utf8")
    except OSError:
        print("文件打开失败")
    else:
        while True:
            w = f.readline()[:-1]
            if w:
                words.add(w)
            else:
                break
    return words


def sense_words(text):
    words = filter_words('filterWords.txt')
    while True:
        for i in words:
            if i in text:
                replace = ''
                for j in range(len(i)):
                    replace = replace+'*'
                text = text.replace(i, replace)
        return text


if __name__ == "__main__":
    print(sense_words("你麻痹"))
