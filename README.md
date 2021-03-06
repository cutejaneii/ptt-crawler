# ptt-crawler

本專案利用[requests](https://github.com/requests/requests)取得ptt文章

## 說明
1. 爬文數量 >= 10，啟用multi-thread (Queue數量=10) 
2. 新增[remove_words.txt](https://github.com/cutejaneii/ptt-crawler/blob/master/ptt-crawler/remove_words.txt)過濾「標題」及「回文」（文章內容不過濾），例如「三小」。偶有錯殺之文章，還請見諒，或可自行修改remove_words.txt

## 安裝條件
<pre><code>pip3 install six<br>
pip3 install beautifulsoup4<br>
pip3 install requests<br>
</code></pre>

## 安裝方法
<pre><code>$ git clone https://github.com/cutejaneii/ptt-crawler.git</code></pre>

## 使用方法

參數說明：

| 參數 | 縮寫 | 預設值 | 說明 | 
| ------ | ------ | ------ | ------ |
| board| -b | movie | 看板名稱 |
| mode | -m | 0 | 爬蟲模式<br> 0：爬最新文章<br>1：爬「某頁」到「某頁」的文章<br>2：爬「某一頁」的文章<br>3：依關鍵字爬文章 |
| from_pageno | -f | 1 | 開始頁數 |
| to_pageno | -t | 1 | 結束頁數 |
| article_id | -a | ** | 文章ID |
| count | -c | 10 | 抓取的文章數量，上限1000筆 |
| get_responses | -r | 0 | 是否要取得回覆，0代表不取，1代表取 |
| keyword | -k | Thor | 關鍵字 |

### 取得最新文章

取得「棒球版」最新10筆文章
<pre><code>$ python3 main.py -b Baseball</code></pre>
![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode_0A.png)

取得「日本旅遊版」最新5筆文章及回覆
<pre><code>$ python3 main.py -b Japan_Travel -c 5 -r 1</code></pre>
![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode_0B.png)

取得最新文章(上限為30筆)，並停止條件為「文章ID=M.1549003732.A.F78」，當取到該篇文章時，爬蟲停止。
若爬到300篇仍未取到該文章，則爬蟲停止。
注意：並不會將該篇文章爬回，只會爬到該文章的前一筆。
<pre><code>$ python3 main.py -b Japan_Travel -c 30 -a M.1549003732.A.F78</code></pre>
![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode_0C.png)

### 取得「某頁數」到「某頁數」的文章
取得「棒球版」頁數「9130」~頁數「9150」的文章
<pre><code>$ python3 main.py -b Baseball -m 1 -f 9130 -t 9150</code></pre>
![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode_1A.png)

取得「信用卡版」頁數「2951」~頁數「2952」的文章及回覆
<pre><code>$ python3 main.py -b creditcard -f 2951 -t 2952 -m 1 -r 1</code></pre>

![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode_1B.png)

### 取「某一頁」的文章
取得「信用卡版」頁數「1500」的文章
<pre><code>$ python3 main.py -b creditcard -f 1500 -m 2</code></pre>
![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode_2A.png)

### 依「關鍵字」爬文章
取得「棒球版」關鍵字為「恰恰」的文章，頁數限定在第1~3頁
<pre><code>$ python3 main.py -m 3 -b Baseball -f 1 -t 3 -k 恰恰</code></pre>
![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode3A.png)

取得「信用卡版」關鍵字為「台新」的文章及回覆，頁數限定在第5~10頁
<pre><code>$ python3 main.py -m 3 -b creditcard -f 5 -t 10 -k 台新 -r 1</code></pre>
![image](https://github.com/cutejaneii/repo_imgs/blob/master/ptt-crawler/mode3B.png)

## 效能
比較條件1：取得「電影版」頁數「3001」~頁數「3030」的文章及回覆
<pre><code>$ python3 main.py -f 3001 -t 3030 -m 1 -r 1</code></pre>
 
| 情境 | 開始時間 | 結束時間 | 花費時間 | 
| ------ | ------ | ------ | ------ |
| single thread | 2019-02-01 14:50:55.000 | 2019-02-01 14:53:33.208 | 2分38秒 |
| multi-thread | 2019-02-01 15:03:11.671 | 2019-02-01 15:04:38.429 | 1分26秒 |
