import aiohttp
import asyncio
import queue



referer = ''
url = 'https://item.jd.com/31218608033.html'
url_queue = queue.Queue()
url_queue.put(url)
import time

headers = {
    "User_Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
    "Referer": referer
}

MAX_TIMES = 5

async def async_crawl(coro_id):
    empty_flag = False
    while True:
        try:
            print("Enter:", coro_id)
            url = url_queue.get(block=False)
            empty_flag = False
            print(coro_id, url)
        except queue.Empty:
            if empty_flag:
                break
            else:
                empty_flag = True
                await asyncio.sleep(60)
                continue
        else:
            pass

        if not url:
            continue

        try_times = 0
        while try_times < MAX_TIMES:
            try:
                async with aiohttp.ClientSession() as session:
                    # 老版本aiohttp没有verify参数，如果报错卸载重装最新版本
                    print(time.time())
                    async with session.get(url, headers=headers, timeout=30, verify_ssl=False) as r:
                        # text()函数相当于requests中的r.text，r.read()相当于requests中的r.content
                        print(time.time())
                        html = await r.text()
                        print(str(coro_id) + "完成" + url)
            except Exception as e:
                print(str(e))
                try_times = try_times + 1
            else:
                break



loop = asyncio.get_event_loop()
to_do = [async_crawl(coro_id) for coro_id in range(0, 10)]
wait_coro = asyncio.wait(to_do)
# 对需要ssl验证的网页，需要250ms左右等待底层连接关闭
loop.run_until_complete(wait_coro)
loop.run_until_complete(asyncio.sleep(0.25))
loop.close()



