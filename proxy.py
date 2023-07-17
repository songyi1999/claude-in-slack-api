# *_* encoding-utf-8 *_*

# 给claude 使用的代理模式 
# 用于将claude的请求通过本地获取后返回给claude 作为它能用的结构数据
"""
 promt : 
 我和你约定一个代理访问的方法，当你对我说proxy 搜索关键词时 。由你来分析这个网站的源代码获取答案，
请求的结构为:proxy 关键词
        例如:需要获取现在时间可以这么来.
        proxy  现在时间
"""
import requests
import asyncio
from pyppeteer import launch
async def get_proxy(commandstring):
    """
        claude 请求的结构为:proxy 关键词
        

        Args:
            args: proxy 关键词

        Returns: 
            获取到的网址源代码或者claude的返回值
    """
   
    #判断是否以proxy开头
    if commandstring.startswith("proxy"):
        #获取关键词
        keyword = commandstring.split("proxy")[1].strip()
        #判断关键词是否为空
        if keyword:
            #获取网页源代码
            html = await get_proxy_pyppeteer(keyword)
            #返回网页源代码
            return html
        else:
            #返回claude的返回值
            return "你没有输入关键词"
    else:
        #返回claude的返回值
        return commandstring
    

# 使用pyppeteer 获取网页源代码
async def get_proxy_pyppeteer(keyword):
    browser = await launch(args=['--no-sandbox'],headless=True) 

    # 新建一个页面
    page = await browser.newPage() 

    # 访问谷歌搜索页面
    await page.goto('https://www.google.com/')
    await page.screenshot({'path': 'example.png'})
    # 在搜索框中输入查询词 "现在时间"
    await page.type('.gLFyf', keyword) 

    # 点击搜索按钮进行搜索
    await page.click('.Aa')

    #等待结果加载完毕
    await page.waitForSelector('.hY7IBd')

    # 获取结果页面的HTML代码
    html = await page.content()
    
    

    # 关闭浏览器
    await browser.close()
    return html


async  def foo():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.google.com/')
    await page.screenshot({'path': 'example.png'})
    await browser.close()
    
if __name__ == '__main__':
    # commandstring="proxy 现在时间"
    # result = asyncio.run(get_proxy(commandstring))
    # print(result)
    asyncio.run(foo())
