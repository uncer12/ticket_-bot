import discord
from discord.ui import Button, View, Select
from discord.ext import commands
import asyncio
import env


PREFIX = 'g.'
bot = commands.Bot(command_prefix= PREFIX, intents=discord.Intents.all())
bot.remove_command('help')




################################################################################################
#  [!]   Тикет система                                                                         #
                                                                                               #
GUILD_ID =  905216984881442817 # Ввести идентификатор сервера (ID)                             #
TEAM_ROLE =  1038883143974932480 # Роль которая должна видеть все входящие обращения           #
TIKECT_CHANNEL = 1038886486700986428 # Канал на котором будут открываться билеты.              #
CATEGORY_ID = 1027651153892212806 # Категория в которой должны быть созданны билеты.           #
################################################################################################

################################################################################################
#   [!]    Система оповещения о новых тикетах.
################################################################################################
MODER_TEXT_ID =  1038881483198320680 # Какнал для информирования Представителей о новом тикете
ROLE_MODER_ID =  1038883143974932480 # ID Role Предстапвителя
#################################################################################################


@bot.event
async def on_ready():
    print("ready!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Majestic 5"))


@bot.command(pass_context = True)
async def ticket(ctx, amount = 1):
    await ctx.channel.purge ( limit = amount )
    button1 = Button(label="📩 Создать обращение", style=discord.ButtonStyle.success, custom_id="ticket_button")
    #button2 = Button(label="⛔️ Закрыть тикет", style=discord.ButtonStyle.danger, custom_id="ticket_button_close")
    view = View()
    view.add_item(button1)
    #view.add_item(button2)
    embed = discord.Embed(description=f"Доброго времени суток!\n\nЕсли у Вас возникли вопросы или Вам необходимо записаться на прием, то воспользуйтесь функцией `Создать обращение`", title=f"Обращения в Правительство")
    embed.set_image(url='')

    channel = bot.get_channel(TIKECT_CHANNEL)
    await channel.send(embed=embed, view=view)
    await ctx.reply("Ожидайте")

@bot.event
async def on_interaction(interaction):
    if interaction.channel.id == TIKECT_CHANNEL:
     if "ticket_button" in str(interaction.data):
       guild = bot.get_guild(GUILD_ID)
       for ticket in guild.channels:
        if str(interaction.user.id) in ticket.name :
            embed = discord.Embed(description=f"Здравствуйте, сейчас вы будете перенаправлены в канал с вашим обращением\nНе выходите с данного канала. {ticket.mention}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    category = bot.get_channel(CATEGORY_ID)
    ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user.id}",category=category, topic=f"Ticket von {interaction.user} \nClient-ID: {interaction.user.id}")

    await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE), send_messages=True, read_messages=True, add_reactions=False,
                                        embed_links=True, attach_files=True, read_message_history=True,
                                        external_emojis=True)
    await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                        embed_links=True, attach_files=True, read_message_history=True,
                                        external_emojis=True)
    

    embed = discord.Embed(description=f"Приветствую тебя  {interaction.user.mention}! \n\nВ ближайшее время вам ответит `Представитель правительства` для решения вашей проблемы."
                          f"Ожидайте! \n"
                          f"Для закрытия тикеты используйте команду - `g.close`",
                color=62719)
 

    embed.set_author(name=f"Новое обращение от {interaction.user.id}")

    #button2 = Button(label="⚠️ Закрыть тикет", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    #view = View()
    #view.add_item(button2)

    category2 = bot.get_channel(MODER_TEXT_ID)
    mess_2 = await ticket_channel.send(embed=embed)
    embed = discord.Embed(title="Обращение создано.",
                         description=f"Ваше обращение будет рассмотрено в -> {ticket_channel.mention}",
                         color=discord.colour.Color.green())
   
    await interaction.response.send_message(embed=embed, ephemeral=True)           

    await category2.send(f'<@&1038883143974932480>\n**Создано обращение! ->** {ticket_channel.mention}\n> Оставь реакцию :white_check_mark: если взяли обращение!')

    return   

#Команда удаления обращения после помощи.
@bot.command(pass_context = True)
async def close(ctx, amount = 1):
    await ctx.channel.purge ( limit = amount )
    button5 = Button( label = 'Университет Штата', style=discord.ButtonStyle.blurple, emoji = '🎓')
    button3 = Button( label = 'State Fraction #5', style=discord.ButtonStyle.green, emoji = '❤️')
    #Специальная кнопка для фанатов семьи Lena FamQ
    button4 = Button( label = 'Стать фанатом', style=discord.ButtonStyle.blurple, emoji = '🖖🏼')
    
    view = View()
    view.add_item(button5)
    view.add_item(button3)
    view.add_item(button4)
    if "ticket" in ctx.channel.name:
        embed = discord.Embed(
            description=F"Всего хорошего!",
            color=16711680)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete()
        await ctx.author.send ('**Спасибо за обращение!**', view=view)
    async def button_callback(interaction):
        await interaction.response.send_message(content = 'https://discord.gg/YmzDXQBaW3')
    async def button2_callback(interaction):
        await interaction.response.send_message(content = 'https://discord.gg/HV8dzAmbX3')
    async def button3_callback(interaction):
        await interaction.response.send_message(content = 'https://discord.gg/hME7qbDx8H')

    button3.callback = button_callback
    button4.callback = button2_callback
    button5.callback = button3_callback




bot.run(env.TOKEN)