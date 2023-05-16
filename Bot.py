import discord
from discord.ext import commands
from collections import defaultdict
from historique_node import CommandHistory
from Arbre_node import BotConversation
from protected_node_history import command_history_lock

intents = discord.Intents.all()
client = commands.Bot(command_prefix="?", intents=intents)
history = CommandHistory()
conversation = BotConversation()

# Création de la table de hachage pour stocker l'historique des commandes
command_history = defaultdict(list)

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):  # Vérifie si le bot est mentionné dans le message
        await message.channel.send("J'ai été mentionné !")  # Répond au message de mention

    await client.process_commands(message)  # Traite les autres commandes


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Bonjour!')

    await client.process_commands(message)

    # Ajout de la commande dans l'historique de l'utilisateur
    command_history[message.author.id].append(message.content)

@client.command(name="reset")
async def reset(ctx):
    conversation.reset()
    await ctx.send("La conversation a été réinitialisée.")

@client.command(name="parle_de")
async def parle_de(ctx, *, topic=None):
    if topic is None:
        await ctx.send("Veuillez spécifier un sujet.")
    else:
        if conversation.speak_about(topic):
            await ctx.send(f"Oui, je peux parler de {topic}.")
        else:
            await ctx.send(f"Non, je ne parle pas de {topic}.")

@client.command(name="next_question")
async def next_question(ctx):
    question = conversation.get_next_question()
    if question is not None:
        await ctx.send(question)
    else:
        await ctx.send("Je n'ai pas de question supplémentaire pour le moment.")

@client.command(name="answer")
async def answer(ctx, user_answer):
    conversation.process_answer(user_answer)
    await ctx.send("Réponse traitée.")

@client.command(name="delete")
async def delete(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
    print("Suppression activée")
    history.add_command("delete", ctx.author.name)  # Ajout de la commande dans l'historique

@client.command(name="previous")
async def previous(ctx):
    command = history.get_previous_command()
    if command:
        await ctx.send(f"Commande précédente : {command.command_name}, par {command.arguments}")
    else:
        await ctx.send("Aucune commande précédente trouvée")

@client.command(name="next")
async def next(ctx):
    command = history.get_next_command()
    if command:
        await ctx.send(f"Commande suivante : {command.command_name}, par {command.arguments}")
    else:
        await ctx.send("Aucune commande suivante trouvée")

@client.command(name="add_command")
async def add_command(ctx, command_name, *arguments):
    arguments_str = " ".join(arguments)
    history.add_command(command_name, arguments_str)
    await ctx.send(f"Commande ajoutée à l'historique : {command_name} {arguments_str}")

@client.command(name="get_user_commands")
async def get_user_commands(ctx, user_id):
    commands = history.get_commands_by_user(user_id)
    if commands:
        await ctx.send(f"Commandes de l'utilisateur {user_id} :")
        for command in commands:
            await ctx.send(f"- {command}")
    else:
        await ctx.send(f"Aucune commande enregistrée pour l'utilisateur {user_id}")

@client.command(name="clear_history")
async def clear_history(ctx):
    history.clear()
    await ctx.send("Historique vidé")

@client.event
async def on_ready():
    print("Bot is ready.")

@client.command(name="cmd_add")
async def add_command(ctx, command_name, *arguments):
    arguments_str = " ".join(arguments)

    # Verrouillage de l'accès à la file de l'historique
    with command_history_lock:
        # Ajout de la commande dans l'historique
        command_history.put((command_name, arguments_str))

    await ctx.send(f"Commande ajoutée à l'historique : {command_name} {arguments_str}")

@client.command(name="get_commands")
async def get_commands(ctx):
    # Vérification si un autre utilisateur accède déjà à l'historique
    if command_history_lock.acquire(blocking=False):
        try:
            commands = []
            while not command_history.empty():
                command = command_history.get()
                commands.append(command)
            
            await ctx.send("Historique des commandes :")
            for command in commands:
                await ctx.send(f"- {command[0]} {command[1]}")
        finally:
            command_history_lock.release()
    else:
        await ctx.send("L'historique est actuellement en cours d'accès par une autre personne.")

client.run('MTEwNzkyOTE5MTMwMDcyNjgyNw.GnYCyL.-dBH2xyL6gch-gBLVQRZdTd83Te1L3H_DXCyKk')
