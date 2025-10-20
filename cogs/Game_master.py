import discord
from discord.ext import commands
from models import Player, RoundSong

class GameMaster(commands.Cog):
    # Cog 클래스의 생성자(__init__)에서 bot 객체를 인자로 받습니다.
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 게임설정값
        self.INITIAL_COIN = 15
        self.ROUND_COIN_FIRST_HALF = 5
        self.ROUND_COIN_SECOND_HALF = 10
        self.MASTER_ROUND_ON_FIRST_ROUND = 0 #0또는 1
        self.MASTER_ROUND_ON_LAST_ROUND = 1 #0또는 1

        # 게임 진행 상태 변수
        self.bot.player_status: list[Player] = []

        self.current_round = 0
        self.total_round = 0
        self.current_half = 1
        self.isscoreinput = False 

    @commands.command(name='게임시작')
    async def _start_game(self, ctx: commands.Context):
        if ctx.author.global_name != self.bot.masterplayer:
            await ctx.send(f"{ctx.author.global_name}님은 진행자가 아닙니다.")
            return
        if self.bot.game_started:
            await ctx.send("게임이 이미 시작했습니다.")
            return
        #게임 초기화
        self.bot.game_started = True
        self.current_round = 0

        #총 라운드 수 계산
        self.total_round = 2 * len(self.bot.playerlist) + self.MASTER_ROUND_ON_FIRST_ROUND + self.MASTER_ROUND_ON_LAST_ROUND

        #player_status 초기화
        self.bot.player_status = [] 
        for name in self.bot.playerlist:
            player = Player(name=name, initial_coin=self.INITIAL_COIN)
            self.bot.player_status.append(player)
        
        await ctx.send(f"게임을 시작하겠습니다. 등록된 플레이어는 {self.bot.playerlist}입니다. 총 라운드 수는 {self.total_round}입니다.")
        await ctx.send(f"곡 등록을 시작합니다.")


    @commands.command(name='곡등록완료')
    async def _end_song_input(self, ctx: commands.Context):
        pass



    @commands.command(name='다음라운드')    
    async def _next_round(self, ctx: commands.Context):
        if not self.bot.game_started:
            await ctx.send("게임이 시작되지 않았습니다.")
            return
        if not self.isscoreinput and self.current_round != 0:
            await ctx.send("점수입력을 하지 않았습니다.[!점수등록완료]를 입력하여 점수를 등록합니다")
            return
        
        if self.current_round == len(self.bot.playerlist) + self.MASTER_ROUND_ON_FIRST_ROUND:
            self.current_half = 2
            await ctx.send(f"전반전이 마무리 돼었습니다. 이제부터는 각 라운드마다 {self.ROUND_COIN_SECOND_HALF}코인이 지급됍니다.")

        if self.current_round != 0:
            for status in self.bot.player_status:
                status.score += status.round_multiplier * status.round_score
                await ctx.send(f"{status.name}님이 {status.round_multiplier} x {status.round_score} = {status.round_multiplier * status.round_score}점을 획득했습니다.")
                status.round_multiplier = 0
                status.round_score = -1
                status.effect_list = []

        self.isscoreinput = False

        if self.current_round == self.total_round:
            await ctx.send("마지막 라운드입니다. [!결과발표]로 결과를 발표합니다.")
            return
        self.current_round += 1

        if self.current_half == 1:
            for status in self.bot.player_status:
                status.coin += self.ROUND_COIN_FIRST_HALF
        else:
            for status in self.bot.player_status:
                status.coin += self.ROUND_COIN_SECOND_HALF

        await ctx.send(f"{self.current_round} 라운드가 시작됩니다.")


    @commands.command(name='점수등록완료')    
    async def _end_score_input(self, ctx: commands.Context):
        player_inputed_flag = True

        for status in self.bot.player_status:
            if status.round_score < 0:
                player_inputed_flag = False
                await ctx.send(f"{status.name}님이 현재 점수를 입력하지 않았거나, 입력한 점수가 음수입니다.")
                
        if player_inputed_flag:
             self.isscoreinput = True
             await ctx.send(f"점수 입력이 완료돼었습니다.")


    @commands.command(name='강제점수등록완료')   #디버깅용
    async def _force_end_score_input(self, ctx: commands.Context):
        self.isscoreinput = True
        await ctx.send(f"점수 입력이 완료돼었습니다.")

    @commands.command(name='플레이어확인')    
    async def _check_player(self, ctx: commands.Context):
        await ctx.send(f"등록된 플레이어: {self.bot.playerlist}")
        if self.bot.game_started:
            await ctx.send(f"현재 플레이어 상태: {self.bot.player_status}")


    @commands.command(name='결과발표')    
    async def _show_result(self, ctx: commands.Context):

        if self.current_round < self.total_round:
            await ctx.send(f"아직 마지막 라운드가 아닙니다.")
            return
        
        highest_score = 0
        await ctx.send("최종결과입니다.")

        for status in self.bot.player_status:
            await ctx.send(f"{status.name}: {status.score}점")

            if highest_score < status.score:
                highest_score = status.score

        for status in self.bot.player_status:
            if highest_score == status.score:
                await ctx.send(f"우승자는...{status.name}.")
        
        await ctx.send(f"게임을 종료합니다. 모두 수고하셨습니다.")

 
async def setup(bot: commands.Bot):
    await bot.add_cog(GameMaster(bot))

