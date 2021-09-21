import tarfile
import re


# PEP8に準拠するとimportが先頭に行くので苦肉の策
while True:
    import sys
    sys.path.append("../000_mymodule/")
    import logger
    from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
    DEBUG_LEVEL = INFO
    break


class TarReader:
    log = logger.Logger("TarReader", level=DEBUG_LEVEL)

    def __init__(self, file_main, file_compressed_1=None, file_compressed_2=None, mode="utf-8"):
        self.file_main = file_main
        self.file_compressed_1 = file_compressed_1
        self.file_compressed_2 = file_compressed_2
        self.mode = mode

        self._tar = None
        self._tar1 = None
        self._tar2 = None
        self._tar3 = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        # 多重ループを抜けるため
        flag = False

        # tarファイルの読み出し
        self._tar1 = tarfile.open(self.file_main)

        # tarファイル内から特定ファイルを読み出す
        for i in self._tar1.getmembers():
            self.log.debug(i)
            if self.file_compressed_1 in i.name:
                
                self._tar2 = self._tar1.extractfile(i)

                # ネストされたファイルの有無で分岐
                if self.file_compressed_2 is None:
                    
                    self._tar = self._tar2
                    flag = True
                else:
                    
                    self._tar3 = tarfile.open(fileobj=self._tar2)

                    for ii in self._tar3.getmembers():

                        self.log.debug(ii)
                        if self.file_compressed_2 in ii.name:
                            
                            self._tar = self._tar3.extractfile(ii)
                            flag = True
                            break
            if flag:
                break

    def close(self):
        self._tar.close()

        # ネストされたファイルの有無確認
        if self.file_compressed_2 is not None:
            self._tar3.close()

        self._tar2.close()
        self._tar1.close()

    def read(self, size=-1):
        result = self._tar.read(size).decode(self.mode)
        return result

    def readline(self):
        result = self._tar.readline().rstrip().decode(self.mode)
        return result

    def readlines(self):
        result = []
        temp = self._tar.readlines()
        for i in temp:
            result.append(i.rstrip().decode(self.mode))
        return result

    def getmembers(self):
        self.log.info(f"file_main:{self.file_main}")
        self.log.info(f"file_compressed_1:{self.file_compressed_1}")
        self.log.info(f"file_compressed_2:{self.file_compressed_2}")
        result1 = []
        resutl2 = []

        # tarファイルの読み出し
        self._tar1 = tarfile.open(self.file_main)

        # tarファイル内がネストしているか確認する
        if self.file_compressed_1 is None:

            # ネストしていない場合
            for i in self._tar1.getmembers():
                result1.append(i.name)

            # 終了処理
            self._tar1.close()
            self.log.info(f"result1:{result1}")

            return result1

        else:
            # ネストしている場合
            for i in self._tar1.getmembers():

                result1.append(i.name)

                if self.file_compressed_1 in i.name:
                    # ネストしているファイル内を読み込む
                    self._tar2 = self._tar1.extractfile(i)
                    self._tar3 = tarfile.open(fileobj=self._tar2)

                    for ii in self._tar3.getmembers():
                        resutl2.append(ii.name)

            # 終了処理
            self._tar3.close()
            self._tar2.close()
            self._tar1.close()

            self.log.info(f"result1:{result1}")
            self.log.info(f"result2:{resutl2}")

            # 2次元リストとして値を戻す
            return [result1, resutl2]


def main():
    # 使い方の例
    # まとめて読み込む
    with TarReader("aaa.tgz", "bbb.tgz", "d.txt") as t:
        print(t.read())

    # 10文字分を読み込む
    with TarReader("aaa.tgz", "bbb.tgz", "c.txt") as t:
        print(t.read(10))

    # readlineで読み込む
    with TarReader("aaa.tgz", "b.txt") as t:
        while (result := t.readline()):
            print(result)
    
    # readlinesで読み込む
    with TarReader("aaa.tgz", "a.txt", ) as t:
        result = t.readlines()
        print(result)

    # tar内のファイル一覧
    result = TarReader("aaa.tgz", "bbb.tgz").getmembers()
    print(result)


if __name__ == "__main__":
    main()
