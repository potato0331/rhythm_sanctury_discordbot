import time
import discord
from discord.ext import commands
from models import Player, RoundSong
import random
import asyncio # [추가됨] 비동기 sleep을 위해 import

class GameMaster(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 게임설정값
        self.INITIAL_COIN = 15
        self.ROUND_COIN_FIRST_HALF = 5
        self.ROUND_COIN_SECOND_HALF = 10
        self.MASTER_ROUND_ON_FIRST_ROUND = 0 # 0 또는 1
        self.MASTER_ROUND_ON_LAST_ROUND = 1 # 0 또는 1

        self.bot.player_status: list[Player] = []
        self.bot.master_first_half = RoundSong(song_name="", song_level="", round_penalty="")
        self.bot.master_second_half = RoundSong(song_name="", song_level="", round_penalty="")
        self.bot.current_round = 0
        self.bot.total_round = 0
        self.bot.current_half = 1
        self.bot.player_deck = [] # 라운드 진행 순서 덱
        self.bot.roundplayer: Player = 0
        self.bot.is_card_draw_possible = False

        self.anonymous_player_list = [] #라운드 패널티 저격할 때, 정렬된 플레이어를 잠깐 저장하는 변수.


    async def song_reveal(self, ctx: commands.Context, player: str, song: RoundSong, open_penalty: bool):
        """곡의 정보 (+패널티)를 임베드로 출력"""
        embed = discord.Embed(
            title=f"{self.bot.current_round} 라운드",
            description=f"이번 라운드의 플레이어는 **{player}** 님입니다.",
            color=discord.Color.green()
        )
        embed.add_field(name="곡명", value=song.song_name, inline=True)
        embed.add_field(name="레벨", value=song.song_level, inline=True)
        if open_penalty:
            embed.add_field(name="패널티", value=song.round_penalty, inline=True)
        await ctx.send(embed=embed)


    @commands.command(name='게임시작')
    async def _start_game(self, ctx: commands.Context):
        if ctx.author.global_name != self.bot.masterplayer:
            return await ctx.send(f"{ctx.author.global_name}님은 진행자가 아닙니다.")
        if self.bot.game_started:
            return await ctx.send("게임이 이미 시작했습니다.")
        
        # 게임 초기화
        self.bot.game_started = True
        self.bot.current_round = 0
        self.bot.current_half = 1
        self.bot.master_first_half = RoundSong(song_name="", song_level="", round_penalty="")
        self.bot.master_second_half = RoundSong(song_name="", song_level="", round_penalty="")
        self.bot.player_deck = []

        # player_status 초기화
        self.bot.player_status = [] 
        for name in self.bot.playerlist:
            player = Player(name=name, initial_coin=self.INITIAL_COIN)
            self.bot.player_status.append(player)

        # 총 라운드 수 계산
        self.bot.total_round = 2 * len(self.bot.playerlist) + self.MASTER_ROUND_ON_FIRST_ROUND + self.MASTER_ROUND_ON_LAST_ROUND
        
        await ctx.send(f"게임을 시작하겠습니다. 등록된 플레이어는 {self.bot.playerlist}입니다. 총 라운드 수는 {self.bot.total_round}입니다.")
        await ctx.send(f"각자 `/선곡등록` 명령어로 전반전/후반전 곡을 등록해주세요.")


    @commands.command(name='곡등록완료') # 1라운드 시작 역할을 겸함
    async def _end_song_input(self, ctx: commands.Context):
        if self.bot.current_round != 0:
            return await ctx.send("이미 라운드가 진행중입니다.")
        
        # 곡 등록 여부 확인
        for status in self.bot.player_status:
            if status.first_half.song_name == "":
                return await ctx.send(f"{status.name}님이 현재 전반전 곡을 등록하지 않았습니다.")
            if status.second_half.song_name == "":
                return await ctx.send(f"{status.name}님이 현재 후반전 곡을 등록하지 않았습니다.")

        # 진행자 라운드 곡 등록 확인
        if self.MASTER_ROUND_ON_FIRST_ROUND == 1 and self.bot.master_first_half.song_name == "":
            return await ctx.send(f"진행자님이 현재 전반전 곡을 등록하지 않았습니다.")
        if self.MASTER_ROUND_ON_LAST_ROUND == 1 and self.bot.master_second_half.song_name == "":
            return await ctx.send(f"진행자님이 현재 후반전 곡을 등록하지 않았습니다.")

        await ctx.send("곡 등록이 확인되었습니다.")
        
        self.bot.player_deck = self.bot.player_status.copy()
        random.shuffle(self.bot.player_deck)

        # 1라운드 시작 상태 초기화
        for status in self.bot.player_status:
            status.round_multiplier = 0
            status.round_score = -1
            status.effect_list = []
            status.coin += self.ROUND_COIN_FIRST_HALF # 1라운드 코인 지급

        self.bot.current_round = 1
        await ctx.send("1라운드를 시작하겠습니다. 건투를 빕니다.")

        # 1라운드 플레이어 지정
        if self.MASTER_ROUND_ON_FIRST_ROUND == 1:
            await self.song_reveal(ctx, self.bot.masterplayer, self.bot.master_first_half,False)
        else: 
            self.bot.roundplayer = self.bot.player_deck.pop()
            await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.first_half,False)


    @commands.command(name='다음라운드')    
    async def _next_round(self, ctx: commands.Context):
        if not self.bot.game_started:
            return await ctx.send("게임이 시작되지 않았습니다.")
        if self.bot.current_round == 0:
            return await ctx.send("아직 1라운드도 시작하지 않았습니다. `!곡등록완료`를 먼저 입력해주세요.")

        # 점수 입력 확인
        for status in self.bot.player_status:
            if status.round_score < 0:
                return await ctx.send(f"{status.name}님이 현재 점수를 입력하지 않았습니다. (`/점수입력` 필요)")

        # 점수 계산
        await ctx.send("--------------------------------")
        for status in self.bot.player_status:
            points_earned = status.round_multiplier * status.round_score
            status.score += points_earned
            await ctx.send(f"{status.name}님이 {points_earned}점을 획득했습니다.({status.round_multiplier} * {status.round_score})")
            
            # 라운드 상태 초기화
            status.round_multiplier = 0
            status.round_score = -1
            status.effect_list = []
        await ctx.send("--------------------------------")

        # 마지막 라운드인지 확인
        if self.bot.current_round == self.bot.total_round:
            return await ctx.send("모든 라운드가 종료되었습니다. `!결과발표`로 최종 결과를 확인해주세요.")

        self.bot.current_round += 1
        self.bot.is_card_draw_possible = False
        
        #전반전이 끝났는지 확인
        if len(self.bot.player_deck) == 0 and self.bot.current_half == 1:
            self.bot.current_half = 2
            await ctx.send(f"전반전이 종료되었습니다. 이제부터는 각 라운드마다 {self.ROUND_COIN_SECOND_HALF}코인이 지급됩니다.")
            
            # 후반전 덱 재구성
            self.bot.player_deck = self.bot.player_status.copy()
            random.shuffle(self.bot.player_deck)

        # 코인 지급
        if self.bot.current_half == 1:
            for status in self.bot.player_status:
                status.coin += self.ROUND_COIN_FIRST_HALF
        else:
            for status in self.bot.player_status:
                status.coin += self.ROUND_COIN_SECOND_HALF

        await ctx.send(f"{self.bot.current_round} 라운드가 시작됩니다.")

        # 다음 라운드 플레이어 지정
            # 전반전 
        if self.bot.current_half == 1: 
            self.bot.roundplayer = self.bot.player_deck.pop()
            await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.first_half,False)

            # 후반전 마지막 라운드 + 마스터 라운드인 경우     
        elif len(self.bot.player_deck) == 0 and self.bot.current_half == 2 and self.MASTER_ROUND_ON_LAST_ROUND == 1:
            await self.song_reveal(ctx, self.bot.masterplayer, self.bot.master_second_half,False) 

            # 후반전 일반 라운드
        else:
            self.bot.roundplayer = self.bot.player_deck.pop()
            await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.second_half,False)


    @commands.command(name='배팅완료')    
    async def _end_betting(self, ctx: commands.Context):
        if not self.bot.game_started:
            return await ctx.send("게임이 시작되지 않았습니다.")
        if self.bot.current_round == 0:
            return await ctx.send("아직 1라운드도 시작하지 않았습니다. `!곡등록완료`를 먼저 입력해주세요.")

        # 점수 입력 확인
        for status in self.bot.player_status:
            if status.betting <= 0:
                return await ctx.send(f"{status.name}님이 현재 배팅하지 않았습니다. (`/배팅` 필요)")
            
        for status in self.bot.player_status:
            status.round_multiplier = status.betting
        
        await ctx.send(f"{self.bot.current_round}라운드 배팅이 완료돼었습니다. 라운드패널티를 공개합니다.")

        #패널티 공개(곡 공개함수 재활용)
        if self.MASTER_ROUND_ON_FIRST_ROUND == 1 and self.bot.current_round == 1:
            await self.song_reveal(ctx, self.bot.masterplayer, self.bot.master_first_half, True)
        elif self.MASTER_ROUND_ON_LAST_ROUND == 1 and self.bot.current_round == self.bot.total_round:
            await self.song_reveal(ctx, self.bot.masterplayer, self.bot.master_secon_half, True)
        elif self.bot.current_half == 1:
            await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.first_half, True)
        else: 
            await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.first_half, True)

        #배팅액 공개
        sorted_players = sorted(self.bot.player_status, key=lambda p: p.betting)

        embed = discord.Embed(
            title=f"{self.bot.current_round} 라운드",
            description=f"이번 라운드의 플레이어는 **{self.bot.roundplayer.name}** 님입니다.",
            color=discord.Color.green()
        )
        self.anonymous_player_list = []
        betting_message = f"{self.bot.current_round}라운드 배팅액:\n"

        for i in range(len(self.bot.player_status)):
            betting_message +=f"{i + 1}번 플레이어: {sorted_players[i].betting}코인\n"
            self.anonymous_player_list.append(sorted_players[i].name)
        await ctx.send(betting_message)
        

    @commands.command(name='저격공개')    
    async def _reveal_player(self, ctx: commands.Context):

        reveal_message = ""

        for i in range(len(self.anonymous_player_list)):
            reveal_message +=f"{i + 1}번 플레이어: {self.anonymous_player_list[i]}\n"
        await ctx.send(reveal_message)
    
        self.bot.is_card_draw_possible = True



    @commands.command(name='플레이어확인')    
    async def _check_player(self, ctx: commands.Context):
        await ctx.send(f"등록된 플레이어: {self.bot.playerlist}")
        if self.bot.game_started and self.bot.player_status:
            await ctx.send(f"현재 플레이어 상태: {self.bot.player_status}")
        else:
            await ctx.send("게임이 시작되지 않았거나 플레이어 상태 정보가 없습니다.")


    @commands.command(name='결과발표')    
    async def _show_result(self, ctx: commands.Context):
        if self.bot.current_round < self.bot.total_round:
            return await ctx.send(f"아직 마지막 라운드가 아닙니다. (현재 {self.bot.current_round}/{self.bot.total_round})")
        
        await ctx.send("--- 🏆 최종결과 🏆 ---")

        # 점수 기준으로 내림차순 정렬
        sorted_players = sorted(self.bot.player_status, key=lambda p: p.score, reverse=True)
        
        highest_score = -99999
        winners = []

        for i, status in enumerate(sorted_players):
            await ctx.send(f"**{i+1}위**: {status.name} - {status.score}점")
            await asyncio.sleep(2) 

            if status.score >= highest_score:
                highest_score = status.score
                winners.append(status.name)

        # 최고 점수 동점자 처리 제미나이 이놈 코드 진짜 잘쓰네
        final_winners = [name for name in winners if any(p.name == name and p.score == highest_score for p in sorted_players)]

        await asyncio.sleep(1)
        await ctx.send("--------------------")
        await ctx.send(f"우승자는... **{', '.join(final_winners)}** 님입니다! 축하합니다!")
        await ctx.send(f"게임을 종료합니다. 모두 수고하셨습니다.")

async def setup(bot: commands.Bot):
    await bot.add_cog(GameMaster(bot))