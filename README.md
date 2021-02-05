讓自己的記憶加深
===============

```
Git1.7.0以後加入了Sparse Checkout模式，該模式可以實現Check Out指定檔或者資料夾
舉個例子：
現在有一個 Memo 倉庫 https://github.com/oscarobwu/Memo.git
你要git clone裡面的 Python 子目錄：


git init Python && cd Python     // 新建倉庫並進入資料夾
git config core.sparsecheckout true // 設置允許克隆子目錄
echo 'Python' >> .git/info/sparse-checkout // 設置要克隆的倉庫的子目錄路徑   //空格別漏 將要下載目錄填入
git remote add origin https://github.com/oscarobwu/Memo.git // 這裡換成你要克隆的項目和庫
git pull origin master    // 下載代碼
```

```
開始使用 F5 BIGREST API 重寫開關機
```
