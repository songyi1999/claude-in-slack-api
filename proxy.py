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

import asyncio
from playwright.async_api import async_playwright
async def get_proxy(commandstring):
    """
        claude 请求的结构为:proxy 关键词
        

        Args:
            args: proxy 关键词

        Returns: 
            获取到的网址源代码或者claude的返回值
    """
   
    #判断是否以proxy开头
    commandstring=commandstring.strip()
    if commandstring.startswith("proxy"):
        #获取关键词
        keyword = commandstring.split("proxy")[1].strip()
        #判断关键词是否为空
        if keyword:
            #获取网页源代码
            html = await get_proxy_playwright(keyword)
            #返回网页源代码
            return html
        else:
            #返回claude的返回值
            return "你没有输入关键词"
    else:
        #返回claude的返回值
        return commandstring
    

# 使用pyppeteer 获取网页源代码
async def get_proxy_playwright(keyword):
    # 启动浏览器
    
    async with async_playwright() as p:
        for browser_type in [p.chromium]:
            browser = await browser_type.launch(args=['--lang=zh-CN'])
            page = await browser.new_page()
            await page.goto(f"http://www.google.com/search?q={keyword}")
            await page.screenshot(path=f'example-{browser_type.name}.png')
            # 等待页面加载完成
            await page.wait_for_load_state()
            
            # 获取渲染后的网页源代码
            bodytext =await  page.locator("body").inner_text()
            await page.screenshot(path=f'example-{browser_type.name}.png')
            await browser.close()
            return "请根据以下获取到的网页内容回答问题'"+keyword+"'\n"+bodytext


   



    
if __name__ == '__main__':
    commandstring="proxy 现在时间"
    result = asyncio.run(get_proxy(commandstring))
    print(result)
    # asyncio.run(get_proxy_playwright('现在时间'))
