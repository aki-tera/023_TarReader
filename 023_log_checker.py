import tarfile
import re


class TarReader:

    def __init__(self, file_main, file_compressed_1, file_compressed_2=None, mode="utf-8"):
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
            if self.file_compressed_1 in i.name:
                
                self._tar2 = self._tar1.extractfile(i)

                # ネストされたファイルの有無で分岐
                if self.file_compressed_2 is None:
                    
                    self._tar = self._tar2
                    flag = True
                else:
                    
                    self._tar3 = tarfile.open(fileobj=self._tar2)

                    for ii in self._tar3.getmembers():
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
        result = self._tar.readlines()
        return result



def main():
    with TarReader("esd_xc.tgz", "prm.tgz", "systemcfg.xml") as t:
        pattern2 = "<BlockId>.*</BlockId>"
        for i in range(10):
            print(t.readline()+"**")
        #results2 = re.findall(pattern2, t.read())
        #for i in results2:
        #    print(i + "\n")


if __name__ == "__main__":
    main()
