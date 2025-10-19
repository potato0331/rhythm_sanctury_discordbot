import discord
from discord.ext import commands

class Prepare(commands.Cog):

    # Cog 클래스의 생성자(__init__)에서 bot 객체를 인자로 받습니다.
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.playerlist = []
        self.bot.masterplayer = ""
        self.bot.game_started = False

    @commands.command(name='초기화')    
    async def _reset_game(self, ctx: commands.Context):
        self.bot.playerlist = []
        self.bot.player_status = []
        self.bot.masterplayer = ""
        self.bot.game_started = False

        await ctx.send(f"리셋이 완료 돼었습니다.")

    @commands.command(name='플레이어등록')
    async def _register_player(self, ctx: commands.Context):
        
        if self.bot.playerlist.count(ctx.author.global_name) == 0 and not self.bot.game_started:
            self.bot.playerlist.append(ctx.author.global_name)
            await ctx.send(f"{ctx.author.global_name}님을 플레이어로 등록했습니다.")
            await ctx.send(f"현재 등록된 플레이어는 {self.bot.playerlist}, 진행자는 {self.bot.masterplayer}입니다.")
        else:
            await ctx.send(f"{ctx.author.global_name}님은 이미 등록된 플레이어입니다.")
    

    @commands.command(name='진행자등록')
    async def _register_master(self, ctx: commands.Context):
     
        if self.bot.masterplayer == "" and not self.bot.game_started:
            self.bot.masterplayer = ctx.author.global_name
            await ctx.send(f"{ctx.author.global_name}님을 진행자로 등록했습니다.")
            await ctx.send(f"현재 등록된 플레이어는 {self.bot.playerlist}, 진행자는 {self.bot.masterplayer}입니다.")
        else:
            await ctx.send(f"이미 진행자가 등록돼어 있습니다.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Prepare(bot)) # Greetings 클래스의 인스턴스를 생성하여 봇에 Cog로 추가합니다.
