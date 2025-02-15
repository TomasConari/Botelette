import os
from dotenv import load_dotenv
import discord
from discord import Embed
from discord.ui import Button, View
from datetime import datetime
from src.embeds import crear_embed_redes, crear_embed_ayuda, crear_embed_verify, crear_embed_rules, crear_info_embed, crear_ticket_embed
from src.ids import id_canales, id_roles, guild_id

load_dotenv(dotenv_path='key.env')

key = os.getenv('DISCORD_TOKEN')

prefix = "%"

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

# Enlaces
link_invitacion = "https://discord.gg/gn4JFNSjs3"

# Roles específicos permitidos para interactuar con el bot
allowed_roles = [id_roles["mod_role_id"], id_roles["admin_role_id"]]

class TicketView(View):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @discord.ui.button(label="Crear Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = self.bot.get_guild(guild_id)
        member = interaction.user

        timestamp = datetime.now().strftime("%d\u2044%m\u2044%Y-%H\u2236%M")

        # Crear un nuevo canal para el ticket
        category = discord.utils.get(guild.categories, id=id_canales["ticket_category_id"])
        if not category:
            await print("La categoría de tickets no está configurada correctamente.", ephemeral=True)
            return

        ticket_channel = await guild.create_text_channel(
            f'{member.name}-{timestamp}',
            category=category
        )

        # Configurar los permisos del canal
        await ticket_channel.set_permissions(member, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(guild.default_role, read_messages=False)

        # Enviar un mensaje de bienvenida en el canal del ticket
        await ticket_channel.send(f'Hola {member.mention}, Escribe un breve resumen de tu problema. Un miembro del Staff se pondrá en contacto contigo pronto.')

        # Actualiza el mensaje para que use la nueva vista
        await interaction.response.send_message(f'Tu ticket ha sido creado: {ticket_channel.mention}', ephemeral=True)

class MyClient(discord.Client):
    
    verify_channel = None
    rules_channel = None
    info_channel = None
    announcement_channel = None
    event_channel = None
    queries_channel = None
    welcome_channel = None
    goodbye_channel = None
    ticket_channel = None
    mod_channel = None
    guild = None
    verified_role = None
    unverified_role = None
    mod_role = None
    admin_role = None
    event_message_id = None

    async def on_ready(self):
        self.verify_channel = self.get_channel(id_canales["verify_channel_id"])
        self.rules_channel = self.get_channel(id_canales["rules_channel_id"])
        self.info_channel = self.get_channel(id_canales["info_channel_id"])
        self.announcement_channel = self.get_channel(id_canales["announcement_channel_id"])
        self.queries_channel = self.get_channel(id_canales["queries_channel_id"])
        self.welcome_channel = self.get_channel(id_canales["welcome_channel_id"])
        self.goodbye_channel = self.get_channel(id_canales["goodbye_channel_id"])
        self.event_channel = self.get_channel(id_canales["event_channel_id"])
        self.ticket_channel = self.get_channel(id_canales["ticket_channel_id"])
        self.mod_channel = self.get_channel(id_canales["mod_channel_id"])
        self.guild = self.get_guild(guild_id)
        self.verified_role = self.guild.get_role(id_roles["verified_role_id"])
        self.unverified_role = self.guild.get_role(id_roles["unverified_role_id"])
        self.mod_role = self.guild.get_role(id_roles["mod_role_id"])
        self.admin_role = self.guild.get_role(id_roles["admin_role_id"])
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
    
        if message.author == self.user:
            return

        if message.content.startswith(f'{prefix}hola'):
            await message.channel.send(f'**¡Hola, {message.author.mention}!👋👋👋**')

        if message.content.startswith(f'{prefix}invitacion'):
            await message.channel.send(f"**Invitación al servidor de Amelie:** \n {link_invitacion}")

        if message.content.startswith(f'{prefix}redes'):
            embed_redes = crear_embed_redes()
            await message.channel.send(embed=embed_redes)

        if message.channel.id == id_canales["user_commands_channel_id"]:
            if message.content.startswith(f'{prefix}ayuda'):
                embed_ayuda = crear_embed_ayuda(message, prefix, allowed_roles)
                await message.channel.send(embed=embed_ayuda)
        
        author_roles = [role.id for role in message.author.roles]
        if not any(role_id in author_roles for role_id in allowed_roles):
            return
        
        if message.content.startswith(f'{prefix}limpiar'):
            try:
                await message.channel.send("Limpiando")
                num_messages = int(message.content.split(' ')[1])
                if num_messages <= 0:
                    await message.channel.send("El número de mensajes a eliminar debe ser mayor que 0.", ephemeral=True)
                    return
                deleted = await message.channel.purge(limit=num_messages + 2)
                await message.channel.send(f"Se han eliminado {len(deleted) - 1} mensajes.", delete_after=5)
            except (IndexError, ValueError):
                await message.channel.send("Error: Por favor proporciona un número válido de mensajes para eliminar.")

        if message.channel.id != id_canales["mod_commands_channel_id"]:
            return

        if message.content.startswith(f'{prefix}setup'):
            try:
                verify_embed = crear_embed_verify(self.rules_channel, self.info_channel)
                msg = await self.verify_channel.send(embed=verify_embed)
                await msg.add_reaction('✅')
                
                rules_embed = crear_embed_rules(self.mod_role, self.queries_channel, self.verify_channel, self.info_channel, self.ticket_channel)
                msg = await self.rules_channel.send(embed=rules_embed)
                
                info_embed = crear_info_embed(self.verify_channel, self.rules_channel)
                msg = await self.info_channel.send(embed=info_embed)

                view = TicketView(self)
                ticket_embed = crear_ticket_embed()
                await self.ticket_channel.send(embed=ticket_embed, view=view)
                
                await message.channel.send(
                    f"**¡Hola, {message.author.mention}! Canales Configurados por este Bot: **\n\n"
                    f"**Bienvenidas: {self.welcome_channel.mention}**\n"
                    f"**Reglas: {self.rules_channel.mention}**\n"
                    f"**Info: {self.info_channel.mention}**\n"
                    f"**Creación de Tickets: {self.ticket_channel.mention}**\n"
                    f"**Verificación: {self.verify_channel.mention}**\n"
                    f"**Despedidas: {self.goodbye_channel.mention}**\n"
                )
            except Exception as e:
                await print(f'**Ha ocurrido un error desconocido: {e}**')

        if message.content.startswith(f'{prefix}rules'):
            rules_embed = crear_embed_rules(self.mod_role, self.queries_channel, self.verify_channel, self.info_channel, self.ticket_channel)
            msg = await self.rules_channel.send(embed=rules_embed)
            await message.channel.send(f'**Reenviadas las reglas del servidor en el canal {self.rules_channel.mention}!**', ephemeral=True)

        if message.content.startswith(f'{prefix}info'):
            info_embed = crear_info_embed(self.verify_channel, self.rules_channel)
            msg = await self.info_channel.send(embed=info_embed)
            await message.channel.send(f'**Reenviada la información del servidor en el canal {self.info_channel.mention}!**', ephemeral=True)

        if message.content.startswith(f'{prefix}verify'):
            verify_embed = crear_embed_verify(self.rules_channel, self.info_channel)
            msg = await self.verify_channel.send(embed=verify_embed)
            await msg.add_reaction('✅')
            await message.channel.send(f'**Reenviado el verificador del servidor en el canal {self.verify_channel.mention}!**', ephemeral=True)
            
        if message.content.startswith(f'{prefix}tickets'):
            view = TicketView(self)
            ticket_embed = crear_ticket_embed()
            await self.ticket_channel.send(embed=ticket_embed, view=view)
            await message.channel.send(f'**Reenviado el creador de tickets en el canal {self.ticket_channel.mention}!**', ephemeral=True)
        
        if message.content.startswith(f'{prefix}anuncia'):
            anuncio = message.content[len(f'{prefix}anuncia '):].strip()
            if anuncio:
                await self.announcement_channel.send(f"¡Atencion {self.verified_role.mention}!\n {anuncio}")
            else:
                await message.channel.send("Por favor proporciona un mensaje para anunciar.", ephemeral=True)

        if message.content.startswith(f'{prefix}evento'):
            anuncio = message.content[len(f'{prefix}evento '):].strip()
            if anuncio:
                await self.event_channel.send(f"{self.verified_role.mention} ¡Evento!:\n {anuncio}")
            else:
                await message.channel.send("Por favor proporciona un mensaje para anunciar.", ephemeral=True)

    async def on_scheduled_event_create(self, event):
        event_name = event.name
        event_description = event.description
        event_start_time = event.start_time

        timestamp = int(event_start_time.timestamp())

        await self.mod_channel.send(f"Se ha creado un nuevo evento: {event_name}")
        msg = await self.event_channel.send(
            "¡Atención @here!\n"
            f"Nuevo Evento: {event_name}. \n"
            f"{event_description}.\n"
            f"Se llevará a cabo en <t:{timestamp}:R> (<t:{timestamp}:f>)"
        )
        self.event_message_id = msg.id

    async def on_guild_channel_create(self, channel):
        if isinstance(channel, discord.TextChannel) and channel.category:
            if channel.category.id == id_canales["ticket_category_id"]:
                msg = await self.mod_channel.send(f'{self.mod_role.mention}, Se ha creado un nuevo Ticket: {channel.mention}')
    
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return

        guild = self.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        if not member:
            return

        if payload.emoji.name == '✅':
            await member.add_roles(self.verified_role)
            if self.unverified_role:
                await member.remove_roles(self.unverified_role)
                print(f"Eliminado el rol {self.unverified_role.name} a {member.display_name}.")

    async def on_member_join(self, member):
        await member.add_roles(self.unverified_role)
        if self.welcome_channel and self.rules_channel and self.verify_channel:
            embed = Embed(
                title=f'¡Bienvenido al servidor, {member.name}!',
                description=f'Bienvenido a nuestro servidor, {member.mention}! Esperamos que te diviertas.',
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Reglas", value=f"Por favor, revisa el canal de reglas: {self.rules_channel.mention}.", inline=True)
            embed.add_field(name="Verificación", value=f"Para ver todos los canales, verificate en {self.verify_channel.mention}.", inline=True)
            embed.set_image(url='https://cdn.discordapp.com/attachments/795756404618559488/1260738840348594238/960_1.gif?ex=66906a0a&is=668f188a&hm=152ff227435289e3fccbe175fa9d47692d09cdd163d78568e89ceb74649d685e&')
            embed.set_footer(text=f"Ahora somos {len(member.guild.members)} miembros en el servidor.")
            await self.welcome_channel.send(embed=embed)
        else:
            print('No se encontraron todos los canales necesarios.')

    async def on_member_remove(self, member):
        if self.goodbye_channel:
            embed = Embed(
                title='Alguien ha dejado el Servidor',
                description=f'**{member.display_name} ha Abandonado {member.guild.name}**',
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_image(url='https://media1.tenor.com/m/MzGKS8oljv0AAAAC/anime-driving.gif')
            embed.add_field(name="", value=f"Estamos tristes por su partida.", inline=True)
            embed.set_footer(text=f"Ahora somos {len(member.guild.members)} miembros en el servidor.")
            await self.goodbye_channel.send(embed=embed)
        else:
            print('No se encontró el canal de despedida.')

client = MyClient(intents=intents)
client.run(key)