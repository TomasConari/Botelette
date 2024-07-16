from discord import Embed
import discord

def crear_embed_redes():
    embed_redes = Embed(
        title="¡Redes de Amelie!",
        description=f"**¡Sigue a Amelie en todas sus redes!:**",
        color=discord.Color.pink()
    )
    embed_redes.set_thumbnail(url="https://cdn.discordapp.com/attachments/795756404618559488/1261128667203899453/e697649f-5855-4737-9659-6e420aec86cd-profile_image-300x300.png?ex=6691d518&is=66908398&hm=5586d57172afaf3c8e6a11b4f256da6d9426aa4fe49186c72159ad77184a4738&")
    embed_redes.add_field(name="⭕Instagram⭕", value="https://www.instagram.com/ameeli.e/", inline=False)
    embed_redes.add_field(name="🟣Twitch🟣", value="https://www.twitch.tv/amelieeetv", inline=False)
    embed_redes.add_field(name="⚫Tiktok⚫", value="https://www.tiktok.com/@ameeli.ee", inline=False)
    embed_redes.add_field(name="🔴Youtube🔴", value="https://www.youtube.com/@Ameli.e", inline=False)

    return embed_redes

def crear_embed_ayuda(func_message, func_prefix, func_allowed_roles):
    embed_ayuda = Embed(
        title="¡Información de Botelette!",
        description=f"**¡Hola {func_message.author.mention}!, soy Botelette, un bot creado especificamente para el servidor de Amelie, aqui algunas de mis funcionalidades:**",
        color=discord.Color.pink()
    )
    embed_ayuda.set_thumbnail(url="https://cdn.discordapp.com/attachments/1260114371749609563/1260411551261790268/Diseno_sin_titulo.png?ex=668f393b&is=668de7bb&hm=8e0ea6d6ad05f7355042c012213d562851a067b40b64fda0a2281bff4994a846&")
    embed_ayuda.add_field(name="Saludar", value=f"Saludame usando el comando {func_prefix}hola", inline=False)
    embed_ayuda.add_field(name="Repetir lo que digas", value=f"Usa el comando {func_prefix}repite (Lo que quieras que repita).", inline=False)
    embed_ayuda.add_field(name="Generar Enlace de Invitación", value=f"Usa el comando {func_prefix}invitacion.", inline=False)
    embed_ayuda.add_field(name="Mensajes de Bienvenida y Despedida", value="Me encargo de dar la bienvenida a los miembros que ingresan y de despedir a los miembros que se van.", inline=False)
    embed_ayuda.add_field(name="Mostrar las redes de Amelie", value=f"Usa el comando {func_prefix}redes para conocer las redes sociales que usa Amelie.", inline=False)
    autor_roles_ids = [role.id for role in func_message.author.roles]
    if any(role_id in func_allowed_roles for role_id in autor_roles_ids):
        embed_ayuda.add_field(name="⚠️Atención⚠️", value="Los siguientes comandos estan reservados para personal de Staff del servidor.", inline=False)
        embed_ayuda.add_field(name="Canales de Reglas e Info", value=f"En caso de que no tengas los mensajes de reglas o info ejecuta los siguientes comandos respectivamente: {func_prefix}rules o {func_prefix}info.", inline=False)
        embed_ayuda.add_field(name="Verificación de Miembros Nuevos", value=f"En caso de que no tengas el mensaje de verificación ejecuta el siguiente comando: {func_prefix}verify.", inline=False)
        embed_ayuda.add_field(name="Limpieza de Mensajes", value=f"Eliminar una cantidad de mensajes: {func_prefix}limpiar (Cantidad de mensajes a borrar).", inline=False)
        embed_ayuda.add_field(name="Hacer un Anuncio", value=f"Pinguea a todo el servidor en el canal de anuncios seguido del mensaje que me des: {func_prefix}anuncia (Mensaje a anunciar).", inline=False)
    else:
        embed_ayuda.add_field(name="Canales de Reglas e Info", value=f"Me encargo de los canales de reglas e info para que el servidor sea un ambiente seguro y divertido para todos.", inline=False)
        embed_ayuda.add_field(name="Verificación de Miembros Nuevos", value=f"Me encargo del canal de Verificación para filtrar bots y spam en el servidor.", inline=False)
    embed_ayuda.set_image(url='https://c.tenor.com/TVFrC38WTRQAAAAC/tenor.gif')
    return embed_ayuda

def crear_embed_verify(func_rules_channel, func_info_channel):
    verify_embed = Embed(
        title="¡Verificate!",
        description=f"Lee las reglas en {func_rules_channel.mention} y reacciona con el emoji a continuación para tener acceso a todos los canales:\n\n"
                    "✅ - Verificar \n",
        color=discord.Color.blue()
    )
    verify_embed.add_field(name="Info", value=f"Para información sobre el servidor pasate por el canal de Info: {func_info_channel.mention}.", inline=False)
    return verify_embed

def crear_embed_rules(func_mod_role, func_queries_channel, func_verify_channel, func_info_channel):
    rules_embed = Embed(
        title="¡Reglas!",
        description=
            f"\n\n**-No insultar o pelearse dentro del servidor.**\n\n"
            "**-No escribir por privado a otro miembro, a menos que sea CON SU PERMISO.**\n\n"
            "**-No realizar amenazas hacia terceros y/o uno mismo (auto lesiones).**\n\n"
            "**-No discriminar, TODOS SOMOS IGUALES UwU.**\n\n"
            "**-No pinguear o arrobar a Amelie.**\n\n"
            f"**-Arrobar al personal de staff: {func_mod_role.mention} para pedir ayuda.**\n\n"
            f"**-Si se tiene una duda o queja, escribirlo en el canal {func_queries_channel.mention}.**\n\n"
            "**-Trata a todo el mundo con respeto. No se tolerará ningún tipo de acoso, caza de brujas, sexismo, racismo o discurso de odio.**\n\n"
            "**-No se permite el spam ni la autopromoción (invitaciones al servidor, anuncios, etc.) sin permiso de un miembro del personal. Esto también incluye mandar MD a otros miembros.**\n\n"
            "**-No se permite contenido con restricción por edad ni obsceno. Esto incluye texto, imágenes o enlaces que presenten desnudos, violencia u otro tipo de contenido gráfico que pueda herir la sensibilidad del espectador.**\n\n"
            "**-Si ves algo que va en contra de las normas o que no te haga sentir seguro, informa al personal.**\n\n\n\n"
            "**⚠️ Si se incumple alguna de las reglas serás baneado automáticamente ⚠️**\n\n"
            f"**Disfruta del servidor.  No olvides verificarte: {func_verify_channel.mention}, y pasarte por el canal de info: {func_info_channel.mention}**",
        color=discord.Color.gold()
    )
    rules_embed.set_image(url="https://cdn.discordapp.com/attachments/795756404618559488/1260744829831348224/gif.gif?ex=66906f9e&is=668f1e1e&hm=1c912e3fe500c1ae5b47b29cd4218aa35f87e0b8b0cc30c0552b037b1186a950&")
    return rules_embed

def crear_info_embed(func_verify_channel, func_rules_channel):
    info_embed = Embed(
        title="¡Hola! Este es el servidor oficial de Ameli.e",
        description=
            f"**Este Servidor te ofrece lo siguiente:**\n\n\n"
            "**Te avisa cada que Amelie sube un video a Youtube o hace stream en Twitch.**\n\n"
            "**Canales para socializar con la comunidad.**\n\n"
            "**Canales de eventos para interactuar con Amelie.**\n\n"
            "**Canales para compartir dibujos, memes, clips y multimedia en general**\n\n"
            "**Aparecer en dinámicas exclusivas que hará Amelie en su canal de Youtube o Twitch.**\n\n\n\n"
            f"**Disfruta del servidor.  No olvides verificarte: {func_verify_channel.mention}, y pasarte por el canal de Reglas: {func_rules_channel.mention}**",
        color=discord.Color.green()
    )
    return info_embed