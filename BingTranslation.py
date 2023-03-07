import urllib.request as url_req
import requests
from bs4 import BeautifulSoup

# 串接 微軟 bing 翻譯器
# 從網頁解析所需參數後 將資料傳到微軟API 得到翻譯好字串

def get_trans_from_bing(content : str,from_lang : str,to_lang : str):
    """
    content : 要翻譯的字串
    from_lang : 輸入字串的語言
    to_lang : 希望翻譯的語言
    en 英文 zh-Hant 繁體中文 ja 日文 zh-Hans 簡體中文
    ----------
    返回 翻譯好的字串
    
    """
    userAgent = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',  
                    }

    search_url = 'https://www.bing.com/translator/?FORM=&mkt=zh-TW'

    request = url_req.Request(search_url,headers=userAgent)
    with url_req.urlopen(request,timeout=10) as resopnse:
        data = resopnse.read().decode("utf-8")
        resopnse.close()
    root = BeautifulSoup(data,"html.parser")
    scripts = root.findAll('script')
    for script in scripts:
        if "params_AbusePreventionHelper" in script.text:
            target = script.text
            target = target.split("params_AbusePreventionHelper = [")[1].split("];")[0]
        if "IG:\"" in script.text:
            target2 = script.text
            ig = target2.split("IG:\"")[1].split("\"")[0]
    key = target.split(",")[0]
    token = target.split("\"")[1]
    data = '&fromLang='+from_lang+'&text='+content+'&to='+to_lang+'&token='+token+'&key='+str(key)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',
    'authority':'www.bing.com',
    'accept-encoding':'gzip, deflate, br',
    'content-type':'application/x-www-form-urlencoded'
    }
    r = requests.post('https://www.bing.com/ttranslatev3?isVertical=1&&IG='+ig+'&IID=translator.5023.1',headers=headers,data=data.encode())
    return r.json()[0]["translations"][0]["text"]

if __name__ == '__main__':
    print(get_trans_from_bing("poly","en","zh-Hant"))
