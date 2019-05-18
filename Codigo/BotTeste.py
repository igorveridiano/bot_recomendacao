from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from imdb import IMDb

updater = Updater(token="851095270:AAGYsUcw3zQ-iOmhPBE5A4EogpAXeBciZPA")
dispatcher = updater.dispatcher

ia = IMDb()


def start(bot, update):
    msg = "Welcome to Filmes Bot"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg
    )

    msg = "Para saber informações de um filme use filme:'nome do filme aqui' e para saber sobre filmes de um " \
          "determinado ator ou diretor use pessoa:'nome do ator ou diretor aqui' "

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg
    )


def echo(bot, update):
    msg = update.message.text

    if msg.lower().__eq__("bom dia"):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Bom dia!")

    elif msg.lower().__eq__("boa noite"):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Boa noite!")

    elif msg.lower().__eq__("boa tarde"):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Boa tarde!")

    elif msg.lower().__eq__("oi") or msg.lower().__eq__("ola") or msg.lower().__eq__("olá") or msg.lower().__eq__("hi"):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Olá, precisa de ajuda!")

    elif msg.lower().__contains__("filme:"):
        msg = msg.lower().replace('filme:', '')

        movie = ia.search_movie(msg)

        msg = 'Filmes com o nome' + ' ' + msg + ' encontrados: '
        if movie.__len__() > 1:
            teste = True
            for movies in movie:
                if teste:
                    msg = msg + movies['title']
                    teste = False
                else:
                    msg = msg + ', ' + movies['title']
        elif movie.__len__() == 1:
            msg = msg + movie[0]['title']
        elif movie.__len__() == 0:
            msg = 'Filme não encontrado'

        bot.send_message(
            chat_id=update.message.chat_id,
            text=msg)

        bot.send_message(
            chat_id=update.message.chat_id,
            text="Caso o filme que deseja esteja na lista, e deseje ver mais informações sobre o filme, use: "
                 "info:'nome do filme aqui'")

    elif msg.lower().__contains__("info:"):
        msg = msg.lower().replace('info:', '')

        movie = ia.search_movie(msg)

        movie = ia.get_movie(movie[0].getID(), info=['taglines', 'plot'])

        msg = 'Sinopse: ' + movie.get('plot')[1]

        bot.send_message(
            chat_id=update.message.chat_id,
            text=msg)

    elif msg.lower().__contains__("pessoa:"):
        msg = msg.lower().replace('pessoa:', '')

        pessoa = ia.search_person(msg)
        msg = 'Pessoas com o nome' + ' ' + msg + 'encontrados: '
        if pessoa.__len__() > 1:
            teste = True
            for pessoas in pessoa:
                if teste:
                    msg = msg + pessoas['name']
                    teste = False
                else:
                    msg = msg + ', ' + pessoas['name']
        elif pessoa.__len__() == 1:
            msg = msg + pessoa[0]['name']
        elif pessoa.__len__() == 0:
            msg = "Pessoa não encontrada"

        bot.send_message(
            chat_id=update.message.chat_id,
            text=msg)

        bot.send_message(
            chat_id=update.message.chat_id,
            text="Caso a pessoa que deseja esteja na lista, e deseje ver uma lista de filmes que ela participe, use: "
                 "lista filmes:'nome da pessoa aqui'")

    elif msg.lower().__contains__("lista filmes:"):
        msg = msg.replace('lista filmes:', '')

        msg = 'Funcionalidade pendente'

        bot.send_message(
            chat_id=update.message.chat_id,
            text=msg)


start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
