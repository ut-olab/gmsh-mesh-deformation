# mesh-deformation

メッシュ変形のための C#コードと gmsh コード

# 使っているもの

- gmsh
  - [gmsh のサイト](https://gmsh.info/#Links)
  - [gitlab にあるソースコード](https://gitlab.onelab.info/gmsh/gmsh)
- 自作コード（c#）

## Basic Installation

- python3 系がインストールされている必要があります。筆者は python3.11 を利用している。
  python のライブラリである、数値計算を高速に扱うための「numpy」と gmsh を利用可能にするための「gmsh」を追加する必要があります。バージョンの違いをなくすために以下のように gmsh のバージョンを 4.11.1 としてライブラリを追加してください。
  <span style="color: red;">**_先頭のドル記号は入力不要です。_**</span>

  ```bash
  # on your windows pc

  #バージョンを揃えるために一度gmshをアンインストールします。
  $ pip3 uninstall gmsh

  $ pip3 install numpy
  # または、pip install numpy
  $ pip3 install gmsh==4.11.1
  # または、pip3 install gmsh==4.11.1

  # python3系なので、pip3でインストールしたほうがよいと思います。
  # pipとpip3の違いはよくわからないので、各自調べてください。
  ```

- 以下のコマンドを入力して、以下のような出力が返ってきたら、無事にライブラリに追加されています。

  ```bash
  # on your windows pc

  # 入力
  $ pip3 list
  # 出力
  Package    Version
  ---------- -------
  gmsh       4.11.1
  numpy      1.23.4
  pip        22.3
  setuptools 65.5.0
  ```

## tutorial

- [python サンプルコードがいっぱいある場所](./gmsh-4.11.1-Windows64/tutorials/python)
- これを一個ずつ試して行けば大体やっていることはわかる
