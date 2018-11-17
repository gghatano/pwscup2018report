# pwscup2018report

PWSCup2018の報告論文作業

## ディレクトリ構成

```
.
├── data : データセット
├── image : 可視化用の画像出力
├── paper: 論文
└── utility: 有用性評価スクリプト
```

## 進捗
- 残タスク
-- https://github.com/gghatano/pwscup2018report/projects/1

## 利用手順(予定)

1. pyhon3.6を用意する

2. パッケージのインストール
```pyhton
$ pip install -r requitements.txt
```

3. data/以下に、評価対象のデータを配置する

4. 有用性評価スクリプトをを実行する
```python
$ python3 ./utlity/
```

5. paper/utility/result_(実行日時).csv に評価結果が出力される

```bash
$ cat paper/utility/result_......csv
ID, filename, utility1, utility2, utility3, ...
1, A1_01_0.csv, 0.1, 0.2, 0.4, ....
2, A1_01_10.csv, 0.23, 0.45, 0.67, ....

```
