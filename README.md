# ptt-crawler

本專案利用[requests](https://github.com/requests/requests)取得ptt文章

## 安裝方法
<pre><code>$ git clone https://github.com/cutejaneii/ptt-crawler.git</code></pre>
## 專案說明
1. 有鑑於PTT版出口成「髒」，新增[remove_words.txt](https://github.com/cutejaneii/ptt-crawler/blob/master/ptt-crawler/remove_words.txt)過濾「標題」及「回文」（文章內容不過濾），
   偶有錯殺之文章，還請見諒，或可自行修改remove_words.txt

## 使用方法

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

<pre><code>git clone </code></pre>

### 取「某一頁」的文章

<pre><code>git clone </code></pre>

### 利用「關鍵字」取得文章

<pre><code>git clone </code></pre>

### 取得「台灣遊園地TaiwanPlaza」底下所有看板及網址
https://www.ptt.cc/cls/806
