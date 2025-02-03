import json
import time

import requests
from flask import Flask, request
global last_update_id
from datetime import datetime, timedelta

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
INGREDIENTS = [['1', 'masalliq 1', 'ingredient 1'], ['2', 'masalliq 2', 'ingredient 2'], ['3', 'masalliq 3', 'ingredient 3'], ['4', 'masalliq 4', 'ingredient 4'], ['5', 'masalliq 5', 'ingredient 5'], ['6', 'masalliq 6', 'ingredient 6'], ['7', 'masalliq 7', 'ingredient 7'], ['8', 'masalliq 8', 'ingredient 8'], ['9', 'masalliq 9', 'ingredient 9'], ['10', 'masalliq 10', 'ingredient 10'], ['11', 'masalliq 11', 'ingredient 11'], ['12', 'masalliq 12', 'ingredient 12'], ['13', 'masalliq 13', 'ingredient 13'], ['14', 'masalliq 14', 'ingredient 14'], ['15', 'masalliq 15', 'ingredient 15'], ['16', 'masalliq 16', 'ingredient 16'], ['17', 'masalliq 17', 'ingredient 17'], ['18', 'masalliq 18', 'ingredient 18'], ['19', 'masalliq 19', 'ingredient 19'], ['20', 'masalliq 20', 'ingredient 20'], ['21', 'masalliq 21', 'ingredient 21'], ['22', 'masalliq 22', 'ingredient 22'], ['23', 'masalliq 23', 'ingredient 23'], ['24', 'masalliq 24', 'ingredient 24'], ['25', 'masalliq 25', 'ingredient 25'], ['26', 'masalliq 26', 'ingredient 26'], ['27', 'masalliq 27', 'ingredient 27'], ['28', 'masalliq 28', 'ingredient 28'], ['29', 'masalliq 29', 'ingredient 29'], ['30', 'masalliq 30', 'ingredient 30'], ['31', 'masalliq 31', 'ingredient 31'], ['32', 'masalliq 32', 'ingredient 32'], ['33', 'masalliq 33', 'ingredient 33'], ['34', 'masalliq 34', 'ingredient 34'], ['35', 'masalliq 35', 'ingredient 35'], ['36', 'masalliq 36', 'ingredient 36'], ['37', 'masalliq 37', 'ingredient 37'], ['38', 'masalliq 38', 'ingredient 38'], ['39', 'masalliq 39', 'ingredient 39'], ['40', 'masalliq 40', 'ingredient 40'], ['41', 'masalliq 41', 'ingredient 41'], ['42', 'masalliq 42', 'ingredient 42'], ['43', 'masalliq 43', 'ingredient 43'], ['44', 'masalliq 44', 'ingredient 44'], ['45', 'masalliq 45', 'ingredient 45'], ['46', 'masalliq 46', 'ingredient 46'], ['47', 'masalliq 47', 'ingredient 47'], ['48', 'masalliq 48', 'ingredient 48'], ['49', 'masalliq 49', 'ingredient 49'], ['50', 'masalliq 50', 'ingredient 50'], ['51', 'masalliq 51', 'ingredient 51'], ['52', 'masalliq 52', 'ingredient 52'], ['53', 'masalliq 53', 'ingredient 53'], ['54', 'masalliq 54', 'ingredient 54'], ['55', 'masalliq 55', 'ingredient 55'], ['56', 'masalliq 56', 'ingredient 56'], ['57', 'masalliq 57', 'ingredient 57'], ['58', 'masalliq 58', 'ingredient 58'], ['59', 'masalliq 59', 'ingredient 59'], ['60', 'masalliq 60', 'ingredient 60'], ['61', 'masalliq 61', 'ingredient 61'], ['62', 'masalliq 62', 'ingredient 62'], ['63', 'masalliq 63', 'ingredient 63'], ['64', 'masalliq 64', 'ingredient 64'], ['65', 'masalliq 65', 'ingredient 65'], ['66', 'masalliq 66', 'ingredient 66'], ['67', 'masalliq 67', 'ingredient 67'], ['68', 'masalliq 68', 'ingredient 68'], ['69', 'masalliq 69', 'ingredient 69'], ['70', 'masalliq 70', 'ingredient 70'], ['71', 'masalliq 71', 'ingredient 71'], ['72', 'masalliq 72', 'ingredient 72'], ['73', 'masalliq 73', 'ingredient 73'], ['74', 'masalliq 74', 'ingredient 74'], ['75', 'masalliq 75', 'ingredient 75'], ['76', 'masalliq 76', 'ingredient 76'], ['77', 'masalliq 77', 'ingredient 77'], ['78', 'masalliq 78', 'ingredient 78'], ['79', 'masalliq 79', 'ingredient 79'], ['80', 'masalliq 80', 'ingredient 80'], ['81', 'masalliq 81', 'ingredient 81'], ['82', 'masalliq 82', 'ingredient 82'], ['83', 'masalliq 83', 'ingredient 83'], ['84', 'masalliq 84', 'ingredient 84'], ['85', 'masalliq 85', 'ingredient 85'], ['86', 'masalliq 86', 'ingredient 86'], ['87', 'masalliq 87', 'ingredient 87'], ['88', 'masalliq 88', 'ingredient 88'], ['89', 'masalliq 89', 'ingredient 89'], ['90', 'masalliq 90', 'ingredient 90'], ['91', 'masalliq 91', 'ingredient 91'], ['92', 'masalliq 92', 'ingredient 92'], ['93', 'masalliq 93', 'ingredient 93'], ['94', 'masalliq 94', 'ingredient 94'], ['95', 'masalliq 95', 'ingredient 95'], ['96', 'masalliq 96', 'ingredient 96'], ['97', 'masalliq 97', 'ingredient 97'], ['98', 'masalliq 98', 'ingredient 98'], ['99', 'masalliq 99', 'ingredient 99'], ['100', 'masalliq 100', 'ingredient 100'], ['101', 'masalliq 101', 'ingredient 101'], ['102', 'masalliq 102', 'ingredient 102'], ['103', 'masalliq 103', 'ingredient 103'], ['104', 'masalliq 104', 'ingredient 104'], ['105', 'masalliq 105', 'ingredient 105']]
MEALS = [['1', "Osh Palov (Plov)", "English version"]]
RECIPE = [
        {
            "id": 1,
            "name": "Osh Palov (Plov)",
            "ingredients": ["1", "2", "3", "4"],
            "steps": [
                "Gurunchni yuving va 30 daqiqa suvda ivitib qo’ying.",
                "Sabzi, piyozni to’g’rang va ta’bizga qarab sarimsoq piyoz qo’shing.",
                "Qozondagi qizigan yog’ga oldindan to’g’rab olgan sabzovatlaringizni qo’shib, oltin rang tusga kirmaguncha qovuring.",
                "Idishga suv va gurunchni solib, guruch yumshoq holatga kelguncha dimlab qo’ying",
                "Tayyor bo’lgan aralashmani dasturxonga tortishdan oldiz tayyor mayizlar bilan aralashtiring."
            ],
            "type": "odatiy"
        },
        {
            "id": 2,
            "name": "Mastava",
            "ingredients": ["100", "101", "102", "102", "103", "104"],
            "steps": [
                "Guruchni yaxshilab yuving va 30 daqiqa suvda ivitib qo’ying.",
                "Sabzini, kartoshkani, piyozni va selderey barglarini to’g’rang.",
                "Go’shtni yumshoq holatga kelgunicha qaynoq suvda qaynating, keyin bo’laklarga ajrating.",
                "Qozonga to’g’ralgan sabzavotlarni, bo’laklarga bo’lingan go’shtni va gurunchni soling.",
                "Sabzavotlar yaxshi pishguncha past olovda qaynating.",
                "Dasturxonga tortishdan oldin ko’katlar bilan bezating."
            ],
            "type": "odatiy"
        },
        {
            "id": 3,
            "name": "Guruchli Veggie salatii",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Gurunchni oldin yaxshilab suvda yuvib ivitib oling.",
                "Alohida skovorodkada to'g'ralgan sabzi, piyoz va maydalangan sarimsoqni ozgina yog'da qovuring.",
                "Pishgan guruchni qovurilgan sabzavotlar bilan aralashtiring.",
                "Tayyor saladni soya yog’i bilan taqdim etsangiz bo’ladi."
            ],
            "type": "odatiy"
        },
        {
            "id": 4,
            "name": "Mevali salad",
            "ingredients": ["1", "1", "1"],
            "steps": [
                "Olma, mandarin va non bo’laklarini yaxshilab yuving va kichik bo’laklarda to’g’rang.",
                "Barcha bo’laklarni bir idishga jamlang va tayyor massani biroz muddat muzlatgichga qo’yib qo’ying."
            ],
            "type": "odatiy"
        },
        {
            "id": 5,
            "name": "Pyure",
            "ingredients": ["1", "1", "1"],
            "steps": [
                "Banan, ismaloq va bodom sutini blenderga soling.",
                "Silliq kremsi holatga kelguncha blenderda aralashtiring.",
                "Tayyor pyureni stakanlarga soling va tortiq eting."
            ],
            "type": "odatiy"
        },
        {
            "id": 6,
            "name": "Sabzavotli pechda pishirilgan tovuq",
            "ingredients": ["1", "1", "1", "1", "1", "1", "1"],
            "steps": [
                "Pechni 375°F (190°C) ga oldindan qizdiring.",
                "Katta idishda o'simlik yog'i va ziravorlar bilan tug'ralgan sabzi, kartoshka, bolgar qalampiri, piyoz va sarimsoqni aralashtiring.",
                "Sabzavotlarni pishirish varag'iga qo'ying. Yuqoridan tovuq bo'laklarini qo'shing. Tovuqni yaxshilab pishiring..",
                "Ta’bga ko’ra ziravorlarni soling.",
                "45 daqiqadan 1 soatgacha yoki tovuq pishib, sabzavotlar yumshoq bo'lguncha pishiring."
            ],
            "type": "odatiy"
        },
        {
            "id": 7,
            "name": "somsa",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Mol go'shti va piyozni mayda to'rtburchak shaklida to'g'rab, katta idishda barchasini aralashtiramiz va ziravorlar sepamiz.",
                "Tayyor xamirni oldindan eritib, 50 gramm keladigan bo'laklarga bo'lamiz. Likopchaga qo'yib ustini sochiq bilan yopamiz va 5 daqiqa tindiramiz..",
                "Har bir bo'lakni 3-4 millimetr qalinlikda yoyamiz. Xamirning o'rtasiga 1,5 osh qoshiq asos solib, somsani uch burchak shaklida tugamiz.",
                "Somsani pergament qog'ozi bilan qoplangan gaz pechi patnisiga joylashtirib, tuxum sarig'ini surtamiz va kunjut sepamiz. 180 C darajada qizdirilgan gaz pechiga 35-40 daqiqaga yuboramiz."
            ],
            "type": "odatiy"
        },
        {
            "id": 8,
            "name": "Pishloqli tovuq",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Tovuq ko'kragini pishirishdan boshlang.Pishgan tovuq go’shtini bir-biridan ajrating",
                "Kichkina skovorodkada o'simlik moyini o'rta olovda qizdiring. 5-7 daqiqa piyozni sariq tusga kirguncha qovuring.",
                "Piyoz qovurilgancha ko’katlarni yaxshilab yuvib to’g’rang.."
            ],
            "type": "odatiy"
        },
        {
            "id": 9,
            "name": "Fajita",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Un va sutdan foydalanib xamir tayyorlang va 20 minut dam bering.",
                "Tayyor xamirni bo’laklarga bo’lib, aylana tarzda yupqa yoying.",
                "Go’shtni tilimlab qizigan yog’da qovurib oling.",
                "Go’sht to’q qizil holatiga kelguncha qovuring va undan so’ng yog’ga bulg’or qalampirini qo’shing.",
                "Oldindan yoyib olingan xamirni yaxshilab qovurib oling.",
                "Qovurilgan xamir ustiga birin-ketin tayyor massani qo’ying. Ta’bizga qarab boshqa ziravorlarni yoki limon suvini qo’shsangiz bo’ladi."
            ],
            "type": "diabetic"
        },
        {
            "id": 10,
            "name": "Sho’rva",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Sabzavotlarni po’stidan ajratib, to’g’rang.",
                "Barcha maxsulotlarni qaynoq suv bilan qozonga soling.",
                "Sabzavotlar yaxshilab pishgunga qadar past olovda qaynating.",
                "Ta’bga ko’ra ziravorlar, tuz va qalampir solib tortiq eting."
            ],
            "type": "diabetic"
        },
        {
            "id": 11,
            "name": "Tovuq va ismaloqli makaron",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Mahsulot muqovasidagi ko'rsatmalarga muvofiq makaronni pishiring..",
                "Tovada o'simlik yog'ini o'rtacha olovda qizdiring. Tug'ralgan sarimsoq, piyoz va bolgar qalampirini qo'shing. Yumshoq bo'lgunga pishiring..",
                "To'g'ralgan tovuq go'shini qo'shing, ziravorlar qo'shing va qizarguncha pishiring.",
                "Tug'ralgan pomidor va ismaloq qo'shing, ismaloq so'lib, pomidor yumshoq bo'lguncha pishiring.",
                "Tayyorlangan makaronni tovuq va sabzavotlar bilan birlashtiring. Dasturxonga tortishdan avval maydalangan pishloq bilan ovqatni ustini bezating.."
            ],
            "type": "diabetic"
        },
        {
            "id": 12,
            "name": "Manti",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Suv va undan foydalnib xamir tayyorlang.",
                "Tayyor xamirni kichik bo’laklarga bo’ling.",
                "Kichik bo’lakdagi xamirlarni go’sht, piyoz va ziravorlardan tashkil topgan aralashma bilan to’ldiring.",
                "Aralashma solingan xamir bo’laklarini xuddi chuchvara kabi chekka qismlarini buklab chiqing.",
                "Tayyor maxsulotni bug’da ichidagi maxsulotlari pishguncha qoldiring.",
                "Mantini dasturxonga smetana yoki eritilgan saryog’ bilan taqdim eting."
            ],
            "type": "obese"
        },
        {
            "id": 13,
            "name": "Tovuq sho’rva",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Qozonga yog’ solib yaxshilab qiziting.",
                "Qizigan yog’ga piyozni solib oltin rang tusga kirguncha qovuring.",
                "Qovurilgan piyozga to’g’ralgan pomidor va bulg’or qalampiri bo’laklarini solib qovuring.",
                "Ulardan so’ng tovuq go’shtini solib qovurishda davom eting.",
                "Tayyor massaga to’gralgan kartoshka va sabzini solib qovuring.",
                "Qovurilgan masalliqlarning ustiga suv solib 20 minut qaynating.",
                "Qaynab chiqqan sho’rvaga moslab ziravorlar va tuz soling.",
                "Dasturxonga tortishdan oldin ko’katlar bilan bezating."
            ],
            "type": "obese"
        },
        {
            "id": 14,
            "name": "Singapur ugrasi",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "O’simlik yog’ini tovada qiziting va unga piyoz bo’laklarini solib qovuring.",
                "Qizargan piyoz ustiga pomidor solib yaxshilab qovuring.",
                "Tayyor massaga suv solib 12 minut dimlab qo’ying.",
                "Keyingi bosqichda esa unga lag’monni solib birga qovuring.",
                "Tayyor ovqatga ko’kat solib dasturxonga tortishingiz mumkin.."
            ],
            "type": "obese"
        },
        {
            "id": 15,
            "name": "Lagman",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "O’ramdagi makaronni yo’riqnomaga asosan tayyorlang.",
                "Go’sht, piyoz,sabzi va bulg’or qalampirini yupqa shaklda tilimlang.",
                "Tilimlangan go’sht va sabzavotlarni yog’da yaxshilab qovuring.",
                "Ta’bga ko’ra ziravorlarni soling.",
                "Qovurilgan maxsulotlarni yuqoridagi tayyor ugra bilan birga dasturxonga torting."
            ],
            "type": "obese"
        },
        {
            "id": 16,
            "name": "Tovuqli buritolar",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Sut va undan foydalanib hamir tayyorlang va biroz dam oldiring.",
                "Tovaga yog’ solib biroz qiziting va piyozni qizarguncha qovuring.",
                "Undan so’ng kartoshkani kub shaklida to’g’rab piyoz ustiga solib uni ham qovurib.",
                "Uning ustidan pomidor va bulg’or qalampirini uzunchoq shaklda to’grab soling va biroz qovurgach olma bo’laklarini ham soling.",
                "Tayyor hamirga massani solib huddi lavashdek qilib tuging."
            ],
            "type": "obese"
        },
        {
            "id": 17,
            "name": "Pishloqli sandvich",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Har bir non bo’lagining bir yog’iga saryog’ surkang.",
                "Pishloq bo’laklarini saryog’ surkilmagan tomonga qo’ying.",
                "Tovani o’rtacha olovda qiziting.",
                "Sandvichni olovda ikki yog’i qizarguncha qovuring."
            ],
            "type": "obese"
        },
        {
            "id": 18,
            "name": "Makaron “Aglio, olio",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Makaronni yo’riqnomaga asosan tayyorlang.",
                "Zaytun moyini tovaga solib qiziting.",
                "Tovaga maydalangan sarimsoq piyoz bo’laklarini soling va qizil tusga kirguncha qovuring.",
                "Tayyor yog’ga oldindan tayyorlanib qo’yilgan makaronni soling.",
                "Ushbu aralashmani qalampir bo’laklari bilan birga dasturxonga taqdim eting."
            ],
            "type": "obese"
        },
        {
            "id": 19,
            "name": "Sabzavotli aralashma",
            "ingredients": ["1", "1", "1", "1", "1"],
            "steps": [
                "Go’shtni qozonda yaxshilab 15-20minut qaynatib oling. Qaynatilgan go’shtni tilimlarga bo’ling.",
                "Qozonga yog’ni solib yaxshilab qiziting va piyozni oltin tusga kirgunicha qovuring. .",
                "Tayyor qovurmaga bulg’or qalampiri va pomidorni to’g’rab soling va yaxshilab qovuring..",
                "Qovurilgan massaga qaynatib qo’ygan go’sht bo’laklarini soling va ozgina suv solib dimlab qo’ying.",
                "Tayyor ovqatga ta’bizga qarab ziravorlarni soling va ko’kat va ismaloqni pishishidan 10-15 minut solib birga damlang."
            ],
            "type": "obese"
        }
]


@app.route('/', methods=['POST'])
def handle_webhook():
    try:
        process(json.loads(request.get_data()))
        return 'Success!'
    except Exception as e:
        print(e)
        return 'Error'

@app.route('/run1', methods=['HEAD'])
def timer():
    with open('timer.txt', 'r') as file:
        time = file.readline()
    with open('tasks.txt', 'r') as file:
        tasks = file.readlines()
    for task in tasks:
        if task.split()[0] == time:
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': task.split()[1],'text': f"*IT IS TIME!!!*",'message_id': task.split()[2],'parse_mode': 'Markdown'})
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/unpinAllChatMessages', params={'chat_id': task.split()[1]})
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/pinChatMessage',params={'chat_id': task.split()[1], 'message_id': task.split()[2]})
    with open('timer.txt', 'w') as file:
        file.write(str(int(time) + 5))
    return 'Success'

def random():
    global last_update_id
    last_update_id = -1
    while True:
        updates = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id}").json().get('result', [])
        for update in updates:
            process(update)
            last_update_id = update['update_id'] + 1
def process(update):
    print(update)
    if 'message' in update:
        if 'text' in update['message']:
            message = update['message']['text']
            if message == '/start':
                reply_markup = {'inline_keyboard': [[{'text': "Yuklanmoqda... 🚛", 'callback_data': f"loading"}]]}
                message_id = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'],'text': '*Choose&Cook - Sizning taom tayyorlashdagi beminnat yordamchingiz.*\n_Atigi 4 ta qadam orqali mazzali ovqat qiling!_','reply_markup': reply_markup, 'parse_mode': 'Markdown'}).json()['result']['message_id']
                reply_markup = {'inline_keyboard': [[{'text': "Sog'lig'ingiz haqida ℹ️", 'callback_data': f"health {message_id}"}]]}
                print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': update['message']['from']['id'], 'message_id': message_id, 'reply_markup': reply_markup}).json())
                with open(f"{update['message']['from']['id']}_health.txt", 'w') as file:
                    file.write("N\nN\n")
                with open(f"{update['message']['from']['id']}_catalog.txt", 'w') as file:
                    file.write('')
                with open(f"{update['message']['from']['id']}_history.txt", 'w') as file:
                    file.write('')
                options = ["Boshlash", "Mahsulotlarim", "Haftalik reja", "Ma'lumotlarim", "Ovqatlanish tarixi", "Statistika", "Taymer"]
                keyboard = {'keyboard': [options[:3],options[3:]],'one_time_keyboard': False,'resize_keyboard': True}
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={'chat_id': update['message']['from']['id'],'text': '*Salom*','reply_markup': json.dumps(keyboard),'parse_mode': 'Markdown'})
                alert(update['message']['from'])
            elif message == 'Boshlash':
                pass
            elif message == 'Mahsulotlarim':
                pass
            elif message == 'Haftalik reja':
                pass
            elif message == "Ma'lumotlarim":
                pass
            elif message == 'Statistika':
                pass
            elif message == 'Taymer':
                reply_markup = {'inline_keyboard': [[{'text': "5 daqiqa", 'callback_data': f"T 5"}], [{'text': "10 daqiqa", 'callback_data': f"T 10"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'],'text': f"*Vaqtni belgilang.*",'reply_markup': reply_markup, 'parse_mode': 'Markdown','reply_to_message_id': update['message']['message_id']})
            elif message == "Ovqatlanish tarixi":
                with open(f"{update['message']['from']['id']}_history.txt", 'r') as file:
                    lines = file.readlines()
                    if lines == '':
                        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'],'text': '_Siz hali hech qanday ovqatni tanlamagansiz!_', 'parse_mode': 'Markdown'})
                        return
                    message = '*Siz qilgan ovqatlar:*\n'
                    for line in lines:
                        message += ('_' + line + '_' + '\n')
                    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'],'text': message, 'parse_mode': 'Markdown'})
            else:
                alert(update)
    elif 'callback_query' in update and 'data' in update['callback_query']:
        data = update['callback_query']['data']
        reply_markup = update['callback_query']['message']['reply_markup']
        query_id = update['callback_query']['id']
        edit_id = update['callback_query']['message']['message_id']
        chat_id = update['callback_query']['from']['id']
        if data.split()[0] == 'health':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': query_id, 'text': "Iltimos, quyidagilarga javob bering!", 'show_alert': False})
            markup = {'inline_keyboard': [[{'text': "Menda qandli diabet mavjud 🤚", 'callback_data': f"diabetes {data.split()[1]}"}], [{'text': "Menda ortiqcha vazn bor 🤚", 'callback_data': f"weight {data.split()[1]}"}], [{'text': "Men ba'zi ovqatlarni xush ko'rmayman 🤚", 'callback_data': f"preference {data.split()[1]}"}], [{'text': "Davom ettirish ⏩", 'callback_data': f"ingredients {data.split()[1]}"}]]}
            print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': chat_id, 'message_id': int(data.split()[1]),'text': "*Sizga tegishli bo'limga bosing.*\n\n_Agar hech qaysi to'g'ri kelmasa keyingi qadamga o'ting!_", 'reply_markup': markup,'parse_mode': 'Markdown'}).json())
        elif data.split()[0] == 'ingredients':
            callback(chat_id, 0, 50, edit_id, True)
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': query_id, 'text': "Mavjud masalliqlarni tanlang!",'show_alert': False})
        if update['callback_query']['data'].split()[0].isdigit():
            callback(chat_id, int(data.split()[0]), int(data.split()[1]), edit_id, False)
        elif data.split()[0] == 'choose':
            lines = '\n'.join(update['callback_query']['message']['text'].split('\n')[2:])
            with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'w') as file:
                file.write(lines)
            catalog = lines.split('\n')
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Qidirilmoqda...",'show_alert': False})
            reply_markup = {'inline_keyboard': [[{'text': "Hech narsa topilmadi 😔", 'callback_data': "sorry"}]]}
            for meal in RECIPE:
                all_present = True
                for ingredient in meal['ingredients']:
                    if catalog[int(ingredient) - 1][-1] != '✅':
                        all_present = False
                        break
                if all_present:  # here you should add addtitional condition if the meal matches with the condition user put using the variables is_healthy, is_diabetic and is_extra_weight
                    reply_markup['inline_keyboard'].append([{'text': f"{meal['name']}", 'callback_data': f"M{meal['id']}"}])
            if len(reply_markup['inline_keyboard']) != 1:
                reply_markup['inline_keyboard'].pop(0)
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': update['callback_query']['from']['id'], 'message_id': int(data.split()[1]), 'text': "*Mos kelgan ovqatlar:*", 'parse_mode': 'Markdown', 'reply_markup': reply_markup})
        elif data.split()[0] == 'diabetes':
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                d = file.readline().strip()
                weight = file.readline().strip()
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': query_id, 'text': "Tushunarli", 'show_alert': False})
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'w') as file:
                if d == 'N':
                    file.write("Y\n")
                    reply_markup['inline_keyboard'][0][0]['text'] = reply_markup['inline_keyboard'][0][0]['text'][:-1] + "✅"
                else:
                    file.write("N\n")
                    reply_markup['inline_keyboard'][0][0]['text'] = reply_markup['inline_keyboard'][0][0]['text'][:-1] + "❌"
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'a') as file:
                file.write(f"{weight}\n")
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': chat_id, 'message_id': int(data.split()[1]),'reply_markup': reply_markup})
        elif data.split()[0] == 'weight':
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                d = file.readline().strip()
                weight = file.readline().strip()
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': query_id, 'text': "Tushunarli", 'show_alert': False})
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'w') as file:
                file.write(f"{d}\n")
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'a') as file:
                if weight == 'N':
                    file.write("Y\n")
                    reply_markup['inline_keyboard'][1][0]['text'] = reply_markup['inline_keyboard'][1][0]['text'][:-1] + "✅"
                else:
                    file.write("N\n")
                    reply_markup['inline_keyboard'][1][0]['text'] = reply_markup['inline_keyboard'][1][0]['text'][:-1] + "❌"
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': chat_id, 'message_id': int(data.split()[1]),'reply_markup': reply_markup})
        elif data == 'allergy' or data == 'preference':
            pass # shows all list of meal
        elif data == 'sorry':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Botni qayta ishga tushurish uchun /restart buyrug'ini bering",'show_alert': False})
        elif data[0] == 'M':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Yuborilmoqda...",'show_alert': False})
            chosen = int(data[1:])
            message = ''
            extra = {
                "odatiy": "Bu taom odatiy",
                "healthy": "*Bu Taom sog'lom*",
                "diabetic": "*Bu Taom diabeti borlar uchun*",
                "obese": "*Bu taom ortiqcha vaznlilar uchun*"
            }
            advice = {
                False: "_Bu taom tavsiya etilmaydi ❌_",
                True: "_Bu taom tavsiya etiladi ✅_"
            }
            is_diabetic = True
            is_extra_weight = True
            state = True
            reply_markup = {'inline_keyboard': []}
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                lines = file.readlines()
                if lines[0] == 'N':
                    is_diabetic = False
                if lines[1] == 'N':
                    is_extra_weight = False
            for meal in RECIPE:
                if meal['id'] == chosen:
                    if meal['type'] == 'diabetic':
                        state = is_diabetic
                    elif meal['type'] == 'obese':
                        state = is_extra_weight
                    message += f'*Taom nomi:* _{meal["name"]}_\n\n*Tayyorlash usuli:\n*'
                    for step in meal['steps']:
                        message += ('_- ' + step + '\n_')
                    message += '\n*Kerakli mahsulotlar*:\n'
                    for step in meal['ingredients']:
                        message += ('_- ' + INGREDIENTS[int(step) - 1][1] + '\n_')
                    message += f'\n{extra[meal["type"]]} \n {advice[state]}'
                    reply_markup = {'inline_keyboard': [[{'text': "Tarixga qo'shish", 'callback_data': f"A{meal['id']}"}]]}
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['callback_query']['from']['id'],'text': message, 'parse_mode': 'Markdown', 'reply_markup': reply_markup})
        elif data[0] == 'A':
            current_date_time = datetime.now()
            new_date_time = current_date_time + timedelta(hours=5)
            date_time_string = new_date_time.strftime("%Y-%m-%d %H:%M")
            with open(f"{update['callback_query']['from']['id']}_history.txt", 'a') as file:
                file.write(f'{data[1:]} {date_time_string}\n')
                print(data[1:], date_time_string)
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Tarixga qo'shildi ✅",'show_alert': False})
        elif data.split()[0] == 'I':
            with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'a') as file:
                file.write(f'{data.split()[1]}\n')
            text = update['callback_query']['message']['text'].split('\n')
            if text[int(data.split()[1]) + 1][-1] != '✅':
                text[int(data.split()[1]) + 1] = text[int(data.split()[1]) + 1][:-1] + '✅'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Mahsulot qo'shildi ✅",'show_alert': False})
            else:
                text[int(data.split()[1]) + 1] = text[int(data.split()[1]) + 1][:-1] + '❌'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Mahsulot olib tashlandi ✅",'show_alert': False})
            lines = '\n'.join(text)
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': chat_id, 'message_id': data.split()[2], 'text': lines, 'parse_mode': 'Markdown', 'reply_markup': reply_markup})
        elif data.split()[0] == 'T':
            with open('tasks.txt', 'a') as file:
                file.write(f"{data.split()[1]} {chat_id} {edit_id}")
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': f"{data.split()[1]} daqiqadan so'ng ogohlantiraman.",'show_alert': False})
        else:
            print(data)

def callback(user_id, start, end, message_id, is_first):
    reply_markup = {'inline_keyboard' : [[{'text': "That was all!", 'callback_data': 'limit'}]]}
    if start <= 0:
        start = 0
    if end >= len(INGREDIENTS):
        end = len(INGREDIENTS)
    count = 0
    row = []
    for i in range(start, end):
        if i == 51:
            print('yedi')
        if count == 5:
            row.append({'text': INGREDIENTS[i][0], 'callback_data': f"I {INGREDIENTS[i][0]} {message_id}"})
            reply_markup['inline_keyboard'].append(row)
            count = 0
            row = []
        else:
            count = count + 1
            row.append({'text': INGREDIENTS[i][0], 'callback_data': f"I {INGREDIENTS[i][0]} {message_id}"})
    if len(reply_markup['inline_keyboard'][0]) >= 1:
        del reply_markup['inline_keyboard'][0]
    if len(row) != 0:
        reply_markup['inline_keyboard'].append(row)
    if len(INGREDIENTS) - end >= 50:
        next = end + 50
    else:
        next = len(INGREDIENTS)
    if start >= 50:
        prev = start - 50
    else:
        prev = 0
    if end == next:
        reply_markup['inline_keyboard'].append([{'text': f"◀️", 'callback_data': f"{prev} {start}"}])
    elif prev == start:
        reply_markup['inline_keyboard'].append([{'text': f"▶️", 'callback_data': f"{end} {next}"}])
    else:
        reply_markup['inline_keyboard'].append([{'text': f"◀️", 'callback_data': f"{prev} {start}"}, {'text': f"▶️", 'callback_data': f"{end} {next}"}])
    reply_markup['inline_keyboard'].append([{'text': f"Davom ettirish ⏩", 'callback_data': f"choose {message_id}"}])
    if is_first:
        text = '*Sizda bor mahsulotlarni belgilang!*\n\n'
        for i in range(len(INGREDIENTS)):
            text += str(i + 1) + '. _' + f'{INGREDIENTS[i][1]}_.\n'
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText', json={'chat_id': user_id, 'message_id': message_id, 'text': text,'reply_markup': reply_markup, 'parse_mode': 'Markdown'})
    else:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup', json={'chat_id': user_id, 'message_id': message_id,'reply_markup': reply_markup})

def alert(user):
    params = {
        'chat_id': 5934725286,
        'text': "<strong>NEW MEMBER!!!\n</strong>" + json.dumps(user),
        'parse_mode': 'HTML',
    }
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)


#if __name__== '__main__':
#    random()

if __name__ == 'main':
    app.run(debug=False)
