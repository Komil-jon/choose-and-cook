import json
import math
import time

import requests
from flask import Flask, request

global last_update_id
from datetime import datetime, timedelta

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
INGREDIENTS = [['1', 'guruch', 'ingredient 1'], ['2', 'sabzi', 'ingredient 2'],
               ['3', 'piyoz', 'ingredient 3'], ['4', 'sarimsoq', 'ingredient 4'],
               ['5', "o'simlik yog'i", 'ingredient 5'], ['6', "go'sht", 'ingredient 6'],
               ['7', 'kartoshka', 'ingredient 7'], ['8', "ko'kat", 'ingredient 8'],
               ['9', 'tovuq', 'ingredient 9'], ['10', "bulg'or qalampiri", 'ingredient 10'],
               ['11', 'ziravorlar', 'ingredient 11'], ['12', 'non', 'ingredient 12'],
               ['13', 'olma', 'ingredient 13'], ['14', 'banan', 'ingredient 14'],
               ['15', 'apelsin', 'ingredient 15'], ['16', 'ismaloq', 'ingredient 16'],
               ['17', 'sut', 'ingredient 17'], ['18', 'un', 'ingredient 18'],
               ['19', 'pomidor', 'ingredient 19'], ['20', 'qatiq', 'ingredient 20'],
               ['21', "lag'mon", 'ingredient 21'], ['22', 'pishloq', 'ingredient 22'],
               ['23', 'makaron', 'ingredient 23'],] #['24', 'masalliq 24', 'ingredient 24'],
               # ['25', 'masalliq 25', 'ingredient 25'], ['26', 'masalliq 26', 'ingredient 26'],
               # ['27', 'masalliq 27', 'ingredient 27'], ['28', 'masalliq 28', 'ingredient 28'],
               # ['29', 'masalliq 29', 'ingredient 29'], ['30', 'masalliq 30', 'ingredient 30'],
               # ['31', 'masalliq 31', 'ingredient 31'], ['32', 'masalliq 32', 'ingredient 32'],
               # ['33', 'masalliq 33', 'ingredient 33'], ['34', 'masalliq 34', 'ingredient 34'],
               # ['35', 'masalliq 35', 'ingredient 35'], ['36', 'masalliq 36', 'ingredient 36'],
               # ['37', 'masalliq 37', 'ingredient 37'], ['38', 'masalliq 38', 'ingredient 38'],
               # ['39', 'masalliq 39', 'ingredient 39'], ['40', 'masalliq 40', 'ingredient 40'],
               # ['41', 'masalliq 41', 'ingredient 41'], ['42', 'masalliq 42', 'ingredient 42'],
               # ['43', 'masalliq 43', 'ingredient 43'], ['44', 'masalliq 44', 'ingredient 44'],
               # ['45', 'masalliq 45', 'ingredient 45'], ['46', 'masalliq 46', 'ingredient 46'],
               # ['47', 'masalliq 47', 'ingredient 47'], ['48', 'masalliq 48', 'ingredient 48'],
               # ['49', 'masalliq 49', 'ingredient 49'], ['50', 'masalliq 50', 'ingredient 50'],
               # ['51', 'masalliq 51', 'ingredient 51'], ['52', 'masalliq 52', 'ingredient 52'],
               # ['53', 'masalliq 53', 'ingredient 53'], ['54', 'masalliq 54', 'ingredient 54'],
               # ['55', 'masalliq 55', 'ingredient 55'], ['56', 'masalliq 56', 'ingredient 56'],
               # ['57', 'masalliq 57', 'ingredient 57'], ['58', 'masalliq 58', 'ingredient 58'],
               # ['59', 'masalliq 59', 'ingredient 59'], ['60', 'masalliq 60', 'ingredient 60'],
               # ['61', 'masalliq 61', 'ingredient 61'], ['62', 'masalliq 62', 'ingredient 62'],
               # ['63', 'masalliq 63', 'ingredient 63'], ['64', 'masalliq 64', 'ingredient 64'],
               # ['65', 'masalliq 65', 'ingredient 65'], ['66', 'masalliq 66', 'ingredient 66'],
               # ['67', 'masalliq 67', 'ingredient 67'], ['68', 'masalliq 68', 'ingredient 68'],
               # ['69', 'masalliq 69', 'ingredient 69'], ['70', 'masalliq 70', 'ingredient 70'],
               # ['71', 'masalliq 71', 'ingredient 71'], ['72', 'masalliq 72', 'ingredient 72'],
               # ['73', 'masalliq 73', 'ingredient 73'], ['74', 'masalliq 74', 'ingredient 74'],
               # ['75', 'masalliq 75', 'ingredient 75'], ['76', 'masalliq 76', 'ingredient 76'],
               # ['77', 'masalliq 77', 'ingredient 77'], ['78', 'masalliq 78', 'ingredient 78'],
               # ['79', 'masalliq 79', 'ingredient 79'], ['80', 'masalliq 80', 'ingredient 80'],
               # ['81', 'masalliq 81', 'ingredient 81'], ['82', 'masalliq 82', 'ingredient 82'],
               # ['83', 'masalliq 83', 'ingredient 83'], ['84', 'masalliq 84', 'ingredient 84'],
               # ['85', 'masalliq 85', 'ingredient 85'], ['86', 'masalliq 86', 'ingredient 86'],
               # ['87', 'masalliq 87', 'ingredient 87'], ['88', 'masalliq 88', 'ingredient 88'],
               # ['89', 'masalliq 89', 'ingredient 89'], ['90', 'masalliq 90', 'ingredient 90'],
               # ['91', 'masalliq 91', 'ingredient 91'], ['92', 'masalliq 92', 'ingredient 92'],
               # ['93', 'masalliq 93', 'ingredient 93'], ['94', 'masalliq 94', 'ingredient 94'],
               # ['95', 'masalliq 95', 'ingredient 95'], ['96', 'masalliq 96', 'ingredient 96'],
               # ['97', 'masalliq 97', 'ingredient 97'], ['98', 'masalliq 98', 'ingredient 98'],
               # ['99', 'masalliq 99', 'ingredient 99'], ['100', 'masalliq 100', 'ingredient 100'],
               # ['101', 'masalliq 101', 'ingredient 101'], ['102', 'masalliq 102', 'ingredient 102'],
               # ['103', 'masalliq 103', 'ingredient 103'], ['104', 'masalliq 104', 'ingredient 104'],
               # ['105', 'masalliq 105', 'ingredient 105']]
MEALS = [['1', "Osh Palov (Plov)", "not available", 234], ['2', "Mastava", "not available", 432], ['3', "Guruchli Veggie salatii", "not available", 100], ['4', "Mevali salad", "not available", 100], ['5', "Pyure", "not available", 100], ['6', "Sabzavotli pechda pishirilgan tovuq", "not available", 100], ['7', "Somsa", "not available", 100], ['8', "Pishloqli tovuq", "not available", 100], ['9', "Fajita", "not available", 100], ['10', "Sho’rva", "not available", 100], ['11', "Tovuq va ismaloqli makaron", "not available", 100], ['12', "Manti", "not available", 100], ['13', "Tovuq sho’rva", "not available", 100], ['14', "Singapur ugrasi", "not available", 100], ['15', "Lagman", "not available", 100], ['16', "Tovuqli buritolar", "not available", 100], ['17', "Pishloqli sandvich", "not available", 100], ['18', "Makaron Aglio", "not available", 100], ['19', "Sabzavotli aralashma", "not available", 100]]
RECIPE = [
    {
        "id": 1,
        "name": "Osh Palov (Plov)",
        "ingredients": ["1", "2", "3", "5"],
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
        "ingredients": ["1", "2", "3", "6", "7", "8"],
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
        "ingredients": ["1", "2", "3", "4", "5"],
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
        "ingredients": ["13", "14", "15"],
        "steps": [
            "Olma, mandarin va non bo’laklarini yaxshilab yuving va kichik bo’laklarda to’g’rang.",
            "Barcha bo’laklarni bir idishga jamlang va tayyor massani biroz muddat muzlatgichga qo’yib qo’ying."
        ],
        "type": "odatiy"
    },
    {
        "id": 5,
        "name": "Pyure",
        "ingredients": ["3", "7", "8", "5"],
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
        "ingredients": ["2", "3", "4", "5", "7", "10", "11"],
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
        "name": "Somsa",
        "ingredients": ["3", "4", "5", "6", "11"],
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
        "ingredients": ["3", "4", "5", "8", "9"],
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
        "ingredients": ["5", "6", "10", "17", "18"],
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
        "ingredients": ["2", "3", "5", "10", "11"],
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
        "ingredients": ["3", "4", "5", "9", "17", "19", "22", "23"],
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
        "ingredients": ["3", "6", "11", "18", "20"],
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
        "ingredients": ["2", "3", "5", "7", "8", "9", "10", "11", "19"],
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
        "ingredients": ["3", "5", "8", "19", "21"],
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
        "ingredients": ["2", "3", "6", "10", "11"],
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
        "ingredients": ["3", "5", "7", "10", "13", "17", "18", "19"],
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
        "ingredients": ["5", "11", "12", "20", "22"],
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
        "name": "Makaron Aglio",
        "ingredients": ["4", "5", "23"],
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
        "ingredients": ["3", "5", "6", "10", "11"],
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


@app.route('/count', methods=['GET'])
def timer():
    current = int(time.time() / 60)
    with open('tasks.txt', 'r') as file:
        tasks = file.readlines()
    for task in tasks:
        if abs(int(task.split()[0]) - current) <= 5:
            print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': int(task.split()[1]), 'text': f"*IT IS TIME!!!*", 'message_id': int(task.split()[2]),'parse_mode': 'Markdown'}).json())
            print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/unpinAllChatMessages',params={'chat_id': int(task.split()[1])}).json())
            print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/pinChatMessage',params={'chat_id': int(task.split()[1]), 'message_id': int(task.split()[2])}).json())
    try:
        response = requests.head('https://choose-cook.onrender.com/count')
        if response.status_code == 200:
            print(f"Successfully pinged")
        else:
            print(f"Failed to ping. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error while pinging: {e}")
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
                print(message_id)
                reply_markup = {
                    'inline_keyboard': [[{'text': "Sog'lig'ingiz haqida ℹ️", 'callback_data': f"health {message_id}"}]]}
                print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': update['message']['from']['id'], 'message_id': message_id,'reply_markup': reply_markup}).json())
                with open(f"{update['message']['from']['id']}_health.txt", 'w') as file:
                    file.write("N\nN\n")
                with open(f"{update['message']['from']['id']}_catalog.txt", 'w') as file:
                    file.write('')
                with open(f"{update['message']['from']['id']}_history.txt", 'w') as file:
                    file.write('')
                alert(update['message']['from'])
            elif message == 'Boshlash':
                message = '*Sizdagi masalliqlar:*\n\n'
                with open(f"{update['message']['from']['id']}_catalog.txt", 'r') as file:
                    lines = file.readlines()
                for line in lines:
                    if line[-2] == '✅':
                        message += "- _" + str(INGREDIENTS[int(line.split()[0][:-1]) - 1][1]) + "_\n"
                try:
                    if lines[-1][-1] == "✅":
                        message += "- _" + str(INGREDIENTS[int(lines[-1].split()[0][:-1]) - 1][1]) + "_\n"
                except:
                    pass
                reply_markup = {'inline_keyboard': [[{'text': "Yuklanmoqda... 🚛", 'callback_data': f"loading"}]]}
                message_id = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'], 'text': message,'reply_markup': reply_markup, 'parse_mode': 'Markdown'}).json()['result']['message_id']
                reply_markup = {'inline_keyboard': [[{'text': "Mahsulotlarimni tahrirlash", 'callback_data': f"ingredients 1 1"}],[{'text': "Davom etish ⏩", 'callback_data': f"choose {message_id} 2"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': update['message']['from']['id'], 'message_id': message_id,'reply_markup': reply_markup})
            elif message == 'Mahsulotlarim':
                message = '*Sizdagi masalliqlar:*\n\n'
                with open(f"{update['message']['from']['id']}_catalog.txt", 'r') as file:
                    lines = file.readlines()
                for line in lines:
                    if line[-2] == '✅':
                        message += "- _" + str(INGREDIENTS[int(line.split()[0][:-1]) - 1][1]) + "_\n"
                try:
                    if lines[-1][-1] == "✅":
                        message += "- _" + str(INGREDIENTS[int(lines[-1].split()[0][:-1]) - 1][1]) + "_\n"
                except:
                    pass
                reply_markup = {'inline_keyboard': [[{'text': "Yuklanmoqda... 🚛", 'callback_data': f"loading"}]]}
                message_id = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'], 'text': message,'reply_markup': reply_markup, 'parse_mode': 'Markdown'}).json()['result']['message_id']
                reply_markup = {'inline_keyboard': [[{'text': "Mahsulotlarimni tahrirlash", 'callback_data': f"ingredients 1 0"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': update['message']['from']['id'], 'message_id': message_id,'reply_markup': reply_markup})
            elif message == 'Haftalik reja':
                pass
            elif message == "Ma'lumotlarim":
                reply_markup = {'inline_keyboard': [[{'text': "Yuklanmoqda... 🚛", 'callback_data': f"loading"}]]}
                message_id = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'],'text': "*Sizga tegishli bo'limga bosing.*\n\n_Agar hech qaysi to'g'ri kelmasa keyingi qadamga o'ting!_",'reply_markup': reply_markup, 'parse_mode': 'Markdown'}).json()['result']['message_id']
                with open(f"{update['message']['from']['id']}_health.txt", 'r') as file:
                    diabet = file.readline().strip()
                    weight = file.readline().strip()
                table = {
                    'Y': '✅',
                    'N': '❌'
                }
                markup = {'inline_keyboard': [[{'text': f"Menda qandli diabet mavjud {table[diabet]}",'callback_data': f"diabetes {message_id}"}], [{'text': f"Menda ortiqcha vazn bor {table[weight]}",'callback_data': f"weight {message_id}"}], [{'text': "Men ba'zi ovqatlarni xush ko'rmayman 🤚",'callback_data': f"preference 1 0"}]]}
                print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': update['message']['from']['id'], 'message_id': message_id,'reply_markup': markup, 'parse_mode': 'Markdown'}).json())
            elif message == 'Statistika':
                pass
            elif message == 'Taymer':
                reply_markup = {'inline_keyboard': [[{'text': "5 daqiqa", 'callback_data': f"T 5"}],[{'text': "10 daqiqa", 'callback_data': f"T 10"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'], 'text': f"*Vaqtni belgilang.*",'reply_markup': reply_markup, 'parse_mode': 'Markdown','reply_to_message_id': update['message']['message_id']})
            elif message == "Ovqatlanish tarixi":
                with open(f"{update['message']['from']['id']}_history.txt", 'r') as file:
                    lines = file.readlines()
                    if lines == '':
                        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'],'text': '_Siz hali hech qanday ovqatni tanlamagansiz!_','parse_mode': 'Markdown'})
                        return
                    message = '*Siz qilgan ovqatlar:*\n'
                    for line in lines:
                        message += ('_' + line + '_' + '\n')
                    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'], 'text': message,'parse_mode': 'Markdown'})
            else:
                alert(update)
    elif 'callback_query' in update and 'data' in update['callback_query']:
        data = update['callback_query']['data']
        reply_markup = update['callback_query']['message']['reply_markup']
        query_id = update['callback_query']['id']
        edit_id = update['callback_query']['message']['message_id']
        chat_id = update['callback_query']['from']['id']
        if data.split()[0] == 'health':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': query_id, 'text': "Iltimos, quyidagilarga javob bering!",'show_alert': False})
            markup = {'inline_keyboard': [
                [{'text': "Menda qandli diabet mavjud 🤚", 'callback_data': f"diabetes {data.split()[1]}"}],
                [{'text': "Menda ortiqcha vazn bor 🤚", 'callback_data': f"weight {data.split()[1]}"}],
                [{'text': "Men ba'zi ovqatlarni xush ko'rmayman 🤚", 'callback_data': f"preference 1 1"}],
                [{'text': "Davom ettirish ⏩", 'callback_data': f"ingredients 0 1"}]]}
            print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': chat_id, 'message_id': int(data.split()[1]),'text': "*Sizga tegishli bo'limga bosing.*\n\n_Agar hech qaysi to'g'ri kelmasa keyingi qadamga o'ting!_",'reply_markup': markup, 'parse_mode': 'Markdown'}).json())
        elif data.split()[0] == 'ingredients':
            callback(chat_id, 0, 50, edit_id, True, int(data.split()[1]), int(data.split()[2]))
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
                          json={'callback_query_id': query_id, 'text': "Mavjud masalliqlarni tanlang!",
                                'show_alert': False})
        elif update['callback_query']['data'].split()[0].isdigit():
            if data.split()[3] == 'I':
                callback(chat_id, int(data.split()[0]), int(data.split()[1]), edit_id, False, int(data.split()[1]),
                         int(data.split()[2]))
            else:
                second(chat_id, edit_id, int(data.split()[0]), int(data.split()[1]), False, data.split()[2])
        elif data == 'save':
            lines = '\n'.join(update['callback_query']['message']['text'].split('\n')[2:])
            with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'w') as file:
                file.write(lines)
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': query_id, 'text': "Saqlandi ✅", 'show_alert': False})
        elif data == 'save_meal':
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                weight  = file.readline().strip()
                diabet = file.readline().strip()
            lines = '\n'.join([weight, diabet] + update['callback_query']['message']['text'].split('\n')[2:]) + '\n'
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'w') as file:
                file.write(lines)
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': query_id, 'text': "Saqlandi ✅", 'show_alert': False})
        elif data.split()[0] == 'choose':
            reply_markup = {'inline_keyboard': [[{'text': "Hech narsa topilmadi 😔", 'callback_data': "sorry"}]]}
            if data.split()[2] == '1':
                lines = '\n'.join(update['callback_query']['message']['text'].split('\n')[2:])
                with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'w') as file:
                    file.write(lines)
                catalog = lines.split('\n')
                with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                    file.readline()
                    file.readline()
                    not_recommend = file.readlines()
                for meal in RECIPE:
                    all_present = True
                    for ingredient in meal['ingredients']:
                        if catalog[int(ingredient) - 1][-1] != '✅':
                            all_present = False
                            break
                    if all_present:  # here you should add addtitional condition if the meal matches with the condition user put using the variables is_healthy, is_diabetic and is_extra_weight
                        add = True
                        for a in not_recommend:
                            if int(a.split()[0][:-1]) == meal['id']:
                                if a[-2] == '❌':
                                    add = False
                                break
                        if add:
                            reply_markup['inline_keyboard'].append([{'text': f"{meal['name']}", 'callback_data': f"M{meal['id']}"}])
            else:
                with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'r') as file:
                    catalog = file.readlines()
                with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                    file.readline()
                    file.readline()
                    not_recommend = file.readlines()
                for meal in RECIPE:
                    all_present = True
                    for ingredient in meal['ingredients']:
                        if catalog[int(ingredient) - 1][-2] != '✅':
                            all_present = False
                            break
                    if all_present:  # here you should add addtitional condition if the meal matches with the condition user put using the variables is_healthy, is_diabetic and is_extra_weight
                        add = True
                        for a in not_recommend:
                            if int(a.split()[0][:-1]) == meal['id']:
                                if a[-2] == '❌':
                                    print('yedi', a[-2])
                                    add = False
                                break
                        if add:
                            reply_markup['inline_keyboard'].append([{'text': f"{meal['name']}", 'callback_data': f"M{meal['id']}"}])
            if len(reply_markup['inline_keyboard']) != 1:
                reply_markup['inline_keyboard'].pop(0)
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': update['callback_query']['from']['id'], 'message_id': int(data.split()[1]),'text': "*Mos kelgan ovqatlar:*", 'parse_mode': 'Markdown','reply_markup': reply_markup})
            if data.split()[2] == '1':
                options = ["Boshlash", "Mahsulotlarim", "Haftalik reja", "Ma'lumotlarim", "Ovqatlanish tarixi","Statistika", "Taymer"]
                buttons_per_row = math.ceil(len(options) / 3)
                options_split = [options[i:i + buttons_per_row] for i in range(0, len(options), buttons_per_row)]
                keyboard = {'keyboard': options_split, 'one_time_keyboard': True, 'resize_keyboard': True}
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",data={'chat_id': update['callback_query']['from']['id'], 'text': '*Keyinchalik quyidagi menyulardan foydalanishingiz mumkin!*','reply_markup': json.dumps(keyboard), 'parse_mode': 'Markdown'})
        elif data.split()[0] == 'choose_me':
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                weight  = file.readline().strip()
                diabet = file.readline().strip()
            lines = '\n'.join([weight, diabet] + update['callback_query']['message']['text'].split('\n')[2:]) + '\n'
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'w') as file:
                file.write(lines)
            table = {
                'Y': '✅',
                'N': '❌'
            }
            markup = {'inline_keyboard': [
                [{'text': f"Menda qandli diabet mavjud {table[diabet]}", 'callback_data': f"diabetes {data.split()[1]}"}],
                [{'text': f"Menda ortiqcha vazn bor {table[weight]}", 'callback_data': f"weight {data.split()[1]}"}],
                [{'text': "Men ba'zi ovqatlarni xush ko'rmayman 🍔", 'callback_data': f"preference 1 1"}],
                [{'text': "Davom ettirish ⏩", 'callback_data': f"ingredients 0 1"}]]}
            print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': update['callback_query']['from']['id'], 'text': "*Sizga tegishli bo'limga bosing.*\n\n_Agar hech qaysi to'g'ri kelmasa keyingi qadamga o'ting!_" ,'message_id': int(data.split()[1]), 'reply_markup': markup,'parse_mode': 'Markdown'}).json())
        elif data.split()[0] == 'diabetes':
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                d = file.readline().strip()
                weight = file.readline().strip()
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
                          json={'callback_query_id': query_id, 'text': "Tushunarli", 'show_alert': False})
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'w') as file:
                if d == 'N':
                    file.write("Y\n")
                    reply_markup['inline_keyboard'][0][0]['text'] = reply_markup['inline_keyboard'][0][0]['text'][:-1] + "✅"
                else:
                    file.write("N\n")
                    reply_markup['inline_keyboard'][0][0]['text'] = reply_markup['inline_keyboard'][0][0]['text'][
                                                                    :-1] + "❌"
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'a') as file:
                file.write(f"{weight}\n")
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',
                          json={'chat_id': chat_id, 'message_id': int(data.split()[1]), 'reply_markup': reply_markup})
        elif data.split()[0] == 'weight':
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'r') as file:
                d = file.readline().strip()
                weight = file.readline().strip()
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
                          json={'callback_query_id': query_id, 'text': "Tushunarli", 'show_alert': False})
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'w') as file:
                file.write(f"{d}\n")
            with open(f"{update['callback_query']['from']['id']}_health.txt", 'a') as file:
                if weight == 'N':
                    file.write("Y\n")
                    reply_markup['inline_keyboard'][1][0]['text'] = reply_markup['inline_keyboard'][1][0]['text'][
                                                                    :-1] + "✅"
                else:
                    file.write("N\n")
                    reply_markup['inline_keyboard'][1][0]['text'] = reply_markup['inline_keyboard'][1][0]['text'][
                                                                    :-1] + "❌"
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',
                          json={'chat_id': chat_id, 'message_id': int(data.split()[1]), 'reply_markup': reply_markup})
        elif data.split()[0] == 'preference':
            if data.split()[1] == '1':
                second(update['callback_query']['from']['id'], update['callback_query']['message']['message_id'], 0, 50, True, data.split()[2])
            elif data.split()[1] == '2':
                message = "*Ovqatlar ro'yxati:*\n\n"
                with open(f"{update['message']['from']['id']}_health.txt", 'r') as file:
                    weight = file.readline()
                    diabet = file.readline()
                    lines = file.readlines()
                for line in lines:
                    if line[-2] == '✅':
                        message += "- _" + str(MEALS[int(line.split()[0][:-1]) - 1][1]) + "_\n"
                try:
                    if lines[-1][-1] == "✅":
                        message += "- _" + str(MEALS[int(lines[-1].split()[0][:-1]) - 1][1]) + "_\n"
                except:
                    pass
                reply_markup = {'inline_keyboard': [[{'text': "Yuklanmoqda... 🚛", 'callback_data': f"loading"}]]}
                message_id = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['message']['from']['id'], 'text': message,'reply_markup': reply_markup, 'parse_mode': 'Markdown'}).json()['result']['message_id']
                reply_markup = {'inline_keyboard': [[{'text': "Tahrirlash", 'callback_data': f"edit_meal"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': update['message']['from']['id'], 'message_id': message_id,'reply_markup': reply_markup})
        elif data == 'sorry':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'],'text': "Botni qayta ishga tushurish uchun /restart buyrug'ini bering",'show_alert': False})
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
                    reply_markup = {
                        'inline_keyboard': [[{'text': "Tarixga qo'shish", 'callback_data': f"A{meal['name']}"}]]}
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                          json={'chat_id': update['callback_query']['from']['id'], 'text': message,
                                'parse_mode': 'Markdown', 'reply_markup': reply_markup})
        elif data[0] == 'A':
            current_date_time = datetime.now()
            new_date_time = current_date_time + timedelta(hours=5)
            date_time_string = new_date_time.strftime("%Y-%m-%d %H:%M")
            with open(f"{update['callback_query']['from']['id']}_history.txt", 'a') as file:
                file.write(f'{data[1:]} {date_time_string}\n')
                print(data[1:], date_time_string)
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",
                          json={'callback_query_id': update['callback_query']['id'], 'text': "Tarixga qo'shildi ✅",
                                'show_alert': False})
        elif data.split()[0] == 'I':
            table = {
                'M': 'ovqat',
                'I': 'mahsulot'
            }
            sign = {
                'M': "❌",
                'I': '✅'
            }
            # with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'a') as file:
            #    file.write(f'{data.split()[1]}\n') WELL DID NOT WORK BASICALLY IT KEPT CHANGING THE FILE
            text = update['callback_query']['message']['text'].split('\n')
            if text[int(data.split()[1]) + 1][-1] == '❌':
                text[int(data.split()[1]) + 1] = text[int(data.split()[1]) + 1][:-1] + '✅'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': f"{table[data.split()[2]]} qo'shildi ✅",'show_alert': False})
            elif text[int(data.split()[1]) + 1][-1] == '✅':
                text[int(data.split()[1]) + 1] = text[int(data.split()[1]) + 1][:-1] + '❌'
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'],'text': f"{table[data.split()[2]]} olib tashlandi ❌", 'show_alert': False})
            else:
                text[int(data.split()[1]) + 1] = text[int(data.split()[1]) + 1][:-1] + sign[data.split()[2]]
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'],'text': f"{table[data.split()[2]]} qo'shildi ✅", 'show_alert': False})
            lines = '\n'.join(text)
            print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',json={'chat_id': chat_id, 'message_id': edit_id, 'text': lines,'parse_mode': 'Markdown', 'reply_markup': reply_markup}).json())
        elif data.split()[0] == 'T':
            current = int(time.time() / 60)
            with open('tasks.txt', 'a') as file:
                file.write(f"{current + int(data.split()[1])} {chat_id} {edit_id}")
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'],'text': f"{data.split()[1]} daqiqadan so'ng ogohlantiraman.", 'show_alert': False})
        else:
            print(data)
    elif 'inline_query' in update:
        response = answer_inline_query(update['inline_query']['id'], update['inline_query']['query'])
        print(response)

def inline_query():
    # Sample data for demonstration
    sample_data = [{"title": "Result 1", "description": "Description for Result 1", "photo_url": "https://raw.githubusercontent.com/phixmexbot/recources/main/voice.png"},
        {"title": "Result 2", "description": "Description for Result 2", "photo_url": "https://raw.githubusercontent.com/phixmexbot/recources/main/voice.png"}]

    results = []

    for idx, item in enumerate(sample_data):
        title = item["title"]
        description = item["description"]
        photo_url = item["photo_url"]
        caption = f"<b>{title}</b>\n{description}"

        # Create inline query result with photo and caption
        result = {"type": "photo", "id": str(idx), "photo_url": photo_url, "thumb_url": photo_url, "caption": caption,
            "parse_mode": "HTML"}
        results.append(result)
    print(results)
    return results


# Function to answer the inline query
def answer_inline_query(query_id, query_text):
    button = {
        'text': 'text',
        "web_app": "description",
        "start_parameter" : "random"
    }
    results = [{'type': 'article', 'id': '1', 'title': 'Title 1',
        'input_message_content': {'message_text': 'Message for Result 1'}, 'description': 'Description for Result 1',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/1.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '2', 'title': 'Title 2',
        'input_message_content': {'message_text': 'Message for Result 2'}, 'description': 'Description for Result 2',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/2.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '3', 'title': 'Title 3',
        'input_message_content': {'message_text': 'Message for Result 3'}, 'description': 'Description for Result 3',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/3.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '4', 'title': 'Title 4',
        'input_message_content': {'message_text': 'Message for Result 4'}, 'description': 'Description for Result 4',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/4.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '5', 'title': 'Title 5',
        'input_message_content': {'message_text': 'Message for Result 5'}, 'description': 'Description for Result 5',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/5.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '6', 'title': 'Title 6',
        'input_message_content': {'message_text': 'Message for Result 6'}, 'description': 'Description for Result 6',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/6.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '7', 'title': 'Title 7',
        'input_message_content': {'message_text': 'Message for Result 7'}, 'description': 'Description for Result 7',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/7.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '8', 'title': 'Title 8',
        'input_message_content': {'message_text': 'Message for Result 8'}, 'description': 'Description for Result 8',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/8.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '9', 'title': 'Title 9',
        'input_message_content': {'message_text': 'Message for Result 9'}, 'description': 'Description for Result 9',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/9.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '10', 'title': 'Title 10',
        'input_message_content': {'message_text': 'Message for Result 10'}, 'description': 'Description for Result 10',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/10.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '11', 'title': 'Title 11',
        'input_message_content': {'message_text': 'Message for Result 11'}, 'description': 'Description for Result 11',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/11.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '12', 'title': 'Title 12',
        'input_message_content': {'message_text': 'Message for Result 12'}, 'description': 'Description for Result 12',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/12.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '13', 'title': 'Title 13',
        'input_message_content': {'message_text': 'Message for Result 13'}, 'description': 'Description for Result 13',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/13.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '14', 'title': 'Title 14',
        'input_message_content': {'message_text': 'Message for Result 14'}, 'description': 'Description for Result 14',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/14.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '15', 'title': 'Title 15',
        'input_message_content': {'message_text': 'Message for Result 15'}, 'description': 'Description for Result 15',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/15.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '16', 'title': 'Title 16',
        'input_message_content': {'message_text': 'Message for Result 16'}, 'description': 'Description for Result 16',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/16.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '17', 'title': 'Title 17',
        'input_message_content': {'message_text': 'Message for Result 17'}, 'description': 'Description for Result 17',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/17.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '18', 'title': 'Title 18',
        'input_message_content': {'message_text': 'Message for Result 18'}, 'description': 'Description for Result 18',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/18.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '19', 'title': 'Title 19',
        'input_message_content': {'message_text': 'Message for Result 19'}, 'description': 'Description for Result 19',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/19.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '20', 'title': 'Title 20',
        'input_message_content': {'message_text': 'Message for Result 20'}, 'description': 'Description for Result 20',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/20.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '21', 'title': 'Title 21',
        'input_message_content': {'message_text': 'Message for Result 21'}, 'description': 'Description for Result 21',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/21.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '22', 'title': 'Title 22',
        'input_message_content': {'message_text': 'Message for Result 22'}, 'description': 'Description for Result 22',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/22.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '23', 'title': 'Title 23',
        'input_message_content': {'message_text': 'Message for Result 23'}, 'description': 'Description for Result 23',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/23.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '24', 'title': 'Title 24',
        'input_message_content': {'message_text': 'Message for Result 24'}, 'description': 'Description for Result 24',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/24.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '25', 'title': 'Title 25',
        'input_message_content': {'message_text': 'Message for Result 25'}, 'description': 'Description for Result 25',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/25.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '26', 'title': 'Title 26',
        'input_message_content': {'message_text': 'Message for Result 26'}, 'description': 'Description for Result 26',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/26.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '27', 'title': 'Title 27',
        'input_message_content': {'message_text': 'Message for Result 27'}, 'description': 'Description for Result 27',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/27.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '28', 'title': 'Title 28',
        'input_message_content': {'message_text': 'Message for Result 28'}, 'description': 'Description for Result 28',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/28.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '29', 'title': 'Title 29',
        'input_message_content': {'message_text': 'Message for Result 29'}, 'description': 'Description for Result 29',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/29.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '30', 'title': 'Title 30',
        'input_message_content': {'message_text': 'Message for Result 30'}, 'description': 'Description for Result 30',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/30.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '31', 'title': 'Title 31',
        'input_message_content': {'message_text': 'Message for Result 31'}, 'description': 'Description for Result 31',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/31.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '32', 'title': 'Title 32',
        'input_message_content': {'message_text': 'Message for Result 32'}, 'description': 'Description for Result 32',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/32.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '33', 'title': 'Title 33',
        'input_message_content': {'message_text': 'Message for Result 33'}, 'description': 'Description for Result 33',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/33.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '34', 'title': 'Title 34',
        'input_message_content': {'message_text': 'Message for Result 34'}, 'description': 'Description for Result 34',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/34.png', 'thumb_width': 10,
        'thumb_height': 10, }, {'type': 'article', 'id': '35', 'title': 'Title 35',
        'input_message_content': {'message_text': 'Message for Result 35'}, 'description': 'Description for Result 35',
        'thumb_url': 'https://raw.githubusercontent.com/sevara10/Resources/main/35.png', 'thumb_width': 10,
        'thumb_height': 10, }, ]
    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerInlineQuery", data={"inline_query_id": query_id, "results": json.dumps(results), 'button': json.dumps(button),  "cache_time": 0})
    return response.json()


def callback(user_id, start, end, message_id, is_first, update, go_on):
    reply_markup = {'inline_keyboard': [[{'text': "That was all!", 'callback_data': 'limit'}]]}
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
            row.append({'text': INGREDIENTS[i][0], 'callback_data': f"I {INGREDIENTS[i][0]} I"})
            reply_markup['inline_keyboard'].append(row)
            count = 0
            row = []
        else:
            count = count + 1
            row.append({'text': INGREDIENTS[i][0], 'callback_data': f"I {INGREDIENTS[i][0]} I"})
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
        reply_markup['inline_keyboard'].append([{'text': f"◀️", 'callback_data': f"{prev} {start} {go_on} I"}])
    elif prev == start:
        reply_markup['inline_keyboard'].append([{'text': f"▶️", 'callback_data': f"{end} {next} {go_on} I"}])
    else:
        reply_markup['inline_keyboard'].append([{'text': f"◀️", 'callback_data': f"{prev} {start} {go_on} I"},
                                                {'text': f"▶️", 'callback_data': f"{end} {next} {go_on} I"}])
    if go_on:
        reply_markup['inline_keyboard'].append([{'text': f"Saqlash", 'callback_data': f"save"},
                                                {'text': f"Davom ettirish ⏩",
                                                 'callback_data': f"choose {message_id} 1"}])
    else:
        reply_markup['inline_keyboard'].append([{'text': f"Saqlash", 'callback_data': f"save"}])
    if is_first:
        text = '*Sizda bor mahsulotlarni belgilang!*\n\n'
        if update != 0:
            with open(f"{user_id}_catalog.txt", 'r') as file:
                lines = file.readlines()
            for line in lines:
                text += line
        else:
            for i in range(len(INGREDIENTS)):
                text += str(i + 1) + '. _' + f'{INGREDIENTS[i][1]}_.\n'
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',
                      json={'chat_id': user_id, 'message_id': message_id, 'text': text, 'reply_markup': reply_markup,
                            'parse_mode': 'Markdown'})
    else:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',
                      json={'chat_id': user_id, 'message_id': message_id, 'reply_markup': reply_markup})


def second(user_id, message_id, start, end, is_first, go_on):
    print(go_on)
    reply_markup = {'inline_keyboard': [[{'text': "That was all!", 'callback_data': 'limit'}]]}
    if start <= 0:
        start = 0
    if end >= len(MEALS):
        end = len(MEALS)
    count = 0
    row = []
    for i in range(start, end):
        if i == 51:
            print('yedi')
        if count == 5:
            row.append({'text': MEALS[i][0], 'callback_data': f"I {MEALS[i][0]} M"})
            reply_markup['inline_keyboard'].append(row)
            count = 0
            row = []
        else:
            count = count + 1
            row.append({'text': MEALS[i][0], 'callback_data': f"I {MEALS[i][0]} M"})
    if len(reply_markup['inline_keyboard'][0]) >= 1:
        del reply_markup['inline_keyboard'][0]
    if len(row) != 0:
        reply_markup['inline_keyboard'].append(row)
    if len(MEALS) - end >= 50:
        next = end + 50
    else:
        next = len(MEALS)
    if start >= 50:
        prev = start - 50
    else:
        prev = 0
    if end == next:
        reply_markup['inline_keyboard'].append([{'text': f"◀️", 'callback_data': f"{prev} {start} {go_on} M"}])
    elif prev == start:
        reply_markup['inline_keyboard'].append([{'text': f"▶️", 'callback_data': f"{end} {next} {go_on} M"}])
    else:
        reply_markup['inline_keyboard'].append([{'text': f"◀️", 'callback_data': f"{prev} {start} {go_on} M"},{'text': f"▶️", 'callback_data': f"{end} {next} {go_on} M"}])
    if go_on == '1':
        reply_markup['inline_keyboard'].append([{'text': f"Saqlash", 'callback_data': f"save_meal"},{'text': f"Davom ettirish ⏩",'callback_data': f"choose_me {message_id} 1"}])
    else:
        reply_markup['inline_keyboard'].append([{'text': f"Saqlash", 'callback_data': f"save_meal"}])
    if is_first:
        text = '*Sizga tavsiya etilmaydigan ovqatlarni belgilang!*\n\n'
        with open(f'{user_id}_health.txt', 'r') as file:
            lines = file.readlines()
        if len(lines) == 2:
            for i in range(len(MEALS)):
                text += str(i + 1) + '. _' + f'{MEALS[i][1]}_.\n'
        else:
            with open(f"{user_id}_health.txt", 'r') as file:
                lines = file.readlines()
            i = 0
            for line in lines:
                i += 1
                if i > 2:
                    text += line
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText', json={'chat_id': user_id, 'message_id': message_id, 'text': text,'reply_markup': reply_markup, 'parse_mode': 'Markdown'})
    else:
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup',json={'chat_id': user_id, 'message_id': message_id, 'reply_markup': reply_markup})


def alert(user):
    params = {
        'chat_id': 5934725286,
        'text': "<strong>NEW MEMBER!!!\n</strong>" + json.dumps(user),
        'parse_mode': 'HTML',
    }
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)


#if __name__ == '__main__':
#    random()

if __name__ == 'main':
   app.run(debug=False)
