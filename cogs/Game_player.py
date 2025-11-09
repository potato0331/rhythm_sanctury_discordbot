import discord
from discord.ext import commands
import config
from models import RoundSong, User
from discord import app_commands


class GamePlayer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="선곡등록", description="게임에 등장시킬 선곡과 라운드 패널티를 지정합니다.")
    @app_commands.describe(전반후반="전반/후반", 곡명="곡의 제목", 곡레벨="선곡한 곡의 레벨(전반: MX8~15+SC1~11, 후반: SC8~15)", 패널티="그 라운드의 패널티")
    @app_commands.choices(전반후반=[
        app_commands.Choice(name="전반", value=0),
        app_commands.Choice(name="후반", value=1),
    ])
    async def _register_song(self, interaction: discord.Interaction, 전반후반: int, 곡명: str, 곡레벨: str, 패널티: str):
        if self.bot.current_phase != config.Phase.PREPARE:
            await interaction.response.send_message(f"아직 게임이 시작하지 않았거나, 이미 시작했습니다.")
            return

        player = self.__find_Player(interaction.user.global_name)

        if player == None:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
            return
                
        view = SongRegisterView()
        view.add_item(SongRegisterButton(style=discord.ButtonStyle.danger, label="거절"))
        view.add_item(SongRegisterButton(style=discord.ButtonStyle.success, label="수락"))
                
        embed = discord.Embed(
            title=f"{interaction.user.global_name}님의 {'후반' if 전반후반 else '전반'}곡 신청",
            color=discord.Color.blue()
        )
        embed.add_field(name="곡 정보", value=f"{곡명} / {곡레벨}", inline=True)
        embed.add_field(name="패널티", value=f"{패널티}", inline=True)
        
        master = await self.bot.fetch_user(master.id)
        await master.send(embed=embed, view=view)
        await interaction.response.send_message(f"{player.name}님의 {'후반' if 전반후반 else '전반'}전 곡을 {곡명}/{곡레벨}/{패널티}로 신청했습니다.", ephemeral=True)

        await view.wait()

        if view.selected_label == "수락":
            player.songs[전반후반] = RoundSong(곡명, 곡레벨, 패널티)
            await interaction.channel.send(f"{player.name}님의 {'후반' if 전반후반 else '전반'}전 곡이 승인됐습니다.")
        else:
            await interaction.channel.send(f"{player.name}님의 {'후반' if 전반후반 else '전반'}전 곡이 거절됐습니다.")

    @app_commands.command(name="상태확인", description="지금 내 상태를 조회합니다.")
    async def _check_status(self, interaction: discord.Interaction):
        player = 0

        for status in self.bot.player_status:
            if status.name == interaction.user.global_name:
                player = status
                break

        if player == 0:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
        else:
            await interaction.response.send_message("------------------------------\n"
                                                    f"{interaction.user.global_name}님\n"
                                                    f"코인 보유량: {player.coin}\n"
                                                    f"현재 배율: {player.round_multiplier}\n"
                                                    f"현재 점수: {player.score}\n"
                                                    f"이번 라운드 효과: {player.effect_list}\n"
                                                    "------------------------------\n",ephemeral = True)


    @app_commands.command(name="점수입력", description="이번 라운드의 게임 플레이 결과를 입력합니다.")
    @app_commands.describe(점수="이번 라운드 최종 점수")
    async def _input_score(self, interaction: discord.Interaction, 점수: int=-1):
        if self.bot.current_round == 0:
            await interaction.response.send_message("아직 라운드가 시작하지 않았습니다.")
            return
        if not self.bot.current_phase == config.Phase.CARD:
            await interaction.response.send_message("지금은 점수를 등록할 수 없습니다.")
            return

        player = self.__find_Player(interaction.user.global_name)

        if player == None:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
        else:
            player.round_score = 점수
            await interaction.response.send_message(f"{interaction.user.global_name}님이 {점수}점을 등록했습니다.")


    @app_commands.command(name="배팅", description="이번 라운드의 배팅액을 입력합니다.")
    @app_commands.describe(배팅액="이번 라운드의 배팅액")
    async def _input_betting(self, interaction: discord.Interaction, 배팅액: int = 0):
        if self.bot.current_round == 0:
            await interaction.response.send_message("아직 라운드가 시작하지 않았습니다.")
            return
        if not self.bot.current_phase == config.Phase.BETTING:
            await interaction.response.send_message("지금은 베팅할 수 없습니다.")
            return

        player = self.__find_Player(interaction.user.global_name)

        if player == None:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
            return
        
        if 배팅액 < 1 or 배팅액 > 15:
            await interaction.response.send_message(f"잘못된 배팅입니다. 배팅은 1코인부터 15코인까지 가능합니다",ephemeral = True)
            return
        
        if 배팅액 > 5 and self.bot.roundplayer.name == player.name:
            await interaction.response.send_message(f"잘못된 배팅입니다. 라운드플레이어는 5코인까지만 베팅할 수 있습니다.",ephemeral = True)
            return
        
        if 배팅액 - player.betting > player.coin:
            await interaction.response.send_message(f"코인이 부족합니다.",ephemeral = True)
            return
        
        player.coin -= 배팅액 - player.betting
        player.betting = 배팅액

        await interaction.response.send_message(f"{player.name}님이 배팅을 완료했습니다.")
        

       
    @app_commands.command(name='효과보기', description="현재 플레이어들에게 적용된 효과를 확인합니다.")
    async def _show_effects(self, interaction: discord.Interaction): 
        # 게임이 시작되지 않았거나 플레이어 정보가 없을 경우를 대비한 예외 처리
        if not hasattr(self.bot, 'player_status'):
            await interaction.response.send_message("플레이어 정보가 없습니다.", ephemeral=True)
            return
        if self.bot.current_round == 0:
            await interaction.response.send_message("아직 라운드가 시작하지 않았습니다.")
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

        effects_str = "\n".join(self.bot.master_player.effect_list) if self.bot.master_player.effect_list else "적용된 효과 없음"
        embed.add_field(name=f"⭐공통효과", value=effects_str, inline=True) 

        await interaction.response.send_message(embed=embed)
    
    def __find_Player(self, name):
        result = None
        for status in self.bot.player_status:
            if status.name == name:
                result = status
                break
        return result
    
class SongRegisterButton(discord.ui.Button):
    """자신의 상위 view에 자신의 label을 반환하는 버튼"""
    def __init__(self, label:str, **kwargs):
        super().__init__(label = label,  **kwargs)
        self.label = label

    async def callback(self, button_interaction: discord.Interaction):
        view = self.view
        view.selected_label = self.label
        msg = button_interaction.message
        embed = msg.embeds[0]
        embed.color = discord.Color.green()
        await msg.edit(embed= embed, view= None)
        view.stop()
        await button_interaction.response.defer() 

class SongRegisterView(discord.ui.View):
    """위 songRegisterButton의 반환값을 받기 위한 view"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_label = None


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
