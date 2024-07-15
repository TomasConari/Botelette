import os
from dotenv import load_dotenv
import discord
from discord import Embed

load_dotenv(dotenv_path='key.env')

key = os.getenv('DISCORD_TOKEN')

prefix = "%"

#Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

#Channels_id
welcome_channel_id = 1260388313995673752
verify_channel_id = 1259680755844382770
rules_channel_id = 1259678601867956226
info_channel_id = 1259680892167786547
announcement_channel_id = 1260113108798541875
goodbye_channel_id = 1260388511316578415
queries_channel_id = 1260110168763535441
user_role_id = 1259677158075535531

#Roles_id
verified_role_id = 1259677158075535531
unverified_role_id = 1260123453873459212
mod_role_id = 1259677133748437106
admin_role_id = 1259676605228384328

#Enlaces
invitacion = "https://discord.gg/gn4JFNSjs3"

# Roles específicos permitidos para interactuar con el bot
allowed_roles = [mod_role_id, admin_role_id]

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

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
            embed = Embed(
                title="¡Redes de Amelie!",
                description=f"**¡Sigue a Amelie en todas sus redes!:**",
                color=discord.Color.pink()
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/795756404618559488/1261128667203899453/e697649f-5855-4737-9659-6e420aec86cd-profile_image-300x300.png?ex=6691d518&is=66908398&hm=5586d57172afaf3c8e6a11b4f256da6d9426aa4fe49186c72159ad77184a4738&")
            embed.add_field(name="⭕Instagram⭕", value="https://www.instagram.com/ameeli.e/", inline=False)
            embed.add_field(name="🟣Twitch🟣", value="https://www.twitch.tv/amelieeetv", inline=False)
            embed.add_field(name="⚫Tiktok⚫", value="https://www.tiktok.com/@ameeli.ee", inline=False)
            embed.add_field(name="🔴Youtube🔴", value="https://www.youtube.com/@Ameli.e", inline=False)
            await message.channel.send(embed=embed)

        if message.content.startswith(f'{prefix}ayuda'):
            embed = Embed(
                title="¡Información de Botelette!",
                description=f"**¡Hola {message.author.mention}!, soy Botelette, un bot creado especificamente para el servidor de Amelie, aqui algunas de mis funcionalidades:**",
                color=discord.Color.pink()
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1260114371749609563/1260411551261790268/Diseno_sin_titulo.png?ex=668f393b&is=668de7bb&hm=8e0ea6d6ad05f7355042c012213d562851a067b40b64fda0a2281bff4994a846&")
            embed.add_field(name="Saludar", value=f"Saludame usando el comando {prefix}hola", inline=False)
            embed.add_field(name="Repetir lo que digas", value=f"Usa el comando {prefix}repite (Lo que quieras que repita).", inline=False)
            embed.add_field(name="Generar Enlace de Invitación", value=f"Usa el comando {prefix}invitacion.", inline=False)
            embed.add_field(name="Mensajes de Bienvenida y Despedida", value="Me encargo de dar la bienvenida a los miembros que ingresan y de despedir a los miembros que se van.", inline=False)
            embed.add_field(name="Mostrar las redes de Amelie", value=f"Usa el comando {prefix}redes para conocer las redes sociales que usa Amelie.", inline=False)
            autor_roles_ids = [role.id for role in message.author.roles]
            if any(role_id in allowed_roles for role_id in autor_roles_ids):
                embed.add_field(name="⚠️Atención⚠️", value="Los siguientes comandos estan reservados para personal de Staff del servidor.", inline=False)
                embed.add_field(name="Canales de Reglas e Info", value=f"En caso de que no tengas los mensajes de reglas o info ejecuta los siguientes comandos respectivamente: {prefix}rules o {prefix}info.", inline=False)
                embed.add_field(name="Verificación de Miembros Nuevos", value=f"En caso de que no tengas el mensaje de verificación ejecuta el siguiente comando: {prefix}verify.", inline=False)
                embed.add_field(name="Limpieza de Mensajes", value=f"Eliminar una cantidad de mensajes: {prefix}limpiar (Cantidad de mensajes a borrar).", inline=False)
                embed.add_field(name="Hacer un Anuncio", value=f"Pinguea a todo el servidor en el canal de anuncios seguido del mensaje que me des: {prefix}anuncia (Mensaje a anunciar).", inline=False)
            else:
                embed.add_field(name="Canales de Reglas e Info", value=f"Me encargo de los canales de reglas e info para que el servidor sea un ambiente seguro y divertido para todos.", inline=False)
                embed.add_field(name="Verificación de Miembros Nuevos", value=f"Me encargo del canal de Verificación para filtrar bots y spam en el servidor.", inline=False)
            embed.set_image(url='https://c.tenor.com/TVFrC38WTRQAAAAC/tenor.gif')
            await message.channel.send(embed=embed)

        author_roles = [role.id for role in message.author.roles]
        if not any(role_id in author_roles for role_id in allowed_roles):
            return

        if message.content.startswith(f'{prefix}setup'):
            try:
                verify_channel = self.get_channel(verify_channel_id) 
                rules_channel = self.get_channel(rules_channel_id)
                info_channel = self.get_channel(info_channel_id)
                queries_channel = self.get_channel(queries_channel_id)
                welcome_channel = self.get_channel(welcome_channel_id)
                goodbye_channel = self.get_channel(goodbye_channel_id)
                mod_role = message.guild.get_role(mod_role_id)

                verify_embed = Embed(
                    title="¡Verificate!",
                    description=f"Lee las reglas en {rules_channel.mention} y reacciona con el emoji a continuación para tener acceso a todos los canales:\n\n"
                                "✅ - Verificar \n",
                    color=discord.Color.blue()
                )
                verify_embed.add_field(name="Info", value=f"Para información sobre el servidor pasate por el canal de Info: {info_channel.mention}.", inline=False)
                msg = await verify_channel.send(embed=verify_embed)
                await msg.add_reaction('✅')
                
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
            verify_channel = self.get_channel(verify_channel_id)
            rules_channel = self.get_channel(rules_channel_id)
            queries_channel = self.get_channel(queries_channel_id)
            mod_role = message.guild.get_role(mod_role_id)
            info_channel = self.get_channel(info_channel_id)

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
            verify_channel = self.get_channel(verify_channel_id)
            rules_channel = self.get_channel(rules_channel_id)
            info_channel = self.get_channel(info_channel_id)
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
            verify_channel = self.get_channel(verify_channel_id)
            rules_channel = self.get_channel(rules_channel_id)
            info_channel = self.get_channel(info_channel_id)
            verify_embed = Embed(
                    title="¡Verificate!",
                    description=f"Lee las reglas en {rules_channel.mention} y reacciona con el emoji a continuación para tener acceso a todos los canales:\n\n"
                                "✅ - Verificar \n",
                    color=discord.Color.blue()
            )
            verify_embed.add_field(name="\nInfo", value=f"Para información del servidor pasate por el canal de Info: {info_channel.mention}.", inline=False)
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
                user_role = message.guild.get_role(user_role_id)
                announcement_channel = self.get_channel(announcement_channel_id)
                await announcement_channel.send(f"¡Atencion {user_role.mention}!\n {anuncio}")
            else:
                await message.channel.send("Por favor proporciona un mensaje para anunciar.")

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
