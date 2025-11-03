import asyncio
import discord
from discord.ext import commands
from models import Card
from discord import app_commands
import config
import card_list
import random 

class CardDraw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.card_deck: list[Card] = []
        self.__deck_reset()

    def __deck_reset(self):
        for card in card_list.CARDS: #덱 리셋
            for i in range(card.card_count):
                self.card_deck.append(card)
        random.shuffle(self.card_deck)
        

    @app_commands.command(name="카드뽑기", description=f"{config.CARD_PRICE}코인을 지불하고 무작위의 찬스카드 1장을 뽑습니다.")
    async def _draw_card(self, interaction: discord.Interaction):
        player = None
        for status in self.bot.player_status:
            if status.name == interaction.user.global_name:
                player = status
                break

        #예외처리
        if(player == None):
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
            return
        if(self.bot.current_phase != config.Phase.CARD):
            await interaction.response.send_message("지금은 카드를 뽑을 수 없습니다.",ephemeral=True)
            return
        if(player.coin < self.bot.current_card_price):
            await interaction.response.send_message("코인이 부족합니다.",ephemeral = True)
            return

        #코인소모
        player.coin -= self.bot.current_card_price

        #카드 뽑기
        if(len(self.card_deck) == 0):
            self.__deck_reset()
        card = self.card_deck.pop()

        #카드 공표용 엠베드 제작
        embed = discord.Embed()

        embed.set_author(name=interaction.user.global_name, icon_url=interaction.user.avatar.url)

        if(card.type == 1):
            embed.color=discord.Color.green()
        elif(card.type == 2):
            embed.color=discord.Color.yellow()
        else:
            embed.color=discord.Color.red()

        if(card.image_file != ""):
            embed.set_image(url=card.image_file)
        else:
            embed.title = f"{card.name}"
            embed.add_field(name="효과", value=card.description, inline=True)
            embed.add_field(name="가산값", value=str(card.betting_value), inline=True)

        await interaction.response.send_message(embed=embed)

    
        #카드 효과 적용
        player.round_multiplier += card.betting_value
        
        match card.effect_tag:
            case "효과해제":
                player.effect_list.clear()
                await interaction.followup.send(f"{player.name}님의 효과를 전부 제거했습니다.")

            case "코인6":
                player.coin += 6
                await interaction.followup.send(f"{player.name}님이 6코인을 획득했습니다.")

            case "(대상랜덤)배율2":
                if len(self.bot.player_status) < 2:
                        await interaction.followup.send("효과 발동 실패: 소매넣기할 다른 플레이어가 없습니다.")
                        return

                while True:
                    random_player = self.bot.player_status[random.randint(0,len(self.bot.player_status)-1)]
                    if random_player.name != player.name:
                        break
                random_player.round_multiplier += 2
                await interaction.followup.send(f"{player.name}님이 {random_player.name}님에게 배수2만큼 소매넣기 하였습니다.")

            case "코인1+1d6":
                random_coin = random.randint(1,6)
                player.coin += 1 + random_coin
                await interaction.followup.send(f"{player.name}님이 1+{random_coin}코인을 획득했습니다.")       

            case "뽑기할인1":
                self.bot.current_card_price -= 1
                await interaction.followup.send(f"이번 라운드의 랜덤카드 가격이 1코인 감소하여 {self.bot.current_card_price}가 돼었습니다.")   

            case "뽑기할증1":
                self.bot.current_card_price += 1
                await interaction.followup.send(f"이번 라운드의 랜덤카드 가격이 1코인 증가하여 {self.bot.current_card_price}가 돼었습니다.")   
            
            case "연설":
                await interaction.followup.send(f"{player.name}님이 연설을 시작합니다!")
                await asyncio.sleep(90)
                await interaction.followup.send(f"{player.name}님의 연설시간이 30초 남았습니다!")
                await asyncio.sleep(30)
                await interaction.followup.send(f"{player.name}님의 연설시간이 종료돼었습니다!")

            case "국민연금":
                await interaction.followup.send(f"{player.name}님의 배팅 가산값 {player.round_multiplier}만큼이 국민연금에 적립돼었습니다!")
                player.saved_pension += player.round_multiplier
                player.round_multiplier = 0

                             
            case _:
                player.effect_list.append(card.effect_tag)


async def setup(bot: commands.Bot):
    await bot.add_cog(CardDraw(bot))
