import tarfile
import zipfile


class TarReader:
    """Easily read tar file without unzipping it.

    Returns:
        result: Contents of the read file.
        result1: List of files in tar.
        result2: List of files in tar which is in tar.
    """

    def __init__(self, file_main, file_compressed_1=None, file_compressed_2=None, mode="utf-8"):
        """Initialize TarReader class.

        Args:
            file_main (str): Tar's file name.
            file_compressed_1 (str, optional): File name in Tar's file.
            file_compressed_2 (str, optional): File name in file_compressed_1.
            mode (str, optional): Encoding parameters. Defaults to "utf-8".
        """
        self.file_main = file_main
        self.file_compressed_1 = file_compressed_1
        self.file_compressed_2 = file_compressed_2
        self.mode = mode

        self._tar = None
        self._tar1 = None
        self._tar2 = None
        self._tar3 = None

    def __enter__(self):
        """For with command.
        
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """For with command.

        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            traceback: The exception traceback information.
        """
        self.close()

    def open(self):
        """Open tar file.
        """
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
        """Close tar file.
        """
        self._tar.close()

        # ネストされたファイルの有無確認
        if self.file_compressed_2 is not None:
            self._tar3.close()

        self._tar2.close()
        self._tar1.close()

    def read(self, size=-1):
        """Same function as standard read command.

        Args:
            size (int, optional): Read file or read file to size if you want. Defaults to -1.

        Returns:
            string: Contents of file with decode.
        """
        result = self._tar.read(size).decode(self.mode)
        return result

    def readline(self):
        """Same function as standard readline command.

        Returns:
            string: One sentence of file with decode.
        """
        result = self._tar.readline().rstrip().decode(self.mode)
        return result

    def readlines(self):
        """Same function as standard readlines command.

        Returns:
            list of string: All sentences of file with decode.
        """
        result = []
        temp = self._tar.readlines()
        for i in temp:
            result.append(i.rstrip().decode(self.mode))
        return result

    def getmembers(self):
        """Get file name in tar file.

        Returns:
            list of string: file names
        """

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

            # 2次元リストとして値を戻す
            return [result1, resutl2]


class ZipReader:
    """Easily read zip file without unzipping it.

    Returns:
        result: Contents of the read file.
        result1: List of files in zip.
        result2: List of files in zip which is in zip.
    """

    def __init__(self, file_main, file_compressed_1=None, file_compressed_2=None, mode="utf-8"):
        """Initialize ZipReader class.

        Args:
            file_main (str): zip's file name.
            file_compressed_1 (str, optional): File name in zip's file.
            file_compressed_2 (str, optional): File name in file_compressed_1.
            mode (str, optional): Encoding parameters. Defaults to "utf-8".
        """
        self.file_main = file_main
        self.file_compressed_1 = file_compressed_1
        self.file_compressed_2 = file_compressed_2
        self.mode = mode

        self._zip = None
        self._zip1 = None
        self._zip2 = None
        self._zip3 = None

    def __enter__(self):
        """For with command.
        
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """For with command.

        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            traceback: The exception traceback information.
        """
        self.close()

    def open(self):
        """Open tar file.
        """
        # 多重ループを抜けるため
        flag = False

        # zipファイルの読み出し
        self._zip1 = zipfile.ZipFile(self.file_main)

        # zipファイル内から特定ファイルを読み出す
        for i in self._zip1.infolist():
            
            if self.file_compressed_1 in i.filename:
                
                self._zip2 = self._zip1.open(i.filename)

                # ネストされたファイルの有無で分岐
                if self.file_compressed_2 is None:
                    
                    self._zip = self._zip2
                    flag = True
                else:
                    
                    self._zip3 = zipfile.ZipFile(self._zip2)

                    for ii in self._zip3.infolist():
                        
                        if self.file_compressed_2 in ii.filename:
                            
                            self._zip = self._zip3.open(ii.filename)
                            flag = True
                            break
            if flag:
                break

    def close(self):
        """Close zip file.
        """
        self._zip.close()

        # ネストされたファイルの有無確認
        if self.file_compressed_2 is not None:
            self._zip3.close()

        self._zip2.close()
        self._zip1.close()

    def read(self, size=-1):
        """Same function as standard read command.

        Args:
            size (int, optional): Read file or read file to size if you want. Defaults to -1.

        Returns:
            string: Contents of file with decode.
        """
        result = self._zip.read(size).decode(self.mode)
        return result

    def readline(self):
        """Same function as standard readline command.

        Returns:
            string: One sentence of file with decode.
        """
        result = self._zip.readline().rstrip().decode(self.mode)
        return result

    def readlines(self):
        """Same function as standard readlines command.

        Returns:
            list of string: All sentences of file with decode.
        """
        result = []
        temp = self._zip.readlines()
        for i in temp:
            result.append(i.rstrip().decode(self.mode))
        return result

    def getmembers(self):
        """Get file name in zip file.

        Returns:
            list of string: file names
        """

        result1 = []
        resutl2 = []

        # tarファイルの読み出し
        self._zip1 = zipfile.ZipFile(self.file_main)

        # tarファイル内がネストしているか確認する
        if self.file_compressed_1 is None:
            # ネストしていない場合
            for i in self._zip1.infolist():
                result1.append(i.filename)

            # 終了処理
            self._zip1.close()

            return result1

        else:
            # ネストしている場合
            for i in self._zip1.infolist():
                result1.append(i.filename)
                if self.file_compressed_1 in i.filename:
                    # ネストしているファイル内を読み込む
                    self._zip2 = self._zip1.open(i.filename)
                    self._zip3 = zipfile.ZipFile(self._zip2)

                    for ii in self._zip3.infolist():
                        resutl2.append(ii.filename)

            # 終了処理
            self._zip3.close()
            self._zip2.close()
            self._zip1.close()

            # 2次元リストとして値を戻す
            return [result1, resutl2]


def main():

    # How to use
    # In the case of tar file
    # Read all
    with TarReader("sample.tgz", "a.txt") as t:
        print(t.read())

    # Read to 10 words
    with TarReader("sample.tgz", "b.txt") as t:
        print(t.read(10))

    # Read in readline
    with TarReader("sample.tgz", "bbb.tgz", "c.txt") as t:
        while (result := t.readline()):
            print(result)
    
    # Read in readlines
    with TarReader("sample.tgz", "bbb.tgz", "d.txt") as t:
        result = t.readlines()
        print(result)

    # Get filenames in tar file
    result = TarReader("sample.tgz", "bbb.tgz").getmembers()
    print(result)

    # How to use
    # In the case of zip file
    with ZipReader("sample.zip", "bbb.zip", "dd.txt")as z:
        print(z.read())

    with ZipReader("sample.zip", "aa.txt")as z:
        print(z.readlines())

    result = ZipReader("sample.zip", "bbb.zip").getmembers()
    print(result)


if __name__ == "__main__":
    main()
