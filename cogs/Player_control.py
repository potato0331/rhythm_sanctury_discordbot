import discord
from discord.ext import commands
from models import Player
from discord import app_commands # 슬래시 명령어를 위해 import
import datetime

class PlayerControl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="진행자점수수정", description="(진행자용 기능)원하는 플레이어의 점수를 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 점수="수정할 점수(변화량)")
    async def _master_score_manage(self, interaction: discord.Interaction, 이름: str="이름", 점수: int = 0):
        target_status = 0
        for status in self.bot.player_status:
            if status.name == 이름:
                target_status = status
                break
        if target_status == 0:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다",ephemeral = True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 점수를 {target_status.score}에서 {target_status.score + 점수}로 수정했습니다.",ephemeral = True)
            target_status.score += 점수

    @app_commands.command(name="진행자코인수정", description="(진행자용 기능)원하는 플레이어의 코인의 수를 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 코인="수정할 코인(변화량)")
    async def _master_coin_manage(self, interaction: discord.Interaction, 이름: str="이름", 코인: int=0):
        target_status = 0
        for status in self.bot.player_status:
            if status.name == 이름:
                target_status = status
                break
        if target_status == 0:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다",ephemeral = True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 코인을 {target_status.coin}에서 {target_status.coin + 코인}로 수정했습니다.",ephemeral = True)
            target_status.coin += 코인

    @app_commands.command(name="진행자현재점수수정", description="(진행자용 기능)원하는 플레이어의 이번 라운드 점수를 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 점수="수정할 점수(변화량)")
    async def _master_round_score_manage(self, interaction: discord.Interaction, 이름: str="이름", 점수: int=-1):
        target_status = 0
        for status in self.bot.player_status:
            if status.name == 이름:
                target_status = status
                break
        if target_status == 0:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다",ephemeral = True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 점수를 {target_status.round_score}에서 {target_status.round_score + 점수}로 수정했습니다.",ephemeral = True)
            target_status.round_score += 점수
            
    @app_commands.command(name="진행자배수수정", description="(진행자용 기능)원하는 플레이어의 이번 라운드의 배팅 가산값을 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 배수="수정할 배수(변화량)")
    async def _master_round_multiplier_manage(self, interaction: discord.Interaction, 이름: str="이름", 배수: int=0):
        target_status = 0
        for status in self.bot.player_status:
            if status.name == 이름:
                target_status = status
                break
        if target_status == 0:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다",ephemeral = True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 배팅 가산값을 {target_status.round_multiplier}에서 {target_status.round_multiplier + 배수}로 수정했습니다.",ephemeral = True)
            target_status.round_multiplier += 배수


    @app_commands.command(name="진행자효과수정", description="(진행자용 기능)원하는 플레이어의 이번 라운드의 적용된 효과를 추가합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 추가제거 = "[추가]또는 [제거]입력", 효과="추가하거나 제거할 효과를 정확히")
    async def _master_effect_manage(self, interaction: discord.Interaction, 이름: str="이름", 추가제거: str="추가", 효과: str="효과"):
        target_status = 0
        for status in self.bot.player_status:
            if status.name == 이름:
                target_status = status
                break
        if target_status == 0:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다",ephemeral = True)
        else:
            if 추가제거 == "제거":
                target_status.effect_list.remove(효과)
                await interaction.response.send_message(f"{target_status.name}님에게 {효과}를 제거했습니다.",ephemeral = True)
            else: 
                target_status.effect_list.append(효과)
                await interaction.response.send_message(f"{target_status.name}님에게 {효과}를 추가했습니다.",ephemeral = True)

    @app_commands.command(name='효과보기', description="현재 플레이어들에게 적용된 효과를 확인합니다.")
    async def _show_effects(self, interaction: discord.Interaction): # 'cinteraction' -> 'interaction' 오타 수정
        # 게임이 시작되지 않았거나 플레이어 정보가 없을 경우를 대비한 예외 처리
        if not hasattr(self.bot, 'player_status') or not self.bot.game_started:
            await interaction.response.send_message("아직 게임이 시작되지 않았거나, 플레이어 정보가 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(
            title="현재 적용 중인 효과 목록",
            description="모든 플레이어의 효과 정보입니다.",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)

        if not self.bot.player_status:
            embed.description = "현재 게임에 참여 중인 플레이어가 없습니다."
        else:
            for status in self.bot.player_status:
                # effect_list (리스트)를 줄바꿈(\n)으로 연결된 하나의 문자열로 변환합니다.
                # 리스트가 비어있을 경우 "효과 없음"을 표시합니다.
                effects_str = "\n".join(status.effect_list) if status.effect_list else "적용된 효과 없음"
                
                # 각 플레이어의 정보를 필드로 추가합니다.
                embed.add_field(name=f"👤 {status.name}", value=effects_str, inline=True) 

        await interaction.response.send_message(embed=embed)

#여기서부터 건들지 말 것-슬래시커맨드용
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"{len(synced)}개의 슬래시 명령어를 동기화했습니다.")
        except Exception as e:
            print(f"명령어 트리 동기화 실패: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerControl(bot)) #여기를 객체명으로 수정
