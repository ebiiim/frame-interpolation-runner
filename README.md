# frame-interpolation-runner

2フレームから中間フレームを生成する[pytorch-sepconv](https://github.com/sniklaus/pytorch-sepconv)にディレクトリを丸ごと突っ込むためのツール

## Usage

```bash
python run.py ./input ./output l1
```

- 第1引数は入力ディレクトリ e.g. `./input` 
    - 連番のpngを想定 e.g. `00000001.png` `00000002.png`
    - 上記以外でも昇順なら動くはずです（`os.listdir()` -> `list.sort()`しています）
- 第2引数は出力ディレクトリ e.g. `./output`
    - 連番のpngを出力します
- 第3引数はpytorch-sepconvのLoss Function `l1` or `lf`

## Installation

- Requirements
    - CUDA 9 (9.2確認済)
    - Python 2.7
    - Python 3 (3.5確認済)

1: Requirementsを満たします

省略

2: pytorch-sepconvを用意します

（本リポジトリをcloneした後に）

```bash
cd frame-interpolation-runner
git clone https://github.com/sniklaus/pytorch-sepconv.git
```

```
.
├── pytorch-sepconv
├── README.md
├── requirements.txt
├── run.py
└── sepconv.sh
```

Python 2.7のvirtualenvで仮想環境`venv`を用意し、requirementsをインストールします。

```bash
cd pytorch-sepconv
bash download.bash

python -V
# Python 2.7.x

sudo apt install python-pip
sudo apt install python-virtualenv
virtualenv venv
. venv/bin/activate

pip install numpy pillow torch cupy

python run.py --model lf --first ./images/first.png --second ./images/second.png --out ./result.png
```

3: 入力ディレクトリを用意して実行します

```bash
cd ..

python3 -V
# Python 3.x.y

python3 run.py ./input ./output l1
```

FFmpegなどで出力ファイルを動画に変換できます。
