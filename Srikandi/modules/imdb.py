from imdb import IMDb
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Srikandi import app

ia = IMDb()


@app.on_message(filters.command("imdb"))
async def imdb(client, message):
    """
    .imdb <movie>
    """
    if len(message.command) > 1:
        movie = " ".join(message.command[1:])
    else:
        return await message.reply_text("<b>Please enter a movie name</b>")
    try:
        movie = ia.get_movie(ia.search_movie(movie)[0].movieID)
    except:
        return await message.edit("<b>Movie not found</b>")

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "More Info",
                    url=f"https://www.imdb.com/title/tt{movie.movieID}",
                )
            ]
        ]
    )
    _writers, _directors, _casts = [], [], []
    try:
        for _i in movie["writer"]:
            _writers.append(_i["name"])
    except:
        pass
    try:
        for _i in movie["director"]:
            _directors.append(_i["name"])
    except:
        pass
    try:
        for _i in movie["cast"]:
            _casts.append(_i["name"])
        _casts = _casts[:4] if len(_casts) >= 5 else _casts
    except:
        pass
    caption = f"<b>{movie['kind'].capitalize()}</b>\n======\n<b>\
Title:</b> <code>{movie['title']}</code>\n\
<b>Year:</b> <code>{movie['year']}</code>\n\
<b>Rating:</b> <code>{movie['rating'] if 'rating' in movie else 'Not Found'}</code>\n\
<b>Genre:</b> <code>{', '.join(movie['genres'])}</code>\n\
<b>Runtime:</b> <code>{movie['runtime'][0] if 'runtime' in movie else 'Not Found'}</code>\n\
<b>Writers:</b> <code>{', '.join(_writers)}</code>\n\
<b>Directors:</b> <code>{', '.join(_directors)}</code>\n\
<b>Actors:</b> <code>{', '.join(_casts)}</code>\n\
<b>Language:</b> <code>{movie['language'] if 'language' in movie else 'Not Found'}</code>\n\
<b>Country:</b> <code>{movie['country'] if 'country' in movie else 'Not Found'}</code>\n\
    "
    try:
        m = await message.reply_photo(
            movie["full-size cover url"],
            caption=caption,
            reply_markup=reply_markup,
        )
    except KeyError:
        m = await message.reply_photo(
            movie["cover url"], caption=caption, reply_markup=reply_markup
        )

    return await m.reply_text(
        f"<b>Plot:</b> <code>{movie['plot outline'] if 'plot outline' in movie else 'Not available'}</code>"
    )
