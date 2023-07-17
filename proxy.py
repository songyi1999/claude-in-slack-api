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
        您好,我是新盘门智能科技的客服猫局。要查询苏州明天的天气,我需要使用搜索引擎。所以我的回答是:

        proxy 苏州明天天气

        非常抱歉,由于网络限制,我无法直接访问搜索引擎来获取苏州明天的天气信息。希望这个代理关键词可以让我使用搜索引擎来查询您需要的信息。如果无法获取结果,请您见谅,还请您直接提供需要的天气信息,我会在获得信息后尽快回复您。谢谢您的理解!

        Args:
            args: proxy 关键词

        Returns: 
            获取到的网址源代码或者claude的返回值
    """
   
    #判断是否包含proxy 关键词 这样一行并解析出关键词
    lines = commandstring.split("\n")
    if "proxy" in commandstring:
        #获取关键词
        keyword = ""
        for line in lines:
            if "proxy" in line:
                keyword = line.replace("proxy","").strip()
                break        

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
            await page.goto(f"https://www.google.com/search?q={keyword}",timeout=600000)
            # await page.screenshot(path=f'example-{browser_type.name}.png')
            # 等待页面加载完成
            await page.wait_for_load_state(timeout=600000)
            
            # 获取渲染后的网页源代码
            bodytext =await  page.locator("body").inner_text()
            # await page.screenshot(path=f'example-{browser_type.name}.png')
            await browser.close()
            return "请根据以下获取到的网页内容回答问题'"+keyword+"'\n"+bodytext


   



    
if __name__ == '__main__':
    commandstring="proxy 现在时间"
    result = asyncio.run(get_proxy(commandstring))
    print(result)
    # asyncio.run(get_proxy_playwright('现在时间'))
