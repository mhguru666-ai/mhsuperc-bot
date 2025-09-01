import asyncio
from playwright.async_api import async_playwright
import telegram

# 🔑 Bot details
TOKEN = "8462393701:AAEPP4EY-v5MSH5taIPQ_WMHQ22TEgfepDU"
CHAT_ID = "716793322"

# Booking page
URL = "https://termine.staedteregion-aachen.de/auslaenderamt/"

bot = telegram.Bot(token=TOKEN)

async def check_slots():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Step 1: Open start page
        await page.goto(URL)

        # Step 2: Click "Termin buchen"
        await page.click("text=Termin buchen")

        # Step 3: Choose service "Aufenthaltstitel verlängern"
        await page.click("text=Aufenthaltstitel verlängern")

        # Step 4: Wait for calendar load
        await page.wait_for_timeout(5000)

        content = await page.content()

        if "Keine Termine" not in content:
            await bot.send_message(chat_id=CHAT_ID, text="⚡ Appointment available! Book now: " + URL)

        await browser.close()

async def main():
    while True:
        await check_slots()
        await asyncio.sleep(60)  # check every 60 sec

asyncio.run(main())
