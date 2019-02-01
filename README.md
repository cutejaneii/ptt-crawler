# ptt-crawler

本專案利用[requests](https://github.com/requests/requests)取得ptt文章

## 說明
1. 爬文數量 >= 10，啟用multi-thread (Queue數量=10) 
2. 新增[remove_words.txt](https://github.com/cutejaneii/ptt-crawler/blob/master/ptt-crawler/remove_words.txt)過濾「標題」及「回文」（文章內容不過濾），例如「三小」。偶有錯殺之文章，還請見諒，或可自行修改remove_words.txt


## 安裝方法
<pre><code>$ git clone https://github.com/cutejaneii/ptt-crawler.git</code></pre>

## 使用方法

參數說明：

| 參數 | 縮寫 | 預設值 | 說明 | 
| ------ | ------ | ------ | ------ |
| board| -b | movie | 看板名稱 |
| mode | -m | 0 | 爬蟲模式<br> 0：爬最新文章<br>1：爬「某頁」到「某頁」的文章<br>2：爬「某一頁」的文章<br>3：爬「幾」天內的文章<br>4：依關鍵字爬文章 |
| from_pageno | -f | 1 | 開始頁數 |
| to_pageno | -t | 1 | 結束頁數 |
| article_id | -a | 1 | 文章ID |
| count | -c | 10 | 抓取的文章數量，上限100筆 |
| get_responses | -r | 0 | 是否要取得回覆，0代表不取，1代表取 |
| keyword | -k | KFC | 關鍵字 |
| days | -d | 1 | 天數 |

### 取得最新文章

取得最新的文章(上限為100筆)，不設定條件。

<pre><code>from ptt_crawler import ptt_crawler
A
B</code></pre>

<pre><code>from ptt_crawler import ptt_crawler
A
B</code></pre>


取得最新文章(上限為100筆)，並停止條件為「某篇文章」，當取到該篇文章時，爬蟲停止。
若爬到100篇仍未取到該文章，則爬蟲停止。
注意：並不會將該篇文章爬回，只會爬到該文章的前一筆。

<pre><code>from ptt_crawler import ptt_crawler
A
B</code></pre>


<pre><code>git clone </code></pre>

### 取得「某頁數」到「某頁數」的文章
取得「棒球版」頁數「9130」~頁數「9150」的文章
<pre><code>$ python3 main.py -b baseball -m 1 -f 9130 -t 9150</code></pre>

### 取「某一頁」的文章

<pre><code>git clone </code></pre>

### 利用「關鍵字」取得文章

<pre><code>git clone </code></pre>


## 效能
比較條件1：取得「電影版」頁數「3001」~頁數「3030」的文章及回覆
<pre><code>$ python3 main.py -f 3001 -t 3030 -m 1 -r 1</code></pre>
 
| 情境 | 開始時間 | 結束時間 | 花費時間 | 
| ------ | ------ | ------ | ------ |
| single thread | 2019-02-01 14:50:55.000 | 2019-02-01 14:53:33.208 | 2分38秒 |
| multi-thread | 2019-02-01 15:03:11.671 | 2019-02-01 15:04:38.429 | 1分26秒 |


### 取得「台灣遊園地TaiwanPlaza」底下所有看板及網址
https://www.ptt.cc/cls/806
