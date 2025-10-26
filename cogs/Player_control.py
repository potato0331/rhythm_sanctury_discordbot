import discord
from discord.ext import commands
from models import Player, RoundSong
from discord import app_commands

# 모든 진행자용 명령어를 담을 그룹 클래스를 정의
# parent를 지정하여 /진행자 OOO 형태의 하위 명령어로
# 명령어를 그룹으로 묶었다는 이유로, 여기서는 self.bot 대신 interaction.client를 사용한다.

@app_commands.guild_only() # 이 명령어 그룹은 서버에서만 사용 가능
@app_commands.default_permissions(manage_guild=True) # 관리자에게만 보이도록 권한 설정
class MasterCommandGroup(app_commands.Group, name="진행자", description="게임 진행과 관련된 명령어 모음입니다."):

    @app_commands.command(name="라운드등록", description="(진행자용 기능)진행자 라운드의 선곡/패널티를 입력합니다.")
    @app_commands.describe(전반후반="전반/후반", 곡명="곡의 제목", 곡레벨="선곡한 곡의 레벨(전반: MX8~15+SC1~11, 후반: SC8~15)", 패널티="그 라운드의 패널티")
    @app_commands.choices(전반후반=[
        app_commands.Choice(name="전반", value="전반"),
        app_commands.Choice(name="후반", value="후반"),
    ])
    async def _master_register_song(self, interaction: discord.Interaction, 전반후반: str="전반", 곡명: str="A", 곡레벨: str="SC1", 패널티: str="없음"):
        if not interaction.client.game_started:
            await interaction.response.send_message("아직 게임이 시작하지 않았습니다.")
            return
        if interaction.client.current_round != 0:
            await interaction.response.send_message(f"이미 라운드가 진행중입니다.")
            return
        
        if 전반후반 == "전반":
            interaction.client.master_first_half = RoundSong(song_name = 곡명, song_level = 곡레벨, round_penalty = 패널티)
        else:
            interaction.client.master_second_half = RoundSong(song_name = 곡명, song_level = 곡레벨, round_penalty = 패널티)

        await interaction.response.send_message(f"진행자 라운드의 {전반후반}전 곡을 {곡명}/{곡레벨}/{패널티}로 설정했습니다.", ephemeral=True)


    @app_commands.command(name="점수수정", description="(진행자용) 플레이어의 총 점수를 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 점수="수정할 총 점수")
    async def score_manage(self, interaction: discord.Interaction, 이름: discord.Member, 점수: int):
        target_status = None
        for status in interaction.client.player_status:
            if status.name == 이름.global_name:
                target_status = status
                break
        
        if target_status is None:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다", ephemeral=True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 점수를 {target_status.score}에서 {점수}로 수정했습니다.", ephemeral=True)
            target_status.score = 점수

    @app_commands.command(name="코인수정", description="(진행자용) 플레이어의 총 코인을 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 코인="수정할 총 코인")
    async def coin_manage(self, interaction: discord.Interaction, 이름: discord.Member, 코인: int):
        target_status = None
        for status in interaction.client.player_status:
            if status.name == 이름.global_name:
                target_status = status
                break
        if target_status is None:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다", ephemeral=True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 코인을 {target_status.coin}에서 {코인}로 수정했습니다.", ephemeral=True)
            target_status.coin = 코인
    
    @app_commands.command(name="현재점수수정", description="(진행자용) 플레이어의 이번 라운드 점수를 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 점수="수정할 이번 라운드 점수")
    async def round_score_manage(self, interaction: discord.Interaction, 이름: discord.Member, 점수: int):
        target_status = None
        for status in interaction.client.player_status:
            if status.name == 이름.global_name:
                target_status = status
                break
        if target_status is None:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다", ephemeral=True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 이번 라운드 점수를 {target_status.round_score}에서 {점수}로 수정했습니다.", ephemeral=True)
            target_status.round_score = 점수

    @app_commands.command(name="배수수정", description="(진행자용) 플레이어의 이번 라운드 배수를 수정합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 배수="수정할 배수")
    async def round_multiplier_manage(self, interaction: discord.Interaction, 이름: discord.Member, 배수: int):
        target_status = None
        for status in interaction.client.player_status:
            if status.name == 이름.global_name:
                target_status = status
                break
        if target_status is None:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다", ephemeral=True)
        else:
            await interaction.response.send_message(f"{target_status.name}님의 배팅 가산값을 {target_status.round_multiplier}에서 {배수}로 수정했습니다.", ephemeral=True)
            target_status.round_multiplier = 배수

    @app_commands.command(name="효과수정", description="(진행자용 기능)원하는 플레이어의 이번 라운드의 적용된 효과를 추가합니다.")
    @app_commands.describe(이름="수정하고 싶은 사람의 닉네임", 추가제거 = "[추가]또는 [제거]입력", 효과="추가하거나 제거할 효과를 정확히")
    @app_commands.choices(추가제거=[
        app_commands.Choice(name="추가", value="추가"),
        app_commands.Choice(name="제거", value="제거"),
    ])
    async def _master_effect_manage(self, interaction: discord.Interaction, 이름: discord.Member, 추가제거: str="추가", 효과: str="효과"):
        target_status = 0
        for status in interaction.client.player_status:
            if status.name == 이름.global_name:
                target_status = status
                break
        if target_status == 0:
            await interaction.response.send_message(f"{이름}님은 플레이어가 아닙니다",ephemeral = True)
        else:
            if 추가제거 == "제거":
                if 효과 in target_status.effect_list:
                    target_status.effect_list.remove(효과)
                    await interaction.response.send_message(f"{target_status.name}님에게 {효과}를 제거했습니다.",ephemeral = True)
                else:
                    await interaction.response.send_message(f"{target_status.name}님에게는 {효과}가 없습니다.",ephemeral = True)
            else: 
                target_status.effect_list.append(효과)
                await interaction.response.send_message(f"{target_status.name}님에게 {효과}를 추가했습니다.",ephemeral = True)


class PlayerControl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # 에러 핸들러는 그대로 유지하여 혹시 모를 에러에 대응합니다.
    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole) or isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("이 명령어는 권한이 있는 사람만 사용할 수 있습니다.", ephemeral=True)
        else:
            await interaction.response.send_message(f"알 수 없는 오류가 발생했습니다: {error}", ephemeral=True)
            print(error)
            
async def setup(bot: commands.Bot):
    # 2. Cog에 개별 명령어가 아닌, 위에서 만든 '그룹'을 추가합니다.
    # guild 인자를 추가하여 특정 서버에서만 명령어를 즉시 동기화하도록 할 수 있습니다. (선택사항)
    bot.tree.add_command(MasterCommandGroup())
    # 기존 Cog 로드는 유지해도 되지만, 그룹으로 묶었으므로 이 Cog는 에러 핸들링 역할만 하게 됩니다.
    await bot.add_cog(PlayerControl(bot))
