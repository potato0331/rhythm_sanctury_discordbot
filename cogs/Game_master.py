import discord
from discord.ext import commands
from models import Player, RoundSong
import random
import asyncio 
import config 

class GameMaster(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.bot.player_status = []
        self.bot.current_round = 0
        self.bot.total_round = 0
        self.bot.current_half = 0
        self.bot.player_deck = [] # 라운드 진행 순서 덱
        self.bot.roundplayer = 0 
        self.bot.current_card_price = config.CARD_PRICE
        self.bot.current_phase = config.Phase.PERPARE #prepare ->(곡등록완료)-> /반복/ betting ->(배팅완료)-> penalty ->(저격공개)-> card ->(다음라운드)-> /반복/
        #current_phase의 수정은 이 파일에서만 이루어지게 함. 


        self.anonymous_player_list = [] #라운드 패널티 저격할 때, 정렬된 플레이어를 잠깐 저장하는 변수.

    @commands.command(name='게임시작')
    async def _start_game(self, ctx: commands.Context):
        if ctx.author.global_name != self.bot.master_player.name:
            return await ctx.send(f"{ctx.author.global_name}님은 진행자가 아닙니다.")
        if self.bot.game_started:
            return await ctx.send("게임이 이미 시작했습니다.")
        
        # 게임 초기화
        self.bot.game_started = True
        self.bot.current_round = 0
        self.bot.current_half = 0
        self.bot.player_deck = []
        self.bot.current_card_price = config.CARD_PRICE

        # player_status 초기화
        self.bot.player_status = [] 
        for name in self.bot.playerlist:
            player = Player(name=name, initial_coin = config.INITIAL_COIN)
            self.bot.player_status.append(player)

        # 총 라운드 수 계산
        self.bot.total_round = 2 * len(self.bot.playerlist) + config.MASTER_ROUND_ON_FIRST_ROUND + config.MASTER_ROUND_ON_LAST_ROUND
        
        await ctx.send(f"게임을 시작하겠습니다. 등록된 플레이어는 {self.bot.playerlist}입니다. 총 라운드 수는 {self.bot.total_round}입니다.")
        await ctx.send(f"각자 `/선곡등록` 명령어로 전반전/후반전 곡을 등록해주세요.")


    @commands.command(name='곡등록완료') # 1라운드 시작 역할을 겸함
    async def _end_song_input(self, ctx: commands.Context):
        if self.bot.current_round != 0:
            return await ctx.send("이미 라운드가 진행중입니다.")
        
        # 곡 등록 여부 확인
        for status in self.bot.player_status:
            if status.songs[0] == None:
                return await ctx.send(f"{status.name}님이 현재 전반전 곡을 등록하지 않았습니다.")
            if status.songs[1] == None:
                return await ctx.send(f"{status.name}님이 현재 후반전 곡을 등록하지 않았습니다.")

        # 진행자 라운드 곡 등록 확인
        if config.MASTER_ROUND_ON_FIRST_ROUND == 1 and self.bot.master_player.songs[0] == None:
            return await ctx.send(f"진행자님이 현재 전반전 곡을 등록하지 않았습니다.")
        if config.MASTER_ROUND_ON_LAST_ROUND == 1 and self.bot.master_player.songs[1] == None:
            return await ctx.send(f"진행자님이 현재 후반전 곡을 등록하지 않았습니다.")

        await ctx.send("곡 등록이 확인되었습니다.")

        self.bot.player_deck = self.__create_deck()

        # 1라운드 시작 상태 초기화
        for status in self.bot.player_status:
            status.round_multiplier = 0
            status.round_score = -1
            status.effect_list = []
            status.coin += config.ROUND_COIN[0]# 1라운드 코인 지급
            status.saved_pension = 0
                

        self.bot.current_card_price = config.CARD_PRICE

        self.bot.current_round = 1
        await ctx.send("1라운드를 시작하겠습니다. 건투를 빕니다.")

        self.bot.roundplayer = self.bot.player_deck.pop()
        
        await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.songs[0],False)
        print(2)

        self.bot.current_phase = config.Phase.BETTING
        await ctx.send("각자 `/배팅` 명령어로 배팅액을 등록해주세요.")


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
            status.betting = 0
            status.round_score = -1
            status.effect_list = []
            if status.saved_pension != 0: #국민연금 처리
                random_multiplier = random.randint(1,6) - 3
                await ctx.send(f"{status.name}님의 국민연금에 적립돼어 있던 배팅 가산값 {status.saved_pension}이 이자를 붙여서{status.saved_pension + random_multiplier}로 돌아왔습니다!")
                status.round_multiplier += status.saved_pension + random_multiplier
                status.saved_pension = 0
        await ctx.send("--------------------------------")

        # 마지막 라운드인지 확인
        if self.bot.current_round == self.bot.total_round:
            return await ctx.send("모든 라운드가 종료되었습니다. `!결과발표`로 최종 결과를 확인해주세요.")

        self.bot.current_round += 1
        self.bot.current_card_price = config.CARD_PRICE
        
        #전반전이 끝났는지 확인
        if (self.bot.current_round == len(self.bot.playerlist) + config.MASTER_ROUND_ON_FIRST_ROUND + 1):
            self.bot.current_half = 1
            await ctx.send(f"전반전이 종료되었습니다. 이제부터는 각 라운드마다 {config.ROUND_COIN[1]}코인이 지급됩니다.")

        # 코인 지급
        for status in self.bot.player_status:
            status.coin += config.ROUND_COIN[self.bot.current_half]

        await ctx.send(f"{self.bot.current_round} 라운드가 시작됩니다.")

        # 다음 라운드 플레이어 지정
        self.bot.roundplayer = self.bot.player_deck.pop()
        await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.songs[self.bot.current_half],False)

        self.bot.current_phase = config.Phase.BETTING
        await ctx.send("각자 `/배팅` 명령어로 배팅액을 등록해주세요.")


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
        await self.song_reveal(ctx, self.bot.roundplayer.name, self.bot.roundplayer.songs[self.bot.current_half],True)
        
        #배팅액 공개
        sorted_players = sorted(self.bot.player_status, key=lambda p: p.betting)
        self.anonymous_player_list = []
        betting_message = f"{self.bot.current_round}라운드 배팅액:\n"
        for i in range(len(self.bot.player_status)):
            betting_message +=f"{i + 1}번 플레이어: {sorted_players[i].betting}코인\n"
            self.anonymous_player_list.append(sorted_players[i].name)
        self.bot.current_phase = config.Phase.PENALTY
        await ctx.send(betting_message)

    @commands.command(name='저격공개')    
    async def _reveal_player(self, ctx: commands.Context):

        reveal_message = ""

        for i in range(len(self.anonymous_player_list)):
            reveal_message +=f"{i + 1}번 플레이어: {self.anonymous_player_list[i]}\n"
        await ctx.send(reveal_message)
    
        self.bot.current_phase = config.Phase.CARD
        await ctx.send("지금부터 카드를 뽑을 수 있습니다.")


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
        
        temp_score = -99999
        temp_rank = -1

        for i, status in enumerate(sorted_players):
            if(temp_score != status.score):
                temp_score = status.score
                temp_rank = i+1
                await ctx.send(f"**{temp_rank}위**: {status.name} - {temp_score}점")
            else:
                await ctx.send(f"**{temp_rank}위**: {status.name} - {temp_score}점")
            await asyncio.sleep(2)

        highest_score = sorted_players[0].score

        sorted_players.reverse()

        final_winners = [sorted_players.pop().name]

        while (len(sorted_players) > 0 and sorted_players[len(sorted_players)-1].score == highest_score):
            final_winners.append(sorted_players.pop().name)
        
        await ctx.send("--------------------")
        await asyncio.sleep(1)
        await ctx.send(f"우승자는... **{', '.join(final_winners)}** 님입니다! 축하합니다!")
        await ctx.send(f"게임을 종료합니다. 모두 수고하셨습니다.")
        
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

    def __create_deck(self):
        result = []
        if (config.MASTER_ROUND_ON_FIRST_ROUND == 1):
            result.append(self.bot.master_player)

        for i in range(2):
            players = self.bot.player_status.copy()
            random.shuffle(players)
            result.extend(players)
        
        if (config.MASTER_ROUND_ON_LAST_ROUND == 1):
            result.append(self.bot.master_player)
        
        result.reverse()

        return result

async def setup(bot: commands.Bot):
    await bot.add_cog(GameMaster(bot))
    
