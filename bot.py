import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import os




def escape_html(message):
    return message.replace("&", "&amp;").replace("<", "&lt;")




def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi There! \nI'm the NASA Bot, I use NASA API to bring you information that NASA provides"
                              ".Currently I provide data about NASA pic of the day and Near real time Images from "
                              "Earth Polychromatic Imaging Camera (EPIC) instrument."
                              "\n send /help for more info")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Possible inputs are:'
                              '\n /Day : To see the NASA pic of the Day'
                              '\n /Mars : Realtime weather data of Mars, obtained from Insight Mars lander '
                              '\n /Natural : To see the latest natural images from NASA EPIC instrument'
                              '\n /Enhanced : To see latest available enhanced images from EPIC'
                              '\n /help : To resend this message, but y tho?'
                              '\n /info : To know more about me :)  ')


def info(update, context):
    """"Send the info of the bot"""
    update.message.reply_text(
        "I was created by : @nithin_joseph \nI was made using Python Telegram Bot wrapper and NASA API :)"
        "\n\n About EPIC API : The EPIC API provides information on the daily imagery collected by DSCOVR's "
        "'Earth Polychromatic Imaging Camera (EPIC) instrument. Uniquely positioned at the Earth-Sun Lagrange point, "
        "EPIC provides full disc imagery of the Earth and captures unique perspectives of certain astronomical events "
        "such as lunar transits using a 2048x2048 pixel CCD (Charge Coupled Device) detector coupled to a 30-cm "
        "aperture Cassegrain telescope."
        "\n\n About Insight API: NASA’s InSight Mars lander takes continuous weather measurements (temperature, wind, pressure) "
        "on the surface of Mars at Elysium Planitia, a flat, smooth plain near Mars’ equator.This API provides per-Sol summary data "
        "for each of the last seven available Sols (Martian Days). As more data from a particular Sol are downlinked from the spacecraft"
        " (sometimes several days later), these values are recalculated, and consequently may change as more data are received on Earth.")




def day(update, context):
    """"Sent pic of the day"""
    #API Call
    id = update.message.chat_id
    api_key = os.environ.get("API_KEY","")
    url = 'https://api.nasa.gov/planetary/apod?api_key={}'.format(api_key)
    res = requests.get(url)
    data = res.json()


    #Assigning_data
    media = data['media_type']
    if media == 'image':
        hdurl= data['hdurl']
    else:
        pass
    date = data['date']
    explanation = data['explanation']
    pic_url = data['url']
    title = data['title']

    #Replying
    context.bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
    context.bot.send_photo(chat_id=str(id), photo =str(pic_url),caption=
                           f"\n<b>Pic of the day :  </b><code>{escape_html(date)}</code>",
                           parse_mode="HTML")                       
    update.message.reply_text(
                            f"\n<b>{escape_html(title)}</b>"
                            f"\n\n{escape_html(explanation)}",
                            parse_mode="HTML")

    if media == 'image': 
        update.message.reply_document(hdurl) 
    elif media == 'Gif' :
        update.message.reply_document(pic_url)
    else:
        update.message.reply_text(pic_url)



def natural(update, context):
    """Sent latest natural pic from EPIC"""
    chat_id = update.message.chat_id
    api_key = os.environ.get("API_KEY","")
    
    #API_CALL
    url = 'https://api.nasa.gov/EPIC/api/natural?api_key={}'.format(api_key)
    res = requests.get(url)
    data = res.json()
    x=len(data)

    #assigning_variables_and_adding_data_to_them
    latitude = []
    longitude = []
    pic_id = []
    date = []
    for value in data:
        id = value['identifier']
        pic_id.append(id)
        coord = value['centroid_coordinates']
        lat = coord['lat']
        latitude.append(lat)
        lon = coord['lon']
        longitude.append(lon)
        date_time = value['date']
        date_time = date_time.split()
        date_time =date_time[0]
        date_time = date_time.replace("-", "/")
        date_time = str(date_time)
        date.append(date_time)
    update.message.reply_text("Date of capture :" + str(date[1]))
    r = 0
    while r < x :
        try:
            pic_url = 'https://epic.gsfc.nasa.gov/archive/natural/{}/png/epic_1b_{}.png'.format(date[r],pic_id[r])
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            context.bot.send_photo(chat_id=str(chat_id), photo =str(pic_url),caption ="Latitude :" + str(latitude[r]) +", Longitude :" + str(longitude[r]))
            r = r+1
        except:
            update.message.reply_text('Data missing')
            r = r + 1
            pass
    update.message.reply_text('Done')




def enhanced(update, context):
    """Sent latest natural pic from EPIC"""
    chat_id = update.message.chat_id
    api_key = os.environ.get("API_KEY","")

    # API_CALL
    url = 'https://api.nasa.gov/EPIC/api/enhanced?api_key={}'.format(api_key)
    res = requests.get(url)
    data = res.json()
    x=len(data)

    # assigning_variables_and_adding_data_to_them
    latitude = []
    longitude = []
    pic_id = []
    date = []
    for value in data:
        id = value['identifier']
        pic_id.append(id)
        coord = value['centroid_coordinates']
        lat = coord['lat']
        latitude.append(lat)
        lon = coord['lon']
        longitude.append(lon)
        date_time = value['date']
        date_time = date_time.split()
        date_time = date_time[0]
        date_time = date_time.replace("-", "/")
        date_time = str(date_time)
        date.append(date_time)
    update.message.reply_text("Date of capture :" + str(date[1]))
    r = 0
    while r < x:
        try:
            pic_url = 'https://epic.gsfc.nasa.gov/archive/enhanced/{}/png/epic_RGB_{}.png'.format(date[r], pic_id[r])
            context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            context.bot.send_photo(chat_id=str(chat_id), photo=str(pic_url),
                                  caption="Latitude :" + str(latitude[r]) + ", Longitude :" + str(longitude[r]))
            r = r + 1
        except:
            update.message.reply_text('Data missing')
            r = r + 1
            pass
    update.message.reply_text('Done')



def mars(update, context):
    
    """Weather data from Mars using insight API"""
    
    degree_sign = u'\N{DEGREE SIGN}'
    api_key = os.environ.get("API_KEY","")
    url = 'https://api.nasa.gov/insight_weather/?api_key={}&feedtype=json&ver=1.0'.format(api_key)
    res = requests.get(url)
    data = res.json()
    n = 0
    x = data['sol_keys']
    x = len(x)
    while n < x :
        try:
            sols = data['sol_keys'][n]
            temperature = data[sols]['AT']['av']
            min_temp = round(data[sols]['AT']['mn'])
            max_temp = round(data[sols]['AT']['mx'])
            Avg_wind = round(data[sols]['HWS']['av'],2)
            min_wind = round(data[sols]['HWS']['mn'])
            max_wind = round(data[sols]['HWS']['mx'])
            Avg_pressure = round(data[sols]['PRE']['av'],2)
            min_pressure = round(data[sols]['PRE']['mn'])
            max_pressure = round(data[sols]['PRE']['mx'])
            season =data[sols]['Season']
            season = season.capitalize()
            date = data[sols]['First_UTC']
            date = date.split('T',2)
            date = date[0]
            wind_direction = data[sols]['WD']['most_common']['compass_point'] 
            n=n+1
            update.message.reply_text(
                            f"<b>Sol {sols}</b>"
                            f"\n\n<b>Date:</b> <code>{date}</code>"
                            f"\n<b>Season:</b> <b>{season}</b>"
                            f"\n<b>Temprature(Avg.)</b>                  <code>{temperature}{degree_sign}C</code>"
                            f"\n<b>Temp(Min/Max)</b>                    <code>({min_temp}/{max_temp}{degree_sign}C)</code>"  
                            f"\n<b>Wind speed(Avg.)</b>                   <code>{Avg_wind} m/s</code>"
                            f"\n<b>Wind speed(Min/Max)</b>           <code>({min_wind}-{max_wind} m/s)</code>"
                            f"\n<b>Wind Direction</b>                         <code>{wind_direction}</code>"
                            f"\n<b>Pressure(Min/Max)</b>                <code>({min_pressure}/{max_pressure}Pa)</code>"
                            f"\n<b>Atmospheric Pressure(Avg.)</b>   <code>{Avg_pressure}Pa</code>" ,
                            parse_mode="HTML"
                                    )
        except:
            n=n+1
            update.message.reply_text('Incomplete data ')
            pass




def main():
    """Start the bot."""
    bot_token = os.environ.get("BOT_TOKEN","")
    updater = Updater( bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("day", day))
    dp.add_handler(CommandHandler("natural", natural))
    dp.add_handler(CommandHandler("enhanced", enhanced))
    dp.add_handler(CommandHandler("mars", mars))

    # Start the Bot
    updater.start_polling()

    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
