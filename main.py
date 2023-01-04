import os
import random
import requests
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("/help 를 입력하여 사용 방법을 확인하실 수 있습니다.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('/random: KOSPI, KOSDAQ, KONEX 상장기업 중 한 기업에 대한 정보를 랜덤으로 제공해드립니다.')
    await update.message.reply_text('기업명 입력\n· 빅텍, 써니전자, 경남스틸 등 검색하고 싶은 기업의 상장명을 정확하게 입력합니다.\n· "전자"와 같은 키워드를 입력하면 기업명에 "전자"가 포함된 기업을 알려드립니다.\n· "LG디스플레이"가 아닌 "엘지디스플레이"와 같이 틀린 이름을 입력하면 어떤 결과 값도 반환하지 않습니다.')
    
    
async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /random is issued."""
    rannum = random.randint(0, len(df))
    name = df.loc[rannum]['회사명']
    ticker = str(df.loc[rannum]['종목코드']).zfill(6)
    sector = df.loc[rannum]['업종']
    item = df.loc[rannum]['주요제품']
    ceo = df.loc[rannum]['대표자명']
    hp = str(df.loc[rannum]['홈페이지'])
    
    txt, link = scrape(name, ticker)
    await update.message.reply_text(text=f"[{link}]({hp})", parse_mode='Markdown', disable_web_page_preview=False)
    await update.message.reply_text(
        text=f"· 대표자명: {ceo}\n· 업종: {sector}\n· 주요제품: {item}"
    )
    await update.message.reply_text(txt)
    
    sector_list = list(f"· {s}" for s in random.sample(sector_dict[sector], min(len(sector_dict[sector]), 10)))
    if sector_list:
        t = f"유사 기업 추천 :: {sector}\n"
        t += "\n".join(sector_list)
        await update.message.reply_text(t)
    

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """reply summary of the company that user search."""
    ticker = update.message.text.upper()
    name, infos = search(ticker)    # infos=[홈페이지, 업종, 주요제품, 대표자명]
    if type(name) == str:
        txt, link = scrape(ticker, name)
        await update.message.reply_text(text=f"[{link}]({infos[0]})", parse_mode='Markdown', disable_web_page_preview=False)
        await update.message.reply_text(
            text=f"· 대표자명: {infos[3]}\n· 업종: {infos[1]}\n· 주요제품: {infos[2]}"
        )
        sector_list = list(f"· {s}" for s in random.sample(sector_dict[infos[1]], min(len(sector_dict[infos[1]]), 10)))
        
    else:
        if name:
            txt = "혹시 이 기업을 검색하셨나요?\n\n" + "\n".join(name)
        else:
            txt = "검색 결과가 없습니다. 키워드를 정확하게 입력해주세요."
    await update.message.reply_text(txt)
    
    try:
        if sector_list:
            t = f"유사 기업 :: {infos[1]}\n"
            t += "\n".join(sector_list)
            await update.message.reply_text(t)
    except:
        pass
    
    
def search(ticker):
    keys = list(df['회사명'])
    if ticker in keys:
        idx = keys.index(ticker)
        return str(list(df['종목코드'])[idx]).zfill(6), [str(list(df['홈페이지'])[idx]), str(list(df['업종'])[idx]), str(list(df['주요제품'])[idx]), str(list(df['대표자명'])[idx])]
    else:
        similar = []
        for key in keys:
            if ticker in key: similar.append(f"· {key}")
        return similar, None
    

def scrape(name, code):
    url = f'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}'
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    soup = BeautifulSoup(html, 'html.parser')
    summary = soup.select('#wrapper > div:nth-child(6) > div.cmp_comment > ul > li')
    link = f"{name}({code})"
    result = []
    for s in summary:
        result.append(f"· {s.text}")
    txt = "\n\n".join(result) if result else "기업 개요가 존재하지 않습니다."
    return txt, link


def main():
    TOKEN = os.environ.get('TELE_KEY')
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()


if __name__ == "__main__":
    df = pd.read_csv("./company.csv")
    sector_dict = defaultdict(list)
    for i in range(len(df)):
        sector_dict[df.loc[i, '업종']].append(df.loc[i, '회사명'])
    main()