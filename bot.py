import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



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
        "aperture Cassegrain telescope.")




def day(update, context):
    """"Sent pic of the day"""
    #API Call
    id = update.message.chat_id
    url = 'https://api.nasa.gov/planetary/apod?api_key=NWGysqqeDHfscBLCaoN0u8cEYkax4bT0SiHoc3dd'
    res = requests.get(url)
    data = res.json()


    #Assigning_data
    date = data['date']
    explanation = data['explanation']
    hdurl= data['hdurl']
    title = data['title']

    #Replying
    context.bot.send_photo(chat_id=str(id), photo =str(hdurl),caption=
                           f"\n<b>Pic of the day :  </b><code>{escape_html(date)}</code>",
                           parse_mode="HTML")
    update.message.reply_text(
                           f"\n<b>{escape_html(title)}</b>"
                           f"\n\n{escape_html(explanation)}",
                           parse_mode="HTML")
    update.message.reply_document(str(hdurl))




def natural(update, context):
    """Sent latest natural pic from EPIC"""
    chat_id = update.message.chat_id
    
    #API_CALL
    url = 'https://api.nasa.gov/EPIC/api/natural?api_key=NWGysqqeDHfscBLCaoN0u8cEYkax4bT0SiHoc3dd'
    res = requests.get(url)
    data = res.json()

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
    while r < 21 :

        pic_url = 'https://epic.gsfc.nasa.gov/archive/natural/{}/png/epic_1b_{}.png'.format(date[r],pic_id[r])
        context.bot.send_photo(chat_id=str(chat_id), photo =str(pic_url),caption ="Latitude :" + str(latitude[r]) +", Longitude :" + str(longitude[r]))
        r = r+1


def enhanced(update, context):
    """Sent latest natural pic from EPIC"""
    chat_id = update.message.chat_id

    # API_CALL
    url = 'https://api.nasa.gov/EPIC/api/enhanced?api_key=NWGysqqeDHfscBLCaoN0u8cEYkax4bT0SiHoc3dd'
    res = requests.get(url)
    data = res.json()

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
    while r < 21:
        pic_url = 'https://epic.gsfc.nasa.gov/archive/enhanced/{}/png/epic_RGB_{}.png'.format(date[r], pic_id[r])
        context.bot.send_photo(chat_id=str(chat_id), photo=str(pic_url),
                               caption="Latitude :" + str(latitude[r]) + ", Longitude :" + str(longitude[r]))
        r = r + 1






def main():
    """Start the bot."""

    updater = Updater("1273635811:AAGCBdt8Ce_7UNuTaaTLFAEzNRDJHkzzuy8", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("day", day))
    dp.add_handler(CommandHandler("natural", natural))
    dp.add_handler(CommandHandler("enhanced", enhanced))

    # Start the Bot
    updater.start_polling()

    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
