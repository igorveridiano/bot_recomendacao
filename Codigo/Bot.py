from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
from imdb import IMDb
from Codigo.Recommend import recommend

imdb = IMDb()

list_movies = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

RECOMENDER, APLY_RECOMMENDER, NOT_FOUND_MOVIE = range(3)


def start(bot, update):
    update.message.reply_text(
        'Oi! Sou um bot de recomendação de filmes. Para ter uma recomendação use /movie. '
        'Envie /cancel para parar de falar comigo.\n\n',
    )


def movie(bot, update):
    update.message.reply_text(
        'Me conte um nome de filme que goste, para que possa ter uma base do que recomendar para você',
    )

    return RECOMENDER


def recomender(bot, update):
    movies = imdb.search_movie(update.message.text)
    x = 1
    if movies.__len__() > 0:
        for movie_aux1 in movies:
            list_movies.update({x: movie_aux1['title']})
            x += 1
    elif movies.__len__() == 0:
        return NOT_FOUND_MOVIE
    user = update.message.from_user
    logger.info("Movie de %s: %s", user.first_name, update.message.text)
    message = 'Escolha o numero do filme correto que me contou, de acordo com os que são mostrados ' + '\n\n'
    if list_movies.__len__() > 0:
        for y in range(1, list_movies.__len__() + 1):
            message += str(y) + '-' + list_movies[y] + '\n'
        update.message.reply_text(message)
    elif list_movies.__len__() == 0:
        return NOT_FOUND_MOVIE

    return APLY_RECOMMENDER


def aply_recommender(bot, update):
    user = update.message.from_user
    movie_title = imdb.search_movie(list_movies[int(update.message.text)])
    recommend_list = recommend(movie_title[0])
    update.message.text = ''
    x = 0
    for movies in recommend_list:
        if x == 0:
            update.message.text = update.message.text + movies
            x += 1
        else:
            update.message.text = ', ' + update.message.text + movies
    logger.info("Lista de Recomendação de %s: %s", user.first_name, update.message.text)
    update.message.text = ''
    for movies in recommend_list:
        update.message.text = update.message.text + movies + '\n\n'
    update.message.reply_text('Aguarde enquanto nosso sistema faz uma recomendação para você: \n\n' +
                              update.message.text + '\n\n'
                              + 'Obrigado por usar meus serviços! Espero poder ajuda-lo outra hora.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("Usuario %s cancelo a recomendação.", user.first_name)
    update.message.reply_text('Certo, obrigado por usar meus serviços, até outra hora',
                              )

    return ConversationHandler.END


def not_found_movie(bot, update):
    user = update.message.from_user
    logger.info("Filme procurado pelo usuario %s não foi encontrado.", user.first_name)
    update.message.reply_text('O filme que está buscando não está em nossa base, sentimos muito por isso!',
                              )

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" causo um erro "%s"', update, error)

    return ConversationHandler.END


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("851095270:AAGYsUcw3zQ-iOmhPBE5A4EogpAXeBciZPA")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('movie', movie)],

        states={

            RECOMENDER: [MessageHandler(Filters.text, recomender)],

            APLY_RECOMMENDER: [MessageHandler(Filters.text, aply_recommender)],

            NOT_FOUND_MOVIE: [MessageHandler(Filters.text, not_found_movie)]

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
