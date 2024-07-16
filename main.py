import os
from dotenv import load_dotenv
import discord
from discord import Embed
from src.embeds import crear_embed_redes, crear_embed_ayuda, crear_embed_verify, crear_embed_rules, crear_info_embed
from src.ids import id_canales, id_roles, guild_id

load_dotenv(dotenv_path='key.env')

key = os.getenv('DISCORD_TOKEN')

prefix = "%"

#Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

#Enlaces
invitacion = "https://discord.gg/gn4JFNSjs3"

# Roles específicos permitidos para interactuar con el bot
allowed_roles = [id_roles["mod_role_id"], id_roles["admin_role_id"]]

class MyClient(discord.Client):
    
    verify_channel = ""
    rules_channel = ""
    info_channel = ""
    announcement_channel = ""
    queries_channel = ""
    welcome_channel = ""
    goodbye_channel = ""
    guild = ""
    verified_role = ""
    unverified_role = ""
    mod_role = ""
    admin_role = ""
    
    async def on_ready(self):
        verify_channel = self.get_channel(id_canales["verify_channel_id"])
        rules_channel = self.get_channel(id_canales["rules_channel_id"])
        info_channel = self.get_channel(id_canales["info_channel_id"])
        announcement_channel = self.get_channel(id_canales["announcement_channel_id"])
        queries_channel = self.get_channel(id_canales["queries_channel_id"])
        welcome_channel = self.get_channel(id_canales["welcome_channel_id"])
        goodbye_channel = self.get_channel(id_canales["goodbye_channel_id"])
        guild = self.get_guild(guild_id)
        verified_role = guild.get_role(id_roles["verified_role_id"])
        unverified_role = guild.get_role(id_roles["unverified_role_id"])
        mod_role = guild.get_role(id_roles["mod_role_id"])
        admin_role = guild.get_role(id_roles["admin_role_id"])
        print(f'Logged on as {self.user}¡')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(f'{prefix}hola'):
            await message.channel.send(f'**¡Hola, {message.author.mention}!👋👋👋**')

        if message.content.startswith(f'{prefix}repite'):
            mensaje_a_repetir = message.content[len(f'{prefix}repite '):]
            await message.channel.send(mensaje_a_repetir)

        if message.content.startswith(f'{prefix}invitacion'):
            await message.channel.send(invitacion)

        if message.content.startswith(f'{prefix}redes'):
            embed_redes = crear_embed_redes()
            await message.channel.send(embed=embed_redes)

        if message.content.startswith(f'{prefix}ayuda'):
            embed_ayuda = crear_embed_ayuda(message, prefix, allowed_roles)
            await message.channel.send(embed=embed_ayuda)

        author_roles = [role.id for role in message.author.roles]
        if not any(role_id in author_roles for role_id in allowed_roles):
            return

        if message.content.startswith(f'{prefix}setup'):
            try:
                verify_embed = crear_embed_verify(rules_channel, info_channel)
                msg = await verify_channel.send(embed=verify_embed)
                await msg.add_reaction('✅')
                
                rules_embed = crear_embed_rules(mod_role, queries_channel, verify_channel, info_channel)
                msg = await rules_channel.send(embed=rules_embed)
                
                info_embed = crear_info_embed(verify_channel, rules_channel)
                msg = await info_channel.send(embed=info_embed)
                
                await message.channel.send(
                    f"**¡Hola, {message.author.mention}! Canales Configurados por este Bot: **\n\n"
                    f"**Bienvenidas: {welcome_channel.mention}**\n"
                    f"**Reglas: {rules_channel.mention}**\n"
                    f"**Info: {info_channel.mention}**\n"
                    f"**Verificación: {verify_channel.mention}**\n"
                    f"**Despedidas: {goodbye_channel.mention}**\n"
                )

            except Exception as e:
                await message.channel.send(f'**Ha ocurrido un error desconocido: {e}**')

        if message.content.startswith(f'{prefix}rules'):

            rules_embed = Embed(
                title="¡Reglas!",
                description=f"\n\n**-No insultar o pelearse dentro del servidor.**\n\n"
                            "**-No escribir por privado a otro miembro, a menos que sea CON SU PERMISO.**\n\n"
                            "**-No realizar amenazas hacia terceros y/o uno mismo (auto lesiones).**\n\n"
                            "**-No discriminar, TODOS SOMOS IGUALES UwU.**\n\n"
                            "**-No pinguear o arrobar a Amelie.**\n\n"
                            f"**-Arrobar al personal de staff: {mod_role.mention} para pedir ayuda.**\n\n"
                            f"**-Si se tiene una duda o queja, escribirlo en el canal {queries_channel.mention}.**\n\n"
                            "**-Trata a todo el mundo con respeto. No se tolerará ningún tipo de acoso, caza de brujas, sexismo, racismo o discurso de odio.**\n\n"
                            "**-No se permite el spam ni la autopromoción (invitaciones al servidor, anuncios, etc.) sin permiso de un miembro del personal. Esto también incluye mandar MD a otros miembros.**\n\n"
                            "**-No se permite contenido con restricción por edad ni obsceno. Esto incluye texto, imágenes o enlaces que presenten desnudos, violencia u otro tipo de contenido gráfico que pueda herir la sensibilidad del espectador.**\n\n"
                            "**-Si ves algo que va en contra de las normas o que no te haga sentir seguro, informa al personal.**\n\n\n\n"
                            "**⚠️ Si se incumple alguna de las reglas serás baneado automáticamente ⚠️**\n\n"
                            f"**Disfruta del servidor.  No olvides verificarte: {verify_channel.mention}, y pasarte por el canal de info: {info_channel.mention}**",
                color=discord.Color.gold()
            )
            rules_embed.set_image(url="https://cdn.discordapp.com/attachments/795756404618559488/1260744829831348224/gif.gif?ex=66906f9e&is=668f1e1e&hm=1c912e3fe500c1ae5b47b29cd4218aa35f87e0b8b0cc30c0552b037b1186a950&")

            msg = await rules_channel.send(embed=rules_embed)
            await message.channel.send(f'**Reenviadas las reglas del servidor en el canal {rules_channel.mention}!**')

        if message.content.startswith(f'{prefix}info'):
            info_embed = Embed(
                    title="¡Hola! Este es el servidor oficial de Ameli.e",
                    description=f"**Este Servidor te ofrece lo siguiente:**\n\n\n"
                                "**Te avisa cada que Amelie sube un video a Youtube o hace stream en Twitch.**\n\n"
                                "**Canales para socializar con la comunidad.**\n\n"
                                "**Canales de eventos para interactuar con Amelie.**\n\n"
                                "**Canales para compartir dibujos, memes, clips y multimedia en general**\n\n"
                                "**Bot Mudae para que compitas con la comunidad por coleccionar personajes de tus animes favoritos.**\n\n"
                                "**Aparecer en dinámicas exclusivas que hará Amelie en su canal de Youtube o Twitch.**\n\n\n\n"
                                f"**Disfruta del servidor.  No olvides verificarte: {verify_channel.mention}, y pasarte por el canal de Reglas: {rules_channel.mention}**",
                    color=discord.Color.green()
                )
            msg = await info_channel.send(embed=info_embed)
            await message.channel.send(f'**Reenviada la información del servidor en el canal {info_channel.mention}!**')

        if message.content.startswith(f'{prefix}verify'):
            verify_embed = crear_embed_verify(rules_channel, info_channel)
            msg = await verify_channel.send(embed=verify_embed)
            await msg.add_reaction('✅')
            await message.channel.send(f'**Reenviado el verificador del servidor en el canal {verify_channel.mention}!**')
        
        if message.content.startswith(f'{prefix}limpiar'):
            try:
                await message.channel.send("Limpiando")
                num_messages = int(message.content.split(' ')[1])
                if num_messages <= 0:
                    await message.channel.send("El número de mensajes a eliminar debe ser mayor que 0.")
                    return
                deleted = await message.channel.purge(limit=num_messages + 2)
                await message.channel.send(f"Se han eliminado {len(deleted) - 1} mensajes.", delete_after=5)
            except (IndexError, ValueError):
                await message.channel.send(message.content.split(' ')[1])
        
        if message.content.startswith(f'{prefix}anuncia'):
            anuncio = message.content[len(f'{prefix}anuncia '):].strip()
            if anuncio:
                await announcement_channel.send(f"¡Atencion {user_role.mention}!\n {anuncio}")
            else:
                await message.channel.send("Por favor proporciona un mensaje para anunciar.")

        if message.content.startswith(f'{prefix}evento'):
            print("hola")
            

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return

        guild = self.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        if not member:
            return

        if payload.emoji.name == '✅':
            verified_role = guild.get_role(verified_role_id)

            if verified_role:
                await member.add_roles(verified_role)
                print(f"Asignado el rol {verified_role.name} a {member.display_name}.")
                unverified_role = guild.get_role(unverified_role_id)
                if unverified_role:
                    await member.remove_roles(unverified_role)
                    print(f"Eliminado el rol {unverified_role.name} a {member.display_name}.")


    async def on_member_join(self, member):
        welcome_channel = member.guild.get_channel(welcome_channel_id)
        rules_channel = member.guild.get_channel(rules_channel_id)
        verify_channel = member.guild.get_channel(verify_channel_id)
        rol = member.guild.get_role(unverified_role_id)
        await member.add_roles(rol)
        
        if welcome_channel and rules_channel and verify_channel:
            embed = Embed(
                title=f'¡Bienvenido al servidor, {member.name}!',
                description=f'Bienvenido a nuestro servidor, {member.mention}! Esperamos que te diviertas.',
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Reglas", value=f"Por favor, revisa el canal de reglas: {rules_channel.mention}.", inline=True)
            embed.add_field(name="Verificación", value=f"Para ver todos los canales, verificate en {verify_channel.mention}.", inline=True)
            embed.set_image(url='https://cdn.discordapp.com/attachments/795756404618559488/1260738840348594238/960_1.gif?ex=66906a0a&is=668f188a&hm=152ff227435289e3fccbe175fa9d47692d09cdd163d78568e89ceb74649d685e&')
            embed.set_footer(text=f"Ahora somos {len(member.guild.members)} miembros en el servidor.")
            await welcome_channel.send(embed=embed)
        else:
            print('No se encontraron todos los canales necesarios.')

    async def on_member_remove(self, member):
        goodbye_channel = member.guild.get_channel(goodbye_channel_id)
        
        if goodbye_channel:
            embed = Embed(
                title='Alguien ha dejado el Servidor',
                description=f'**{member.display_name} ha Abandonado {member.guild.name}**',
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_image(url='https://media1.tenor.com/m/MzGKS8oljv0AAAAC/anime-driving.gif')
            embed.add_field(name="", value=f"Estamos tristes por su partida.", inline=True)
            embed.set_footer(text=f"Ahora somos {len(member.guild.members)} miembros en el servidor.")
            await goodbye_channel.send(embed=embed)
        else:
            print('No se encontró el canal de despedida.')

client = MyClient(intents=intents)
client.run(key)
