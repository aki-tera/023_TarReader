import tarfile
import zipfile


class TarReader:
    """Easily read tar file without unzipping it.

    Returns:
        result: Contents of the read file.
        file_name_array_1: List of files in tar.
        file_name_array_2: List of files in tar which is in tar.
    """

    def __init__(self, target_file, file_compressed_1=None, file_compressed_2=None, coding_name="utf-8"):
        """Initialize TarReader class.

        Args:
            target_file (str): Tar's file name.
            file_compressed_1 (str, optional): File name in Tar's file.
            file_compressed_2 (str, optional): File name in file_compressed_1.
            coding_name (str, optional): Encoding parameters. Defaults to "utf-8".
        """
        self.target_file = target_file
        self.file_compressed_1 = file_compressed_1
        self.file_compressed_2 = file_compressed_2
        self.coding_name = coding_name

        self.tar_object_1 = None
        self.tar_object_2 = None
        self.tar_object_3 = None
        self.tar_object_target = None

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
        is_break_loop = False

        # tarファイルの読み出し
        self.tar_object_1 = tarfile.open(self.target_file)

        # tarファイル内から特定ファイルを読み出す
        for i in self.tar_object_1.getmembers():
            
            if self.file_compressed_1 in i.name:
                
                self.tar_object_2 = self.tar_object_1.extractfile(i)

                # ネストされたファイルの有無で分岐
                if self.file_compressed_2 is None:
                    
                    self.tar_object_target = self.tar_object_2
                    is_break_loop = True
                else:
                    
                    self.tar_object_3 = tarfile.open(fileobj=self.tar_object_2)

                    for ii in self.tar_object_3.getmembers():
                        
                        if self.file_compressed_2 in ii.name:
                            
                            self.tar_object_target = self.tar_object_3.extractfile(ii)
                            is_break_loop = True
                            break
            if is_break_loop:
                break

    def close(self):
        """Close tar file.
        """
        self.tar_object_target.close()

        # ネストされたファイルの有無確認
        if self.file_compressed_2 is not None:
            self.tar_object_3.close()

        self.tar_object_2.close()
        self.tar_object_1.close()

    def read(self, size=-1):
        """Same function as standard read command.

        Args:
            size (int, optional): Read file or read file to size if you want. Defaults to -1.

        Returns:
            string: Contents of file with decode.
        """
        result = self.tar_object_target.read(size).decode(self.coding_name)
        return result

    def readline(self, size=-1):
        """Same function as standard readline command.

        Returns:
            string: One sentence of file with decode.
        """
        result = self.tar_object_target.readline(size).rstrip().decode(self.coding_name)
        return result

    def readlines(self, hint=-1):
        """Same function as standard readlines command.

        Returns:
            list of string: All sentences of file with decode.
        """
        result = []
        temp = self.tar_object_target.readlines(hint)
        for i in temp:
            result.append(i.rstrip().decode(self.coding_name))
        return result

    def getmembers(self):
        """Get file name in tar file.

        Returns:
            list of string: file names
        """

        file_name_array_1 = []
        file_name_array_2 = []

        # tarファイルの読み出し
        self.tar_object_1 = tarfile.open(self.target_file)

        # tarファイル内がネストしているか確認する
        if self.file_compressed_1 is None:
            # ネストしていない場合
            for i in self.tar_object_1.getmembers():
                file_name_array_1.append(i.name)

            # 終了処理
            self.tar_object_1.close()

            return file_name_array_1

        else:
            # ネストしている場合
            for i in self.tar_object_1.getmembers():
                file_name_array_1.append(i.name)
                if self.file_compressed_1 in i.name:
                    # ネストしているファイル内を読み込む
                    self.tar_object_2 = self.tar_object_1.extractfile(i)
                    self.tar_object_3 = tarfile.open(fileobj=self.tar_object_2)

                    for ii in self.tar_object_3.getmembers():
                        file_name_array_2.append(ii.name)

            # 終了処理
            self.tar_object_3.close()
            self.tar_object_2.close()
            self.tar_object_1.close()

            # 2次元リストとして値を戻す
            return [file_name_array_1, file_name_array_2]


class ZipReader:
    """Easily read zip file without unzipping it.

    Returns:
        result: Contents of the read file.
        file_name_array_1: List of files in zip.
        file_name_array_2: List of files in zip which is in zip.
    """

    def __init__(self, target_file, file_compressed_1=None, file_compressed_2=None, coding_name="utf-8"):
        """Initialize ZipReader class.

        Args:
            target_file (str): zip's file name.
            file_compressed_1 (str, optional): File name in zip's file.
            file_compressed_2 (str, optional): File name in file_compressed_1.
            coding_name (str, optional): Encoding parameters. Defaults to "utf-8".
        """
        self.target_file = target_file
        self.file_compressed_1 = file_compressed_1
        self.file_compressed_2 = file_compressed_2
        self.coding_name = coding_name

        self.zip_object_1 = None
        self.zip_object_2 = None
        self.zip_object_3 = None
        self.zip_object_target = None

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
        is_break_loop = False

        # zipファイルの読み出し
        self.zip_object_1 = zipfile.ZipFile(self.target_file)

        # zipファイル内から特定ファイルを読み出す
        for i in self.zip_object_1.infolist():
            
            if self.file_compressed_1 in i.filename:
                
                self.zip_object_2 = self.zip_object_1.open(i.filename)

                # ネストされたファイルの有無で分岐
                if self.file_compressed_2 is None:
                    
                    self.zip_object_target = self.zip_object_2
                    is_break_loop = True
                else:
                    
                    self.zip_object_3 = zipfile.ZipFile(self.zip_object_2)

                    for ii in self.zip_object_3.infolist():
                        
                        if self.file_compressed_2 in ii.filename:
                            
                            self.zip_object_target = self.zip_object_3.open(ii.filename)
                            is_break_loop = True
                            break
            if is_break_loop:
                break

    def close(self):
        """Close zip file.
        
        """
        self.zip_object_target.close()

        # ネストされたファイルの有無確認
        if self.file_compressed_2 is not None:
            self.zip_object_3.close()

        self.zip_object_2.close()
        self.zip_object_1.close()

    def read(self, size=-1):
        """Same function as standard read command.

        Args:
            size (int, optional): Read file or read file to size if you want. Defaults to -1.

        Returns:
            string: Contents of file with decode.
        """
        result = self.zip_object_target.read(size).decode(self.coding_name)
        return result

    def readline(self, size=-1):
        """Same function as standard readline command.

        Returns:
            string: One sentence of file with decode.
        """
        result = self.zip_object_target.readline(size).rstrip().decode(self.coding_name)
        return result

    def readlines(self, hint=-1):
        """Same function as standard readlines command.

        Returns:
            list of string: All sentences of file with decode.
        """
        result = []
        temp = self.zip_object_target.readlines(hint)
        for i in temp:
            result.append(i.rstrip().decode(self.coding_name))
        return result

    def getmembers(self):
        """Get file name in zip file.

        Returns:
            list of string: file names
        """

        file_name_array_1 = []
        file_name_array_2 = []

        # tarファイルの読み出し
        self.zip_object_1 = zipfile.ZipFile(self.target_file)

        # tarファイル内がネストしているか確認する
        if self.file_compressed_1 is None:
            # ネストしていない場合
            for i in self.zip_object_1.infolist():
                file_name_array_1.append(i.filename)

            # 終了処理
            self.zip_object_1.close()

            return file_name_array_1

        else:
            # ネストしている場合
            for i in self.zip_object_1.infolist():
                file_name_array_1.append(i.filename)
                if self.file_compressed_1 in i.filename:
                    # ネストしているファイル内を読み込む
                    self.zip_object_2 = self.zip_object_1.open(i.filename)
                    self.zip_object_3 = zipfile.ZipFile(self.zip_object_2)

                    for ii in self.zip_object_3.infolist():
                        file_name_array_2.append(ii.filename)

            # 終了処理
            self.zip_object_3.close()
            self.zip_object_2.close()
            self.zip_object_1.close()

            # 2次元リストとして値を戻す
            return [file_name_array_1, file_name_array_2]


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
