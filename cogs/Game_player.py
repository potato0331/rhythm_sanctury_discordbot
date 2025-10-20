import discord
from discord.ext import commands
from models import Player, RoundSong
from discord import app_commands
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

    @app_commands.command(name="점수입력", description="이번 라운드의 게임 플레이 결과를 입력합니다.")
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

    @app_commands.command(name="선곡등록", description="게임에 등장시킬 선곡과 라운드 패널티를 지정합니다.")
    @app_commands.describe(전반후반="전반/후반", 곡명="곡의 제목", 곡레벨="선곡한 곡의 레벨(전반: MX8~15+SC1~11, 후반: SC8~15)", 패널티="그 라운드의 패널티")
    @app_commands.choices(전반후반=[
        app_commands.Choice(name="전반", value="전반"),
        app_commands.Choice(name="후반", value="후반"),
    ])
    async def _register_song(self, interaction: discord.Interaction, 전반후반: str="전반", 곡명: str="A", 곡레벨: str="SC1", 패널티: str="없음"):
        my_status = 0

        for status in self.bot.player_status:
            if status.name == interaction.user.global_name:
                my_status = status
                break

        if my_status == 0:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
            return
        
        if 전반후반 == "전반":
            my_status.first_half = RoundSong(song_name = 곡명, song_level = 곡레벨, round_penalty = 패널티)
        else:
            my_status.second_half = RoundSong(song_name = 곡명, song_level = 곡레벨, round_penalty = 패널티)

        await interaction.response.send_message(f"{my_status.name}님의 {전반후반}전 곡을 {곡명}/{곡레벨}/{패널티}로 설정했습니다.", ephemeral=True)
       
    @app_commands.command(name='효과보기', description="현재 플레이어들에게 적용된 효과를 확인합니다.")
    async def _show_effects(self, interaction: discord.Interaction): 
        # 게임이 시작되지 않았거나 플레이어 정보가 없을 경우를 대비한 예외 처리
        if not hasattr(self.bot, 'player_status') or not self.bot.game_started:
            await interaction.response.send_message("아직 게임이 시작되지 않았거나, 플레이어 정보가 없습니다.", ephemeral=True)
            return

        embed = discord.Embed(
            title="현재 적용 중인 효과 목록",
            description="모든 플레이어의 효과 정보입니다.",
            color=discord.Color.blue(),
        )

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
