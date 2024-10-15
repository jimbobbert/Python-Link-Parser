import time
import discord
import re
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True, pass_context=True)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command(pass_context=True)
async def paste(ctx):
    with open("input.txt", "r", encoding='utf-8') as f, \
            open("output.txt", "w", encoding='utf-8') as z:

        download_name_pattern = r'href="([^"]+)".*<em><strong>Download (?:for )?(.+?)</strong></em>'
        pattern = r"<strong>-(.+?)-</strong>"

        # Process each line in the input file
        for line in f:

            download_match = re.search(download_name_pattern, line)
            if download_match:
                # Extract the download link and name
                download_link = download_match.group(1)
                name = download_match.group(2)

                # Print the result
                print(name)
                await ctx.send(name)
                print(download_link)
                await ctx.send(download_link)

            # base names

            if re.match(r'^<a href="https://discord\.com/channels/\d+/\d+', line):
                continue

            matches = re.findall(pattern, line)
            for match in matches:
                z.write(match + "\n")
                print(match)
                await ctx.send(match)

            # source links

            if "<strong>Source</strong>" in line or "<strong>&gt;Source&lt;</strong>" in line:
                if "discord.com" not in line:
                    link = line.split('href="')[1].split('">')[0]
                    z.write(link + "\n")
                    print(link)
                    await ctx.send(link)

            # download links

            if "<strong>Download</strong>" in line or "<strong>&gt;Download&lt;</strong>" in line:
                link2 = line.split('href="')[1].split('">')[0]
                z.write(link2 + "\n \n")
                print(link2)
                await ctx.send(link2)
            time.sleep(.75)
        return
    return

bot.run("")
