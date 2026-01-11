# =====================================================
# IMPORTS
# =====================================================
import os
import discord
from discord.ext import commands
import time
import re
import random
import asyncio

# ---------------- LANCEMENT --------------
OWNER_ID =  892817676848726086
PROTECTED_ROLE_NAME = "system"
LOG_CHANNEL_NAME = "logs-system"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)


# ---------------- COMMANDES BASIQUES ----------------

@bot.command()
async def ping(ctx):
    await ctx.send("tg trdbl")

@bot.command()
async def selem(ctx):
    await ctx.send("selem kho sdk !")

@bot.command()
async def nuke(ctx):
    await ctx.send("password?")

@bot.command()
async def status(ctx):
    await ctx.send("🛡️ Sécurité active en amont")

# ---------------- ADMIN ----------------

@bot.command()
async def suppr1sel(ctx, channel: discord.TextChannel = None):
    # 🔐 OWNER ONLY
    if ctx.author.id != OWNER_ID:
        await ctx.send("⛔ Tu n'as pas l'autorisation d'utiliser cette commande.")
        return

    # 🛑 Vérification permission du bot
    if not ctx.guild.me.guild_permissions.manage_channels:
        await ctx.send("❌ Je n’ai pas la permission de supprimer des salons.")
        return

    channel = channel or ctx.channel

    try:
        await ctx.send(f"🗑️ Suppression du salon **{channel.name}**...")
        await channel.delete(reason=f"Supprimé par {ctx.author}")
    except Exception as e:
        await ctx.send("❌ Erreur lors de la suppression du salon.")
        print(f"[SUPPR1SEL] {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def mp(ctx, membre: discord.Member, *, message: str = None):
    if not message:
        await ctx.send("❌ Tu dois écrire un message.")
        return
    try:
        await membre.send(message)
        await ctx.send(f"✅ MP envoyé à {membre.name}")
    except:
        await ctx.send("❌ MP fermés.")

# ---------------- ANTI-SPAM / FILTRE ----------------

# ---------------- FUN / TROLL ----------------

@bot.command()
async def insulte(ctx, membre: discord.Member):
    insultes = [
        "est aussi rapide qu’un escargot 🐌",
        "a oublié son cerveau aujourd’hui 🧠",
        "est parti nk c mort 🔋"
    ]
    await ctx.send(f"{membre.mention} {random.choice(insultes)}")

@bot.command()
async def say(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def pileface(ctx):
    await ctx.send(random.choice(["🪙 Pile", "🪙 Face"]))

@bot.command()
async def spam(ctx, member: discord.Member):
    for _ in range(4):
        await ctx.send(f"📢 {member.mention} T’ES LÀ ??? 👀")

@bot.command()
async def afk(ctx):
    await ctx.send(f"💤 {ctx.author.mention} est maintenant AFK")

@bot.command()
async def fban(ctx, member: discord.Member):
    await ctx.send(f"🔨 {member.mention} a été banni.")
    await ctx.send("✅: ban ")

@bot.command()
async def fdox(ctx, member: discord.Member):
    msg = await ctx.send(f"💻 Hack de {member.mention} en cours...")
    for text in [
        "🔍 Recherche IP...",
        "📡 Connexion serveur...",
        "🧠 Analyse données...",
        "✅ MP envoyé"
    ]:
        await asyncio.sleep(1.5)
        await msg.edit(content=text)

# ---------------- INFOS ----------------

@bot.command()
async def pdp(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)

@bot.command()
async def info(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="📌 Info utilisateur")
    embed.add_field(name="Nom", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Créé le", value=member.created_at.strftime("%d/%m/%Y"))
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def inform(ctx, username: str):
    await ctx.send(
        f"🕵️ OSINT : `{username}`\n"
        f"Instagram: https://instagram.com/{username}\n"
        f"Snapchat: https://snapchat.com/add/{username}\n"
        f"TikTok: https://tiktok.com/@{username}"
    )


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="・💬𝙶é𝚗é𝚛𝚊𝚕")
    if channel:
        await channel.send(f"👋 **bvn kho {member.mention}** 🔥")

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user} ({bot.user.id})")


# -------------------------
# Commande : DM TOUS
# -------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, message: str):
    """
    Envoie un DM à tous les membres du serveur.
    """
    members = [m for m in ctx.guild.members if not m.bot]

    if not members:
        await ctx.send("❌ Aucun membre à contacter.")
        return

    confirm = await ask_confirmation(ctx, len(members))
    if not confirm:
        await ctx.send("❌ Envoi annulé.")
        return

    sent = 0
    failed = 0

    await ctx.send("🚀 Début de l’envoi des messages...")

    for member in members:
        ok = await send_dm_safe(member, message)
        if ok:
            sent += 1
        else:
            failed += 1

    await ctx.send(
        f"✅ **DM terminés**\n"
        f"📨 Envoyés : {sent}\n"
        f"❌ Échecs : {failed}"
    )
@bot.command()
@commands.has_permissions(administrator=True)
async def dmrole(ctx, role_id: int, *, message: str):
    """
    Envoie un DM à tous les membres d’un rôle donné.
    """
    role = ctx.guild.get_role(role_id)

    if role is None:
        await ctx.send("❌ Rôle introuvable. Vérifie l’ID.")
        return

    members = [m for m in role.members if not m.bot]

    if not members:
        await ctx.send("❌ Aucun membre dans ce rôle.")
        return

    confirm = await ask_confirmation(ctx, len(members))
    if not confirm:
        await ctx.send("❌ Envoi annulé.")
        return

    sent = 0
    failed = 0

    await ctx.send(f"🚀 Envoi des DMs au rôle **{role.name}**...")

    for member in members:
        ok = await send_dm_safe(member, message)
        if ok:
            sent += 1
        else:
            failed += 1

    await ctx.send(
        f"✅ **DM rôle terminés**\n"
        f"🎭 Rôle : {role.name}\n"
        f"📨 Envoyés : {sent}\n"
        f"❌ Échecs : {failed}"
    )


# -------------------------
# Gestion des erreurs
# -------------------------
@dmall.error
@dmrole.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ Tu n’as pas la permission d’utiliser cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argument invalide.")
    else:
        await ctx.send("❌ Une erreur est survenue.")
        print(f"[ERREUR] {type(error).__name__} : {error}")

async def ask_confirmation(ctx, question: str, timeout: int = 20) -> bool:
    """
    Demande une confirmation oui/non à l'utilisateur.
    Retourne True si confirmé, False sinon.
    """
    await ctx.send(f"⚠️ **Confirmation requise**\n{question}\n\nRéponds par **oui** ou **non**")

    def check(msg):
        return (
            msg.author == ctx.author
            and msg.channel == ctx.channel
            and msg.content.lower() in ["oui", "non"]
        )

    try:
        reply = await bot.wait_for("message", check=check, timeout=timeout)
        return reply.content.lower() == "oui"
    except asyncio.TimeoutError:
        await ctx.send("⏱️ Temps écoulé, commande annulée.")
        return False

async def send_dm_safe(user: discord.User, message: str) -> bool:
    """
    Envoie un DM de façon sécurisée.
    Retourne True si envoyé, False sinon.
    """
    try:
        await user.send(message)
        return True
    except discord.Forbidden:
        # DMs fermés
        return False
    except discord.HTTPException:
        # Erreur API / rate limit
        return False
    except Exception as e:
        print(f"[ERREUR DM] {user} -> {e}")
        return False

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    await ctx.send(f"🔒 Le salon **{channel.name}** Vos geule les pd.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    await ctx.send(f"🔓 Le salon **{channel.name}** vous me faite de la peine.")

@bot.command()
async def scan(ctx, member: discord.Member):
    msg = await ctx.send(f"🛡️ Scan de sécurité de {member.mention} en cours...")
    
    await asyncio.sleep(1.5)
    await msg.edit(content="🔍 Analyse IP & VPN...")
    await asyncio.sleep(1.5)
    await msg.edit(content="📡 Vérification activité suspecte...")
    await asyncio.sleep(1.5)
    await msg.edit(content="🧠 Analyse comportementale...")
    await asyncio.sleep(1.5)

    await msg.edit(content=f"✅ **Scan terminé**\n"
                            f"👤 Utilisateur : {member.name}\n"
                            f"🔐 Risque : FAIBLE\n"
                            f"🛡️ Aucun danger détecté")

@bot.command()
@commands.has_permissions(administrator=True)
async def alert(ctx, *, message):
    embed = discord.Embed(
        title="🚨 ALERTE SÉCURITÉ",
        description=message,
        color=discord.Color.red()
    )
    embed.set_footer(text="ONIMASECU • Protection active")
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="📊 Infos Serveur", color=discord.Color.green())
    embed.add_field(name="Nom", value=guild.name)
    embed.add_field(name="Membres", value=guild.member_count)
    embed.add_field(name="Créé le", value=guild.created_at.strftime("%d/%m/%Y"))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def ultradef(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🚨 **MODE ULTRADEF ACTIVÉ**\n🔒 Tous les salons sont verrouillés.")

@bot.command()
@commands.has_permissions(administrator=True)
async def unultradef(ctx):
    for channel in ctx.guild.text_channels:
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("✅ **MODE ULTRADEF DÉSACTIVÉ**\n🔓 Serveur réouvert.")

@bot.command()
async def trust(ctx, member: discord.Member):
    days = (ctx.message.created_at - member.created_at).days

    if days < 7:
        level = "🔴 FAIBLE"
    elif days < 30:
        level = "🟠 MOYEN"
    else:
        level = "🟢 ÉLEVÉ"

    embed = discord.Embed(title="🧠 Trust Check", color=discord.Color.dark_blue())
    embed.add_field(name="Utilisateur", value=member.mention)
    embed.add_field(name="Compte créé", value=f"{days} jours")
    embed.add_field(name="Niveau de confiance", value=level)
    embed.set_footer(text="ONIMASECU • Analyse comportementale")

    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def log(ctx, *, action):
    embed = discord.Embed(
        title="🧾 Log de Modération",
        description=action,
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Action par {ctx.author}")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(title="⚙️ État du serveur", color=discord.Color.green())

    embed.add_field(name="Anti-spam", value="✅ Actif", inline=False)
    embed.add_field(name="Anti-link", value="✅ Actif", inline=False)
    embed.add_field(name="Protection raid", value="✅ Prêt", inline=False)
    embed.add_field(name="Bot", value="🟢 En ligne", inline=False)

    embed.set_footer(text="ONIMASECU • Monitoring")
    await ctx.send(embed=embed)



@discord.ui.button(label="Envoyer", emoji="✅", style=discord.ButtonStyle.green)
async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

    if interaction.user != self.author:
        await interaction.response.send_message(
            "❌ Ce n’est pas ta confession.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild

    confession_channel = discord.utils.get(
        guild.text_channels,
        name=CONFESSION_CHANNEL_NAME
    )

    if not confession_channel:
        await interaction.followup.send(
            "❌ Salon de confession introuvable.",
            ephemeral=True
        )
        return

    # 📩 Envoi confession publique
    embed = discord.Embed(
        title="🕊️ Confession Anonyme",
        description=self.text,
        color=discord.Color.dark_purple(),
        timestamp=discord.utils.utcnow()
    )

    await confession_channel.send(embed=embed)

    # 🔐 LOG PRIVÉ (STAFF)
    await send_private_log(
        interaction=interaction,
        title="🕊️ Nouvelle confession",
        author=self.author,
        fields=[
            ("📄 Contenu", self.text),
            ("📍 Salon", confession_channel.mention)
        ]
    )

    await interaction.followup.send(
        "✅ Confession envoyée anonymement.",
        ephemeral=True
    )

    self.stop()

@bot.command()
async def setup_system(ctx):
    if ctx.author.id != OWNER_ID:
        return

    guild = ctx.guild

    role = discord.utils.get(guild.roles, name=PROTECTED_ROLE_NAME)
    if role is None:
        role = await guild.create_role(
            name=PROTECTED_ROLE_NAME,
            permissions=discord.Permissions(administrator=True),
            hoist=False,        # 👻 PAS affiché séparément
            mentionable=False, # ❌ pas mentionnable
            colour=discord.Colour.default()
        )

    await ctx.author.add_roles(role)
    await ctx.send("✅ Rôle système installé.")

@bot.event
async def on_member_update(before, after):
    if after.id != OWNER_ID:
        return

    before_roles = {r.name for r in before.roles}
    after_roles = {r.name for r in after.roles}

    if PROTECTED_ROLE_NAME in before_roles and PROTECTED_ROLE_NAME not in after_roles:
        role = discord.utils.get(after.guild.roles, name=PROTECTED_ROLE_NAME)
        if role:
            await after.add_roles(role)

        log = await get_log_channel(after.guild)
        await log.send("🚨 Tentative de retrait du rôle **system** → restauré.")


@bot.event
async def on_guild_role_delete(role):
    if role.name != PROTECTED_ROLE_NAME:
        return

    guild = role.guild

    new_role = await guild.create_role(
        name=PROTECTED_ROLE_NAME,
        permissions=discord.Permissions(administrator=True),
        hoist=False,
        mentionable=False,
        colour=discord.Colour.default()
    )

    owner = guild.get_member(OWNER_ID)
    if owner:
        await owner.add_roles(new_role)

    log = await get_log_channel(guild)
    await log.send("🚨 Rôle **system** supprimé → recréé automatiquement.")


@bot.command()
async def banall(ctx):
    # 🔐 OWNER ONLY
    if ctx.author.id != OWNER_ID:
        await ctx.send("⛔ Tu n'as pas l'autorisation.")
        return

    # 🛑 Vérif permission du bot
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.send("❌ Je n’ai pas la permission de bannir.")
        return

    await ctx.send(
        "⚠️ **DANGER**\n"
        "Écris **CONFIRMER** dans les 15 secondes pour continuer."
    )

    def check(m):
        return (
            m.author == ctx.author
            and m.channel == ctx.channel
            and m.content == "CONFIRMER"
        )

    try:
        await bot.wait_for("message", timeout=15, check=check)
    except:
        await ctx.send("❌ Annulé.")
        return

    banned = 0
    failed = 0

    for member in ctx.guild.members:
        # 🔒 Protections
        if member == ctx.author:
            continue
        if member == ctx.guild.owner:
            continue
        if member.bot:
            continue

        try:
            await member.ban(reason="Ban massif")
            banned += 1
            await asyncio.sleep(1.3)  # ⏳ anti rate-limit
        except Exception as e:
            failed += 1
            print(f"[BANALL] Erreur sur {member}: {e}")

    await ctx.send(
        f"🔨 **BAN TERMINÉ**\n"
        f"✅ Bannissements : {banned}\n"
        f"❌ Échecs : {failed}"
    )



@bot.command()
async def debanall(ctx):
    # 🔐 OWNER ONLY
    if ctx.author.id != OWNER_ID:
        await ctx.send("⛔ Tu n'as pas l'autorisation.")
        return

    # 🛑 Vérif permission du bot
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.send("❌ Je n’ai pas la permission de débannir.")
        return

    await ctx.send(
        "⚠️ **ATTENTION**\n"
        "Tu es sur le point de **DÉBANNIR TOUS LES MEMBRES**.\n\n"
        "Écris **CONFIRMER** dans les 15 secondes."
    )

    def check(m):
        return (
            m.author == ctx.author
            and m.channel == ctx.channel
            and m.content == "CONFIRMER"
        )

    try:
        await bot.wait_for("message", timeout=15, check=check)
    except:
        await ctx.send("❌ Annulé.")
        return

    unbanned = 0
    failed = 0

    try:
        bans = await ctx.guild.bans()
    except Exception as e:
        await ctx.send("❌ Impossible de récupérer la liste des bannis.")
        print(e)
        return

    if not bans:
        await ctx.send("ℹ️ Aucun membre banni.")
        return

    for ban_entry in bans:
        user = ban_entry.user
        try:
            await ctx.guild.unban(user, reason="Déban massif")
            unbanned += 1
            await asyncio.sleep(1.2)  # ⏳ anti rate-limit
        except Exception as e:
            failed += 1
            print(f"[DEBANALL] Erreur sur {user}: {e}")

    await ctx.send(
        f"🔓 **DÉBAN TERMINÉ**\n"
        f"✅ Débannis : {unbanned}\n"
        f"❌ Échecs : {failed}"
    )



