# -*- coding: utf-8 -*-
"""create_sample_data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jy5XweBs18ib6hHpLVdzO9U5H8Xpqh7p

# 匿名化データからそれっぽいデータを作る

一般化されたセルについて、範囲から一様にサンプルして、元の扱いやすいデータを作る

1.  日付
2.  商品ID
3.  価格
4.  量

について、一般化されたものから一様にサンプルする。仮IDはそのまま使う。
"""

"""
USAGE: python3 create_sample_data.py
"""

import pandas as pd
import numpy as np
import re
import datetime
import random

# for date  sample
## 日付のサンプリングについて、fakerを使うのが楽でした
# ! pip install faker
from faker import Faker
import datetime
fake = Faker()

"""## データの準備"""

## A1_01(鋼鉄データでテストする)

### ダウンロード 
dat_anon = pd.read_csv("https://www.iwsec.org/pws/2018/submitted_data/cup18-dataset-2-A1/A1_01.csv", header=None)
dat_anon.columns = ["ID_ANON", "DATE_ANON", "ITEMID_ANON", "PRICE_ANON", "AMOUNT_ANON"]
print(dat_anon.head())


### テスト用の空データ
column_name = ["ID", "DATE", "ITEMID", "PRICE", "AMOUNT"]
dat_sample = pd.DataFrame(columns = column_name)

"""## 日付の一様サンプル"""

# 日付の一様サンプル

def sample_date(date_anon):
  # deleted
  if date_anon == "*":
    return np.nan
  
  # extract data
  date_pattern = r"[0-9]+/[0-9]+/[0-9]+"
  date_matched_list = re.findall(date_pattern, date_anon)
  
  # parse & sample
  if date_matched_list:
    if len(date_matched_list) == 1:
      return datetime.datetime.strptime(date_matched_list[0], "%Y/%m/%d")
    else:
      date_start = datetime.datetime.strptime(date_matched_list[0], "%Y/%m/%d")
      date_end = datetime.datetime.strptime(date_matched_list[1], "%Y/%m/%d")
  
      date_random = fake.date_between_dates(date_start, date_end)
      return date_random
  else:
    return np.nan
    

## TEST
print("====== sample date =====")
print(sample_date("*"))
print(sample_date("2010/12/02;2010/12/05]"))
print(sample_date("2010/12/02"))
anon_date_vec = ["[2010/12/02;2010/12/05]","2010/12/02;2010/12/05"]

dat_sample["DATE"] = list(map(lambda x: sample_date(x), dat_anon["DATE_ANON"]))

print(dat_sample.head())

"""## 商品IDの一様サンプル"""

# 商品の一様サンプル
def sample_item(item_anon):
  if(item_anon == "*"):
    return np.nan
  else:
    item_anon_list = item_anon.replace("{", "").replace("}", "").split(sep = ";")
    return random.choice(item_anon_list)

# TEST 
print("====== sample itemid =====")
print(sample_item("{AAAA;BBBB;CCCC}"))
print(sample_item("AAAA"))
print(sample_item("*"))

dat_sample["ITEMID"] = list(map(lambda x: sample_item(x), dat_anon["ITEMID_ANON"]))
print(dat_sample.head())

"""## 価格の一様サンプル

0.01刻みだっけ...
"""

# 価格の一様サンプル
def sample_price(price_anon):
  if(price_anon == "*"):
    return np.nan
  else:
    price_anon_list = price_anon.replace("[", "").replace("]", "").split(sep=";")
    if(len(price_anon_list) == 1):
      return float(price_anon_list[0])
    else:
      return round(random.uniform(float(price_anon_list[0]), float(price_anon_list[1])), 2)
  
## TEST
print("====== sample price =====")
print(sample_price("*"))
print(sample_price("[10;20]"))
print(sample_price("10"))

dat_sample["PRICE"] = list(map(lambda x: sample_price(x), dat_anon["PRICE_ANON"]))

print(dat_sample.head())

# 数量の一様サンプル
def sample_amount(amount_anon):
  if(amount_anon == "*"):
    return np.nan
  else:
    amount_anon_list = amount_anon.replace("[", "").replace("]", "").split(sep=";")
    if(len(amount_anon_list) == 1):
      return int(amount_anon_list[0])
    else:
      return random.randint(int(amount_anon_list[0]), int(amount_anon_list[1]))

## TEST
print("====== sample amount =====")
print(sample_amount("*"))
print(sample_amount("[1;20]"))
print(sample_amount("1"))

dat_sample["AMOUNT"] = list(map(lambda x: sample_amount(x), dat_anon["AMOUNT_ANON"]))
print(dat_sample.head())

"""## サンプルデータの作成
create_sample_data()を実行するだけ
"""

## まとめ


def create_sample_data(dat_anon):
  column_name = ["ID", "DATE", "ITEMID", "PRICE", "AMOUNT"]
  dat = pd.DataFrame(columns = column_name)
  dat["ID"] = dat_anon["ID_ANON"]
  dat["DATE"] = list(map(lambda x: sample_date(x), dat_anon["DATE_ANON"]))
  dat["ITEMID"] = list(map(lambda x: sample_item(x), dat_anon["ITEMID_ANON"]))
  dat["PRICE"] = list(map(lambda x: sample_price(x), dat_anon["PRICE_ANON"]))
  dat["AMOUNT"] = list(map(lambda x: sample_amount(x), dat_anon["AMOUNT_ANON"]))
  
  return dat

"""## ファイルの保存

各チームの匿名加工データに対して、データ生成を$N$回実行します

チーム数は13なので、$13N$のデータができます。

1ファイル6MB程度なので、全チームで $ 80 \text{MB} \times N$ のデータができます。N=100だと8GBになります。
"""

teamname_list = ["01", "02", "03", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"]

N = 1
for i in range(0,N):
  for teamname in teamname_list: 
    filename = "A1_" + teamname + ".csv"
    url = "https://www.iwsec.org/pws/2018/submitted_data/cup18-dataset-2-A1/" + filename
    print(i)
    print(filename)

    ## A2
    dat_anon1 = pd.read_csv(url, header=None)
    dat_anon1.columns = ["ID_ANON", "DATE_ANON", "ITEMID_ANON", "PRICE_ANON", "AMOUNT_ANON"]
    #print(dat_anon1.head())
    dat_res = create_sample_data(dat_anon1)
    #print(dat_res.head())
    
    outputfilename = "A1_" + teamname + "_" + str(i) + ".csv"
    with open(outputfilename, "w") as f:
      dat_res.to_csv(f)

