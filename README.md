
# 023_TarReader

![python3](https://img.shields.io/badge/type-python3-brightgreen)  ![passing](https://img.shields.io/badge/windows%20build-passing-brightgreen) ![MIT](https://img.shields.io/badge/license-MIT-brightgreen)  
![tar](https://img.shields.io/badge/compression-tar/tgz-red) ![zip](https://img.shields.io/badge/compression-zip-red)

## DEMO

### Compressed files are cumbersome to handle. It's even more difficult if there are compressed files within those compressed files. Here is a good news for those who are in such trouble. With this python program, you can view the text inside a compressed file `without decompressing the compressed file`.

<pre>
sample.tgz  
  ┣a.txt          <-you can read with this module!  
  ┗aaa  
    ┣b.txt        <-you can read with this module!  
    ┣aaa.tgz  
    ┗bbb.tgz  
      ┣c.txt      <-you can read with this module!  
      ┗ccc  
        ┗d.txt    <-you can read with this module!  
</pre>
  
## Features

You can view the text inside a tar file(or zip file) without decompressing the tar file(or zip file).  
Tar file is `.tar` and `.tgz`, `.tar.tgz`, and others.  
Zip file is `.zip` without password.

### specification

- can use `read` and `readline`, `readlines`.
- can get filenames in the compressed files and the compressed files in commpressed files.  

## Requirement

Python 3

- I ran this program with the following execution environment.
  - Python 3.9
  - Windows 10

## Usage

- At first, place this program in the same folder as the program you are creating.  
- It is TarReader if you read tar file.
  - It is ZipReader if you read zip file.
- Next, please show following.  
  
<img src="https://user-images.githubusercontent.com/44888139/134872684-d5fccd1a-7550-4289-bcbd-20dc785635da.png" height="285px">  <img src="https://user-images.githubusercontent.com/44888139/134873452-38ca310a-f81c-4ebb-95f5-ea1968381b8c.png" height="285px">  
  
<img src="https://user-images.githubusercontent.com/44888139/134872827-25b1cabd-155c-40c7-bb27-4eed6db59678.png" height="285px">  <img src="https://user-images.githubusercontent.com/44888139/134872873-89559e32-088d-4e4b-a665-0f64580917d8.png" height="285px">  

## License

This program is under MIT license.  
  
<br>
<br>

# 【日本語】

## 機能

圧縮ファイルのなかにある圧縮ファイルを解凍することなく読み取るプログラムです。

- 仕様
  - tarファイル(or zipファイル)の中にあるテキストを読み取ります。
  - tarファイル(or zipファイル)のさらにtarファイル(or zipファイル)内を読み取ることができます。
  - それらのファイル名を取得することができます。  

## 必要なもの

Python 3

- このプログラムは、Python 3.9とWindows10で動作確認しています。

## 使い方

1. まずこのプログラムを、あなたが作っているファイルと同じフォルダに置きます。
1. tarファイルを読みたい場合はTarReaderを使います。
   - zipファイルを読みたい場合はZipReaderを使います。
1. あとは上にある絵を見て下さい。

## ライセンス

本プログラムは、MITライセンスです。
