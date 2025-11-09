from discord.ext import commands
from discord import app_commands
import discord
from models import User
import config

class Prepare(commands.Cog):

    # Cog 클래스의 생성자(__init__)에서 bot 객체를 인자로 받습니다.
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='플레이어등록', description="연말정산에 참가합니다.")
    async def _register_player(self, interaction: discord.Interaction):
        name = interaction.user.global_name
        
        if self.bot.current_phase != config.Phase.READY:
            await interaction.response.send_message(f"현재는 등록할 수 없습니다.", ephemeral=True)
            return
        
        if not name in self.bot.playerlist:
            self.bot.playerlist.append(name)
            await interaction.response.send_message(f"{name}님을 플레이어로 등록했습니다.")
        else:
            await interaction.response.send_message(f"{name}님은 이미 등록된 플레이어입니다.", ephemeral=True)
    

    @commands.command(name='진행자등록')
    async def _register_master(self, ctx: commands.Context):
     
        if not self.bot.master_player and self.bot.current_phase == config.Phase.READY:
            
            self.bot.master_player = User(ctx.author.id, ctx.author.global_name)
            await ctx.send(f"{ctx.author.global_name}님을 진행자로 등록했습니다.")
            await ctx.send(f"현재 등록된 플레이어는 {self.bot.playerlist}, 진행자는 {self.bot.master_player.name}입니다.")
        else:
            await ctx.send(f"이미 진행자가 등록돼어 있습니다. 혹은, 이미 게임이 시작했습니다.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Prepare(bot)) 
