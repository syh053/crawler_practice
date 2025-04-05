# Python 爬蟲程式與資料視覺化開發

  此專案為網頁爬蟲和 [Flask](https://github.com/hsuanchi/flask-template) 網站開發練習 

  - 利用 Blueprint  將原本的 main.py 拆分成多個獨立模塊
  
  - 利用 jinja2 繼承樣板功能，將重複使用到的 html 元素分離

  - PTT 新聞資料使用 aiohttp 及 asyncio 套件實作 "非同步" 爬蟲 ( 節省時間約 80% )

  相關連結

  - [非同步](https://dashcamp057.medium.com/%E7%88%AC%E8%9F%B2%E7%B3%BB%E5%88%97-python%E7%88%AC%E8%9F%B2%E5%85%A5%E9%96%80%E5%AF%A6%E4%BD%9C-%E4%B8%89-%E9%9D%9E%E5%90%8C%E6%AD%A5%E7%88%AC%E8%9F%B2-aka%E7%95%B0%E6%AD%A5%E7%88%AC%E8%9F%B2-1-66e892de05fd) - 非同步介紹

<br>

# Python 及套件版本

### Python 版本

- Python==3.8.5

### 套件版本

- Flask==3.0.3

- bs4==0.0.2

- flask-paginate==2024.4.12

- mysql-connector-python==9.0.0

- requests==2.32.3

- selenium==4.27.1

<br>

# 專案簡介

  ### 目前開發的路由為

  - 大盤指數

  - 股市新聞
  
  ### 開發中路由

  - 個股指標

<br>

大盤指數 : <br>

  - 顯示台股大盤指數，開盤、最高、最低、收盤及成交量(億)

股市新聞 : <br>

  - 顯示 PTT 及 聯合新聞網資訊

  - 可以使用搜尋欄分別查詢平台、作者、推文數

個股指標 : <br>

  - 因尚未開發完成，若使用者點選該路由，會顯示 "尚未開放~~"

<br>

# 預覽

### 大盤指數

![大盤指數-圖片](https://imgur.com/SVO7fsa.png)

### 股市新聞

![股市新聞-圖片](https://imgur.com/fiwFRbk.png)

### 個股指標

![個股指標-圖片](https://imgur.com/mHp41Oq.png)
