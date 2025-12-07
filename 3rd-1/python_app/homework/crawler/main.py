import requests
from bs4 import BeautifulSoup
import json

def fetch_gossiping_data():
    target_url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    
    # 設定 Headers (模擬瀏覽器)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 設定 Cookie (通過滿18歲驗證)
    cookies = {
        "over18": "1"
    }

    try:
        # 發送 GET 請求
        response = requests.get(target_url, headers=headers, cookies=cookies)
        response.raise_for_status() # 檢查請求是否成功

        # 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        articles_data = []

        # PTT 的文章列表在 div.r-ent 區塊中
        rents = soup.find_all("div", class_="r-ent")

        for rent in rents:
            # 1. 抓取標題與連結
            title_div = rent.find("div", class_="title")
            
            # 如果文章已被刪除，title_div 內通常沒有 a tag，或是 title_div 本身結構不同
            if not title_div:
                continue
                
            a_tag = title_div.find("a")
            
            # 處理已刪除的文章 (有 title div 但無連結)
            if not a_tag:
                continue

            title = a_tag.text.strip()
            link = "https://www.ptt.cc" + a_tag["href"]

            # 2. 抓取推文數 (up)
            nrec_div = rent.find("div", class_="nrec")
            up_count = "0" # 預設為 0
            
            if nrec_div:
                span = nrec_div.find("span")
                if span:
                    up_count = span.text.strip()
                # 如果沒有 span，表示推文數為 0，維持預設值

            # 3. 整理資料
            article_info = {
                "title": title,
                "up": up_count,
                "link": link
            }
            articles_data.append(article_info)

        return articles_data

    except Exception as e:
        print(f"發生錯誤: {e}")
        return []

if __name__ == "__main__":
    result = fetch_gossiping_data()
    
    # 輸出 JSON (ensure_ascii=False 讓中文正常顯示)
    json_output = json.dumps(result, indent=4, ensure_ascii=False)
    
    # 印出結果
    print(json_output)
    
    # 也可以選擇寫入檔案
    with open("gossiping_result.json", "w", encoding="utf-8") as f:
        f.write(json_output)

