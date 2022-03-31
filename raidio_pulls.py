import asyncio
from pyppeteer import launch
import time
import csv
import re

URL = 'https://raider.io/sepulcher-of-the-first-ones/rankings/world/mythic'
async def main():
    browser = await launch(
        headless=False,
        dumpio=True,
        autoClose=True,
        ignoreHTTPSErrors=True,
        userDataDir="D:\\tmp",
        args=['--window-size=1024,768',]) 
    page = await browser.newPage()
    await page.setViewport({'width': 1024, 'height': 768})
    await page.evaluateOnNewDocument(
        '() =>{ Object.defineProperties(navigator,'
        '{ webdriver:{ get: () => false } }) }')
    await page.goto(url=URL,options={'waitUntil':'domcontentloaded','timeout':50 * 1000})
    await asyncio.sleep(2)
    for i in range(1,10):
        xp = await page.querySelector('#content > div > div:nth-child(1) > div > div.fresnel-container.fresnel-greaterThan-sm > table > tbody > tr:nth-child(%s) > td.slds-cell-wrap > div > div > h3 > a'%i)
        await xp.click()
        page.waitForNavigation({'waitUntil':'domcontentloaded'})
        await asyncio.sleep(2)
        await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        guild = re.search(r'(?<=\‹).*(?=\›)',await page.title()).group()
        await asyncio.sleep(2)

        html = await page.Jx('//*[@id="content"]/div/div[1]/div/div/section[2]/div[2]/table/tbody[1]/tr')
        data = []
        for i in html:
            guildinfo=[]
            guildinfo.append(guild)
            name = await i.Jx('./td[1]/span[2]')
            if len(name) == 0:
                continue
            else:
                boss = await (await name[0].getProperty("innerText")).jsonValue()
            guildinfo.append(boss)

            guild_pro = await i.Jx('./td[2]/div/div[1]/span')
            if len(guild_pro) == 0:
                continue
            else:
                pro = await (await guild_pro[0].getProperty("innerText")).jsonValue()
                killtime = re.search(r'(?<=First Killed).*(?=\()',pro)
                if killtime == None:
                    killtime = 'Not Killed'
                guildinfo.append(killtime[0])
                killweek = re.search(r'(?<=\().*(?=\))',pro)
                if killweek == None:
                    killweek = 'Not Killed'
                guildinfo.append(killweek[0])
                pulls = re.search(r'(?<=\))\d+',pro)
                if pulls == None:
                    pulls = re.search(r'(?<=ed)\d+',pro)
                guildinfo.append(pulls[0])
                data.append(guildinfo)
            await page.goBack()
            await asyncio.sleep(2)
            
        with open('D:\\wx\\pulls.csv','w+',encoding='utf-8',newline='') as f:
        w = csv.writer(f)
        w.writerow(['GUILD','BOSS','KillTime','Kill_Week','Pulls'])
        w.writerows(data)

    await browser.close()
        
        
        
    asyncio.get_event_loop().run_until_complete(main())
