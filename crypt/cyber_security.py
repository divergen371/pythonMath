# Standard Library
import os

# Third Party Library
import openai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_article_content(driver) -> str:
    """
    記事ページから本文を抽出する関数。

    Args:
        driver: Selenium WebDriver のインスタンス。

    Returns:
        str: 抽出された本文。
    """
    try:
        content_div = driver.find_element(By.CSS_SELECTOR, "div.post-body")
        # 記事のHTMLを取得
        content_html = content_div.get_attribute("innerHTML")

        # BeautifulSoup を使用してHTMLを解析
        # Third Party Library
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(content_html, "html.parser")
        paragraphs = []

        for element in soup.children:
            if element.name == "p":
                paragraphs.append(element.get_text(strip=True))
            elif element.name == "ul" or element.name == "ol":
                list_items = []
                for li in element.find_all("li"):
                    list_items.append(f"・ {li.get_text(strip=True)}")
                paragraphs.append("\n".join(list_items))
            elif element.name:
                # 他のタグも必要に応じて処理
                paragraphs.append(element.get_text(strip=True))

        content = "\n\n".join(paragraphs)
        return content

    except Exception as e:
        print("記事内容の抽出中にエラーが発生しました:", e)
        return ""


def summarize_text_using_chatgpt(text: str) -> str:
    """
    ChatGPT を使用してテキストを要約する関数。

    Args:
        text (str): 要約対象のテキスト

    Returns:
        str: 要約結果
    """
    system_prompt = (
        "取得した記事毎に日本語で要約してください。各記事の要約の長さは3000字でお願いします。\n"
        "3000字以内で要約しきれない場合に限り、重要項目が脱落しないように圧縮してください。\n"
        "また、出力する要約が途中で途切れることは許されません。\n"
        "必要に応じて項目化してください。\n\n"
    )
    user_prompt = text
    try:
        response = openai.ChatCompletion.create(
            model="chatgpt-4o-latest",  # もしくは利用可能な最新モデル
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=3500,  # 要約の長さを調整
            temperature=0.3,
            top_p=0.8
        )
        summary = response.choices[0].message["content"].strip()
        return summary
    except Exception as e:
        print("ChatGPTによる要約中にエラーが発生しました:", e)
        return "要約不可"


def scrape_popular_articles_selenium(url: str) -> list[dict]:
    """
    Selenium を使用して The Hacker News の人気記事の見出しとリンクを取得し、
    各記事の内容を抽出して要約します。

    Args:
        url (str): スクレイピング対象の URL。

    Returns:
        list[dict]: 各記事の見出し、リンク、要約を含むリスト。
    """
    print("Seleniumを使用してページにアクセスします。")

    # WebDriver Manager を使用して ChromeDriver を自動的に管理
    options = Options()
    options.add_argument(
        "--headless"
    )  # ヘッドレスモード（ブラウザを表示しない）
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/133.0.6943.126 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print("WebDriverの初期化中にエラーが発生しました:", e)
        return []

    try:
        driver.get(url)
        print(f"URLにアクセスしました: {url}")

        # ページが完全にロードされるまで待機（必要に応じて調整）
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//div[contains(@class, "cf") and contains(@class, "pop-article") and contains(@class, "clear") and not(ancestor::div[@id="sidebar-list"])]',
                    )
                )
            )
            print("人気記事の要素がロードされました。")
        except Exception as e:
            print(
                "人気記事の要素がロードされるまで待機中にエラーが発生しました:",
                e,
            )
            return []

        # 人気記事の要素を取得 (div.cf.pop-article.clear から div#sidebar-list 内を除外)
        articles = driver.find_elements(
            By.XPATH,
            '//div[contains(@class, "cf") and contains(@class, "pop-article") and contains(@class, "clear") and not(ancestor::div[@id="sidebar-list"])]',
        )
        print("取得した記事ブロックの件数:", len(articles))

        if not articles:
            print(
                "指定した記事ブロックが見つかりませんでした。HTML構造を確認してください。"
            )
            return []

        # （オプション）取得したHTMLの一部を表示
        page_source = driver.page_source
        print("ページのHTML内容（最初の1000文字）:")
        print(page_source[:1000])

        headlines_data = []
        for idx, article in enumerate(articles, start=1):
            try:
                # 見出しのテキストを取得
                headline_div = article.find_element(By.CLASS_NAME, "pop-title")
                headline = headline_div.text.strip()

                # 見出しのリンクを取得
                link_element = article.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")

                print(f"\n記事ブロック {idx}:")
                print(f"見出し取得成功: {headline}")
                print(f"リンク: {link}")

                # 記事ページにアクセスして内容を抽出
                driver.execute_script("window.open('');")  # 新しいタブを開く
                driver.switch_to.window(
                    driver.window_handles[1]
                )  # 新しいタブに切り替える
                driver.get(link)
                print(f"記事ページにアクセスしました: {link}")

                # ページが完全にロードされるまで待機
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div.post-body")
                        )
                    )
                    print("記事のメインコンテンツがロードされました。")
                except Exception as e:
                    print(
                        "記事のメインコンテンツがロードされるまで待機中にエラーが発生しました:",
                        e,
                    )
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    summary = "要約不可"
                    headlines_data.append(
                        {
                            "headline": headline,
                            "link": link,
                            "summary": summary,
                        }
                    )
                    continue

                # 記事内容の抽出
                content = extract_article_content(driver)
                if not content:
                    print("記事内容が抽出できませんでした。")
                    summary = "要約不可"
                else:
                    # ChatGPT を使用して記事内容を要約
                    summary = summarize_text_using_chatgpt(content)
                    print(f"要約: {summary}")

                headlines_data.append(
                    {"headline": headline, "link": link, "summary": summary}
                )

                driver.close()  # 現在のタブを閉じる
                driver.switch_to.window(
                    driver.window_handles[0]
                )  # 元のタブに戻る

            except Exception as e:
                print(f"記事ブロック {idx} の処理中にエラーが発生しました:", e)
                # 可能な限り処理を続行
                try:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                except Exception:
                    pass
                continue

        return headlines_data

    except Exception as e:
        print("Seleniumでの操作中にエラーが発生しました:", e)
        return []
    finally:
        driver.quit()
        print("WebDriverを終了しました。")


if __name__ == "__main__":
    print("Seleniumスクリプトの実行を開始します。")
    url = "https://thehackernews.com/"
    headlines = scrape_popular_articles_selenium(url)

    if headlines:
        print("\n人気記事の見出しと要約:")
        for article in headlines:
            print(f" - 見出し: {article['headline']}")
            print(f"   リンク: {article['link']}")
            print(f"   要約: {article['summary']}\n")
    else:
        print("見出しが取得できませんでした。")
    print("Seleniumスクリプトの実行が終了しました。")
