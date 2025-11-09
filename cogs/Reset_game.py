import discord
from discord.ext import commands
from models import Player, User, Card
import config 
import pickle
import os 

SAVE_FILE = config.SAVE_FILE

class ResetGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "rb") as f:
                    game_state = pickle.load(f)
                
                # 저장된 상태로 봇 변수들 덮어쓰기
                self.bot.player_status = game_state.get("player_status", [])
                self.bot.current_round = game_state.get("current_round", 0)
                self.bot.total_round = game_state.get("total_round", 0)
                self.bot.current_half = game_state.get("current_half", 0)
                self.bot.player_deck = game_state.get("player_deck", [])
                self.bot.roundplayer = game_state.get("roundplayer", 0)
                self.bot.current_card_price = game_state.get("current_card_price", config.CARD_PRICE)
                self.bot.current_phase = game_state.get("current_phase", config.Phase.BETTING)
                self.bot.game_started = game_state.get("game_started", False) 
                self.bot.playerlist = game_state.get("playerlist", [])      
                self.bot.master_player = game_state.get("master_player", None) 
                self.bot.card_deck = game_state.get("card_deck", [])

                print("=== 게임 상태 복원 완료 ===")

            except Exception as e:
                print(f"게임 상태 복원 실패: {e}")
                self.__initialize_state() # ◀ 4. 실패 시 초기화
        else:
            self.__initialize_state() # ◀ 4. 파일 없으면 초기화
            
        self.anonymous_player_list = []

    def __initialize_state(self):
        self.bot.player_status = []
        self.bot.current_round = 0
        self.bot.total_round = 0
        self.bot.current_half = 0
        self.bot.player_deck = []
        self.bot.roundplayer = 0 
        self.bot.current_card_price = config.CARD_PRICE
        self.bot.current_phase = config.Phase.READY
        self.bot.game_started = False
        self.bot.playerlist = []
        self.bot.master_player = None
        self.bot.card_deck = []
        print("=== 게임 상태 초기화 완료 ===")
        
    def save_game_state(self):
        try:
            game_state = {
                "player_status": self.bot.player_status,
                "current_round": self.bot.current_round,
                "total_round": self.bot.total_round,
                "current_half": self.bot.current_half,
                "player_deck": self.bot.player_deck,
                "roundplayer": self.bot.roundplayer,
                "current_card_price": self.bot.current_card_price,
                "current_phase": self.bot.current_phase,
                "game_started": self.bot.game_started,
                "playerlist": self.bot.playerlist,
                "master_player": self.bot.master_player,
                "card_deck": self.bot.card_deck
            }
            
            with open(SAVE_FILE, "wb") as f:
                pickle.dump(game_state, f)
            print("게임 상태 저장 완료.")

        except Exception as e:
            print(f"!!! 게임 상태 저장 실패: {e}")


    @commands.command(name='초기화')
    async def _reset_game(self, ctx: commands.Context):
        self.bot.player_status = []
        self.bot.current_round = 0
        self.bot.total_round = 0
        self.bot.current_half = 0
        self.bot.player_deck = [] # 라운드 진행 순서 덱
        self.bot.roundplayer = 0 
        self.bot.current_card_price = config.CARD_PRICE
        self.bot.card_deck: list[Card] = []
        self.bot.playerlist = []
        self.bot.master_player = None
        self.bot.current_phase = config.Phase.READY

        if os.path.exists(config.SAVE_FILE):
            os.remove(config.SAVE_FILE)
        await ctx.send("저장된 게임 상태 파일을 삭제했습니다.")

        await ctx.send(f"리셋이 완료 돼었습니다.")


async def setup(bot: commands.Bot):
    await bot.add_cog(ResetGame(bot))




       