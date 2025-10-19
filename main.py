import discord
from discord.ext import commands
from discord import app_commands, ui 
import random 
import asyncio 
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user.name}이(가) 성공적으로 로그인했습니다!')
    print(f'봇 ID: {bot.user.id}')
    print('------')
    # 봇의 상태 메시지를 설정합니다.
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help 명령어 입력"))

# 초기 Cog 로드 함수
async def load_extensions():
    # 'cogs' 폴더 안의 모든 .py 파일을 찾아 Cog로 로드합니다.
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            # 파일명에서 .py 확장자를 제거하여 모듈 이름으로 사용합니다. (예: cogs.greetings)
            extension_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(extension_name)
                print(f'{extension_name} 로드 완료.')
            except Exception as e:
                print(f'{extension_name} 로드 실패: {e}')

# 비동기 메인 함수 정의 (봇 실행 및 Cog 로드를 위해)
async def main():
    BOT_TOKEN = input("토큰을 입력하세요: ")

    async with bot: # bot 객체를 컨텍스트 매니저로 사용하여 안전하게 시작 및 종료
        await load_extensions() # Cog 로드
        await bot.start(BOT_TOKEN) # 봇 시작

# 메인 함수 실행
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("봇 종료 중...")
    except discord.LoginFailure:
        print("잘못된 토큰입니다. Discord Developer Portal에서 토큰을 확인하세요.")
    except Exception as e:
        print(f"봇 실행 중 오류 발생: {e}")






