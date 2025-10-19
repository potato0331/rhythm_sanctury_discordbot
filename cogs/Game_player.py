import discord
from discord.ext import commands
from models import Player
from discord import app_commands # 슬래시 명령어를 위해 import
import random 

class GamePlayer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="상태확인", description="지금 내 점수와 코인 보유량을 조회합니다.")
    async def _check_status(self, interaction: discord.Interaction):
        my_status = 0

        for status in self.bot.player_status:
            if status.name == interaction.user.global_name:
                my_status = status
                break

        if my_status == 0:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
        else:
            await interaction.response.send_message(f"{interaction.user.global_name}님의 코인 보유량: {my_status.coin}, 현재 점수: {my_status.score}",ephemeral = True)

    @app_commands.command(name="점수입력", description="지금 내 점수와 코인 보유량을 조회합니다.")
    @app_commands.describe(점수="이번 라운드 최종 점수")
    async def _input_score(self, interaction: discord.Interaction, 점수: int=-1):
        my_status = 0

        for status in self.bot.player_status:
            if status.name == interaction.user.global_name:
                my_status = status
                break

        if my_status == 0:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
        else:
            my_status.round_score = 점수
            await interaction.response.send_message(f"{interaction.user.global_name}님이 점수 입력을 완료했습니다.")
       



#여기서부터 건들지 말 것
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"{len(synced)}개의 슬래시 명령어를 동기화했습니다.")
        except Exception as e:
            print(f"명령어 트리 동기화 실패: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(GamePlayer(bot))
