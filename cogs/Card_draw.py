import discord
from discord.ext import commands
from models import Player, RoundSong, Card
from discord import app_commands
import config
import card_list
import random 

class CardDraw(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.card_deck: list[Card] = []
        self.deck_reset()

    def deck_reset(self):
        for card in card_list.CARDS: #덱 리셋
            for i in range(card.card_count):
                self.card_deck.append(card)
        random.shuffle(self.card_deck)
        

    @app_commands.command(name="카드뽑기", description=f"{config.CARD_PRICE}코인을 지불하고 무작위의 찬스카드 1장을 뽑습니다.")
    async def _draw_card(self, interaction: discord.Interaction):
        my_status = 0
        for status in self.bot.player_status:
            if status.name == interaction.user.global_name:
                my_status = status
                break

        #예외처리
        if my_status == 0:
            await interaction.response.send_message(f"{interaction.user.global_name}님은 플레이어가 아닙니다. 또는 알 수 없는 오류가 발생했습니다.",ephemeral = True)
            return
        if not self.bot.current_phase == "card":
            await interaction.response.send_message("지금은 카드를 뽑을 수 없습니다.")
            return
        if my_status.coin < config.CARD_PRICE:
            await interaction.response.send_message("코인이 부족합니다.",ephemeral = True)
            return

        #코인소모
        my_status.coin -= config.CARD_PRICE

        #카드 뽑기
        if len(self.card_deck) == 0:
            self.deck_reset()
        card = self.card_deck.pop()

        #카드 효과 적용
        my_status.round_multiplier += card.betting_value
        my_status.effect_list.append(card.effect_tag)

        #카드 공표용 엠베드 제작
        embed = discord.Embed()

        embed.set_author(name=interaction.user.global_name, icon_url=interaction.user.avatar.url)

        if card.type == 1:
            embed.color=discord.Color.green()
        elif card.type == 2:
            embed.color=discord.Color.yellow()
        else:
            embed.color=discord.Color.red()

        if card.image_file != "":
            embed.set_image(url=card.image_file)
        else:
            embed.title = f"{card.name}"
            embed.add_field(name="효과", value=card.description, inline=True)
            embed.add_field(name="가산값", value=str(card.betting_value), inline=True)

        await interaction.response.send_message(embed=embed)








async def setup(bot: commands.Bot):
    await bot.add_cog(CardDraw(bot))
