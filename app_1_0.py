import json
import requests
from flask import Flask, request
global last_update_id
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
RECIPE = {
    "odatiy": {
        "Osh Palov (Plov)": {
            "ingredients": ["guruch", "sabzi", "sarimsoq", "o'simlik yog'i"],
            "steps": [
                "Gurunchni yuving va 30 daqiqa suvda ivitib qo’ying.",
                "Sabzi, piyozni to’g’rang va ta’bizga qarab sarimsoq piyoz qo’shing.",
                "Qozondagi qizigan yog’ga oldindan to’g’rab olgan sabzovatlaringizni qo’shib, oltin rang tusga kirmaguncha qovuring.",
                "Idishga suv va gurunchni solib, guruch yumshoq holatga kelguncha dimlab qo’ying",
                "Tayyor bo’lgan aralashmani dasturxonga tortishdan oldiz tayyor mayizlar bilan aralashtiring."
            ]
        },
        "Mastava": {
            "ingredients": ["guruch", "go'sht", "sabzi", "kartoshka", "piyoz", "ko'kat"],
            "steps": [
                "Guruchni yaxshilab yuving va 30 daqiqa suvda ivitib qo’ying.",
                "Sabzini, kartoshkani, piyozni va selderey barglarini to’g’rang.",
                "Go’shtni yumshoq holatga kelgunicha qaynoq suvda qaynating, keyin bo’laklarga ajrating.",
                "Qozonga to’g’ralgan sabzavotlarni, bo’laklarga bo’lingan go’shtni va gurunchni soling.",
                "Sabzavotlar yaxshi pishguncha past olovda qaynating.",
                "Dasturxonga tortishdan oldin ko’katlar bilan bezating."
            ]
        },
        "Guruchli Veggie salatii": {
            "ingredients": ["guruch", "sabzi", "piyoz", "soya", "sarimsoq"],
            "steps": [
                "Gurunchni oldin yaxshilab suvda yuvib ivitib oling.",
                "Alohida skovorodkada to'g'ralgan sabzi, piyoz va maydalangan sarimsoqni ozgina yog'da qovuring.",
                "Pishgan guruchni qovurilgan sabzavotlar bilan aralashtiring.",
                "Tayyor saladni soya yog’i bilan taqdim etsangiz bo’ladi."
            ]
        },
        "Mevali salad": {
            "ingredients": ["olma", "non", "mandarin"],
            "steps": [
                "Olma, mandarin va non bo’laklarini yaxshilab yuving va kichik bo’laklarda to’g’rang.",
                "Barcha bo’laklarni bir idishga jamlang va tayyor massani biroz muddat muzlatgichga qo’yib qo’ying."
            ]
        },
        "Pyure": {
            "ingredients": ["banan", "ismaloq", "bodom suti"],
            "steps": [
                "Banan, ismaloq va bodom sutini blenderga soling.",
                "Silliq kremsi holatga kelguncha blenderda aralashtiring.",
                "Tayyor pyureni stakanlarga soling va tortiq eting."
            ]
        },
        "Sabzavotli pechda pishirilgan tovuq": {
            "ingredients": ["sabzi", "tovuq go’sht", "piyoz", "sarimsoq", "bolgar qalampiri", "ziravorlar", "o’simlik yog’i"],
            "steps": [
                "Pechni 375°F (190°C) ga oldindan qizdiring.",
                "Katta idishda o'simlik yog'i va ziravorlar bilan tug'ralgan sabzi, kartoshka, bolgar qalampiri, piyoz va sarimsoqni aralashtiring.",
                "Sabzavotlarni pishirish varag'iga qo'ying. Yuqoridan tovuq bo'laklarini qo'shing. Tovuqni yaxshilab pishiring..",
                "Ta’bga ko’ra ziravorlarni soling.",
                "45 daqiqadan 1 soatgacha yoki tovuq pishib, sabzavotlar yumshoq bo'lguncha pishiring."
            ]
        },
        "somsa": {
            "ingredients": ["un", "sut", "go’sht", "piyoz", "ziravorlar"],
            "steps": [
                "Mol go'shti va piyozni mayda to'rtburchak shaklida to'g'rab, katta idishda barchasini aralashtiramiz va ziravorlar sepamiz.",
                "Tayyor xamirni oldindan eritib, 50 gramm keladigan bo'laklarga bo'lamiz. Likopchaga qo'yib ustini sochiq bilan yopamiz va 5 daqiqa tindiramiz..",
                "Har bir bo'lakni 3-4 millimetr qalinlikda yoyamiz. Xamirning o'rtasiga 1,5 osh qoshiq asos solib, somsani uch burchak shaklida tugamiz.",
                "Somsani pergament qog'ozi bilan qoplangan gaz pechi patnisiga joylashtirib, tuxum sarig'ini surtamiz va kunjut sepamiz. 180 C darajada qizdirilgan gaz pechiga 35-40 daqiqaga yuboramiz."
            ]
        },
        "Pishloqli tovuq": {
            "ingredients": ["pishloq", "tovuq go'sh", "piyoz", "pomidor", "ziravorlar"],
            "steps": [
                "Tovuq ko'kragini pishirishdan boshlang.Pishgan tovuq go’shtini bir-biridan ajrating",
                "Kichkina skovorodkada o'simlik moyini o'rta olovda qizdiring. 5-7 daqiqa piyozni sariq tusga kirguncha qovuring.",
                "Piyoz qovurilgancha ko’katlarni yaxshilab yuvib to’g’rang.."
            ]
        }
    },
    "diabetic": {
        "Fajita": {
            "ingredients": ["un", "go’sht", "piyoz", "ziravorlar", "sut"],
            "steps": [
                "Un va sutdan foydalanib xamir tayyorlang va 20 minut dam bering.",
                "Tayyor xamirni bo’laklarga bo’lib, aylana tarzda yupqa yoying.",
                "Go’shtni tilimlab qizigan yog’da qovurib oling.",
                "Go’sht to’q qizil holatiga kelguncha qovuring va undan so’ng yog’ga bulg’or qalampirini qo’shing.",
                "Oldindan yoyib olingan xamirni yaxshilab qovurib oling.",
                "Qovurilgan xamir ustiga birin-ketin tayyor massani qo’ying. Ta’bizga qarab boshqa ziravorlarni yoki limon suvini qo’shsangiz bo’ladi."
            ]
        },
        "Sho’rva": {
            "ingredients": ["go’sht", "kartoshka", "sabzi", "piyoz", "pomidor", "bolgar qalampiri"],
            "steps": [
                "Sabzavotlarni po’stidan ajratib, to’g’rang.",
                "Barcha maxsulotlarni qaynoq suv bilan qozonga soling.",
                "Sabzavotlar yaxshilab pishgunga qadar past olovda qaynating.",
                "Ta’bga ko’ra ziravorlar, tuz va qalampir solib tortiq eting."
            ]
        },
        "Tovuq va ismaloqli makaron": {
            "ingredients": ["makaron", "tovuq go'sht", "piyoz", "ismaloq", "o’simlik yog’i"],
            "steps": [
                "Mahsulot muqovasidagi ko'rsatmalarga muvofiq makaronni pishiring..",
                "Tovada o'simlik yog'ini o'rtacha olovda qizdiring. Tug'ralgan sarimsoq, piyoz va bolgar qalampirini qo'shing. Yumshoq bo'lgunga pishiring..",
                "To'g'ralgan tovuq go'shini qo'shing, ziravorlar qo'shing va qizarguncha pishiring.",
                "Tug'ralgan pomidor va ismaloq qo'shing, ismaloq so'lib, pomidor yumshoq bo'lguncha pishiring.",
                "Tayyorlangan makaronni tovuq va sabzavotlar bilan birlashtiring. Dasturxonga tortishdan avval maydalangan pishloq bilan ovqatni ustini bezating.."
            ]
        }
    },
    "obese": {
        "Manti": {
            "ingredients": ["un", "go’sht", "piyoz", "ziravorlar", "qatiq"],
            "steps": [
                "Suv va undan foydalnib xamir tayyorlang.",
                "Tayyor xamirni kichik bo’laklarga bo’ling.",
                "Kichik bo’lakdagi xamirlarni go’sht, piyoz va ziravorlardan tashkil topgan aralashma bilan to’ldiring.",
                "Aralashma solingan xamir bo’laklarini xuddi chuchvara kabi chekka qismlarini buklab chiqing.",
                "Tayyor maxsulotni bug’da ichidagi maxsulotlari pishguncha qoldiring.",
                "Mantini dasturxonga smetana yoki eritilgan saryog’ bilan taqdim eting."
            ]
        },
        "Tovuq sho’rva": {
            "ingredients": ["tovuq go’sht", "pomidor", "piyoz", "ziravorlar", "kartoshka", "o’simlik yog’i"],
            "steps": [
                "Qozonga yog’ solib yaxshilab qiziting.",
                "Qizigan yog’ga piyozni solib oltin rang tusga kirguncha qovuring.",
                "Qovurilgan piyozga to’g’ralgan pomidor va bulg’or qalampiri bo’laklarini solib qovuring.",
                "Ulardan so’ng tovuq go’shtini solib qovurishda davom eting.",
                "Tayyor massaga to’gralgan kartoshka va sabzini solib qovuring.",
                "Qovurilgan masalliqlarning ustiga suv solib 20 minut qaynating.",
                "Qaynab chiqqan sho’rvaga moslab ziravorlar va tuz soling.",
                "Dasturxonga tortishdan oldin ko’katlar bilan bezating."
            ]
        },
        "Singapur ugrasi": {
            "ingredients": ["lag’mon", "go’sht", "piyoz", "ziravorlar", "o’simlik yog’i"],
            "steps": [
                "O’simlik yog’ini tovada qiziting va unga piyoz bo’laklarini solib qovuring.",
                "Qizargan piyoz ustiga pomidor solib yaxshilab qovuring.",
                "Tayyor massaga suv solib 12 minut dimlab qo’ying.",
                "Keyingi bosqichda esa unga lag’monni solib birga qovuring.",
                "Tayyor ovqatga ko’kat solib dasturxonga tortishingiz mumkin.."
            ]
        },
        "Lagman": {
            "ingredients": ["lag’mon", "go’sht", "piyoz", "sabzi", "bolgar qalampiri", "ziravorlar", "o’simlik yog’i"],
            "steps": [
                "O’ramdagi makaronni yo’riqnomaga asosan tayyorlang.",
                "Go’sht, piyoz,sabzi va bulg’or qalampirini yupqa shaklda tilimlang.",
                "Tilimlangan go’sht va sabzavotlarni yog’da yaxshilab qovuring.",
                "Ta’bga ko’ra ziravorlarni soling.",
                "Qovurilgan maxsulotlarni yuqoridagi tayyor ugra bilan birga dasturxonga torting."
            ]
        },
        "Tovuqli buritolar": {
            "ingredients": ["sut", "tovuq go'sht", "kartoshka", "sabzi", "bolgar qalampiri", "ziravorlar", "olma", "o’simlik yog’i"],
            "steps": [
                "Sut va undan foydalanib hamir tayyorlang va biroz dam oldiring.",
                "Tovaga yog’ solib biroz qiziting va piyozni qizarguncha qovuring.",
                "Undan so’ng kartoshkani kub shaklida to’g’rab piyoz ustiga solib uni ham qovurib.",
                "Uning ustidan pomidor va bulg’or qalampirini uzunchoq shaklda to’grab soling va biroz qovurgach olma bo’laklarini ham soling.",
                "Tayyor hamirga massani solib huddi lavashdek qilib tuging."
            ]
        },
        "Pishloqli sandvich": {
            "ingredients": ["non", "pishloq"],
            "steps": [
                "Har bir non bo’lagining bir yog’iga saryog’ surkang.",
                "Pishloq bo’laklarini saryog’ surkilmagan tomonga qo’ying.",
                "Tovani o’rtacha olovda qiziting.",
                "Sandvichni olovda ikki yog’i qizarguncha qovuring."
            ]
        },
        "Makaron “Aglio, olio": {
            "ingredients": ["makaron", "sarimsoq"],
            "steps": [
                "Makaronni yo’riqnomaga asosan tayyorlang.",
                "Zaytun moyini tovaga solib qiziting.",
                "Tovaga maydalangan sarimsoq piyoz bo’laklarini soling va qizil tusga kirguncha qovuring.",
                "Tayyor yog’ga oldindan tayyorlanib qo’yilgan makaronni soling.",
                "Ushbu aralashmani qalampir bo’laklari bilan birga dasturxonga taqdim eting."
            ]
        },
        "Sabzavotli aralashma": {
            "ingredients": ["bolgar qalampiri", "go’sht", "piyoz", "ziravorlar", "o’simlik yog’i"],
            "steps": [
                "Go’shtni qozonda yaxshilab 15-20minut qaynatib oling. Qaynatilgan go’shtni tilimlarga bo’ling.",
                "Qozonga yog’ni solib yaxshilab qiziting va piyozni oltin tusga kirgunicha qovuring. .",
                "Tayyor qovurmaga bulg’or qalampiri va pomidorni to’g’rab soling va yaxshilab qovuring..",
                "Qovurilgan massaga qaynatib qo’ygan go’sht bo’laklarini soling va ozgina suv solib dimlab qo’ying.",
                "Tayyor ovqatga ta’bizga qarab ziravorlarni soling va ko’kat va ismaloqni pishishidan 10-15 minut solib birga damlang."
            ]
        }
    }
}

@app.route('/', methods=['POST'])
def handle_webhook():
    try:
        process(json.loads(request.get_data()))
        return 'Success!'
    except Exception as e:
        print(e)
        return 'Error'
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
            if message == '/start' or message == '/restart':
                reply_markup = {
                    'inline_keyboard': [[{'text': "Davom ettirish", 'callback_data': f"continue"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                              json={'chat_id': update['message']['from']['id'],
                                    'text': '*Men retseptlar chiqarib beraman.* _Davom etmoqchimisiz?_',
                                    'reply_markup': reply_markup, 'parse_mode': 'Markdown'})
                with open(f"{update['message']['from']['id']}.txt", 'w') as file:
                    file.write('')
                with open(f"{update['message']['from']['id']}_catalog.txt", 'w') as file:
                    file.write('')
                if message == '/start':
                    with open(f"{update['message']['from']['id']}_history.txt", 'w') as file:
                        file.write('')
                print(update)
            if message == '/history':
                with open(f"{update['message']['from']['id']}_history.txt", 'r') as file:
                    lines = file.readlines()
                    if lines == '':
                        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                                      json={'chat_id': update['message']['from']['id'],
                                            'text': '_Siz hali hech qanday ovqatni tanlamagansiz!_', 'parse_mode': 'Markdown'})
                        return
                    message = '*Siz qilgan ovqatlar:*\n'
                    for line in lines:
                        message += ('_' + line + '_' + '\n')
                    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                                  json={'chat_id': update['message']['from']['id'],
                                        'text': message, 'parse_mode': 'Markdown'})
    elif 'callback_query' in update and 'data' in update['callback_query']:
        data = update['callback_query']['data']
        if data == 'continue':
            reply_markup = {'inline_keyboard': [[{'text': "Ha", 'callback_data': f"1Y"}],
                                                [{'text': "Yo'q", 'callback_data': f"1N"}]]}
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                          json={'chat_id': update['callback_query']['from']['id'],
                                'text': "_Sog'lom ovqatlanmoqchimisiz?_", 'reply_markup': reply_markup, 'parse_mode': 'Markdown'})
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Iltimos quyidagi savollarga javob bering!",'show_alert': False})
        elif data == 'sorry':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Botni qayta ishga tushurish uchun /restart buyrug'ini bering",'show_alert': False})
        elif data == 'done':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Qidirilmoqda...",'show_alert': False})
            catalog = []
            with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    #catalog.append(line.strip())
                    catalog.append(line[:2].strip())
            message = f"*Mos kelgan ovqatlar:*"
            reply_markup = {'inline_keyboard': [[{'text': "Hech narsa topilmadi 😔", 'callback_data': "sorry"}]]}
            for type in RECIPE:
                for meal in RECIPE[type]:
                    #ingredients = RECIPE[type][meal]['ingredients']
                    ingredients = [ingredient[:2] for ingredient in RECIPE[type][meal]['ingredients']]
                    all_present = all(ingredient in catalog for ingredient in ingredients)
                    if all_present:  # here you should add addtitional condition if the meal matches with the condition user put using the variables is_healthy, is_diabetic and is_extra_weight
                        if reply_markup['inline_keyboard'][0][0]['callback_data'] == 'sorry':
                            reply_markup['inline_keyboard'].pop(0)
                        reply_markup['inline_keyboard'].append([{'text': f"{meal}", 'callback_data': f"M{meal}"}])
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['callback_query']['from']['id'],'text': message, 'parse_mode': 'Markdown', 'reply_markup': reply_markup})
        elif data[1] == 'Y' or data[1] == 'N':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Qabul qilindi ✅",'show_alert': False})
            if data[0] == '1':
                with open(f"{update['callback_query']['from']['id']}.txt", 'a') as file:
                    file.write(f'{data}\n')
                reply_markup = {'inline_keyboard': [[{'text': "Ha", 'callback_data': f"2Y"}],
                                                    [{'text': "Yo'q", 'callback_data': f"2N"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                              json={'chat_id': update['callback_query']['from']['id'],
                                    'text': "_Diabetingiz bormi?_", 'reply_markup': reply_markup, 'parse_mode': 'Markdown'})
            elif data[0] == '2':
                with open(f"{update['callback_query']['from']['id']}.txt", 'a') as file:
                    file.write(f'{data}\n')
                reply_markup = {'inline_keyboard': [[{'text': "Ha", 'callback_data': f"3Y"}],
                                                    [{'text': "Yo'q", 'callback_data': f"3N"}]]}
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                              json={'chat_id': update['callback_query']['from']['id'],
                                    'text': "_Ortiqcha vazningiz bormi?_",
                                    'reply_markup': reply_markup, 'parse_mode': 'Markdown'})
            elif data[0] == '3':
                with open(f"{update['callback_query']['from']['id']}.txt", 'a') as file:
                    file.write(f'{data}\n')
                reply_markup = {
                    'inline_keyboard': [
                        [{'text': "guruch", 'callback_data': "guruch"},
                         {'text': "sabzi", 'callback_data': "sabzi"}],
                        [{'text': "piyoz", 'callback_data': "piyoz"},
                         {'text': "sarimsoq", 'callback_data': "sarimsoq"}],
                        [{'text': "o'simlik yog'i", 'callback_data': "o'simlik yog'i"},
                         {'text': "go'sht", 'callback_data': "go'sht"}],
                        [{'text': "kartoshka", 'callback_data': "kartoshka"},
                         {'text': "ko'kat", 'callback_data': "ko'kat"}],
                        [{'text': "tovuq go'sht", 'callback_data': "tovuq go'sht"},
                         {'text': "bolgar qalampiri", 'callback_data': "bolgar qalampiri"}],
                        [{'text': "ziravorlar", 'callback_data': "ziravorlar"},
                         {'text': "non", 'callback_data': "non"}],
                        [{'text': "olma", 'callback_data': "olma"},
                         {'text': "banan", 'callback_data': "banan"}],
                        [{'text': "apelsin", 'callback_data': "apelsin"},
                         {'text': "ismaloq", 'callback_data': "ismaloq"}],
                        [{'text': "sut", 'callback_data': "sut"},
                         {'text': "un", 'callback_data': "un"}],
                        [{'text': "pomidor", 'callback_data': "pomidor"},
                         {'text': "qatiq", 'callback_data': "qatiq"}],
                        [{'text': "lag'mon", 'callback_data': "lag'mon"},
                         {'text': "pishloq", 'callback_data': "pishloq"}],
                        [{'text': "makaron", 'callback_data': "makaron"},
                         {'text': "sarimsoq", 'callback_data': "sarimsoq"}],
                        [{'text': "avokado", 'callback_data': "avokado"},
                        {'text': "mandarin", 'callback_data': "mandarin"}],
                        [{'text': "piyoz", 'callback_data': "piyoz"},
                         {'text': "soya", 'callback_data': "soya"}],
                        [{'text': "ismaloq", 'callback_data': "ismaloq"},
                         {'text': "bodom suti", 'callback_data': "bodom suti"}],
                        [{'text': "Bo'ldi", 'callback_data': "done"}],
                    ]
                }
                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                              json={'chat_id': update['callback_query']['from']['id'],
                                    'text': "*Sizda bor mahsulotlarni tanlang!*", 'reply_markup': reply_markup, 'parse_mode': 'Markdown'})
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                              json={'chat_id': update['callback_query']['from']['id'],
                                    'message_id': update['callback_query']['message'][
                                                      'message_id'] - 1})
        elif data[0] == 'M':
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Yuborilmoqda...",'show_alert': False})
            chosen = data[1:]
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
            is_healthy = True
            is_diabetic = True
            is_extra_weight = True
            state = True
            reply_markup = {'inline_keyboard': []}
            with open(f"{update['callback_query']['from']['id']}.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line[0] == '1':
                        if line[1] == 'N':
                            is_healthy = False
                    elif line[0] == '2':
                        if line[1] == 'N':
                            is_diabetic = False
                    else:
                        if line[1] == 'N':
                            is_extra_weight = False
            for type in RECIPE:
                for meal in RECIPE[type]:
                    if meal == chosen:
                        if type == 'diabetic':
                            state = is_diabetic
                        elif type == 'obese':
                            state = is_extra_weight
                        message += f'*Taom nomi:* _{meal}_\n\n*Tayyorlash usuli:\n*'
                        for step in RECIPE[type][meal]['steps']:
                            message += ('_- ' + step + '\n_')
                        message += '\n*Kerakli mahsulotlar*:\n'
                        for step in RECIPE[type][meal]['ingredients']:
                            message += ('_- ' + step + '\n_')
                        message += f'\n{extra[type]} \n {advice[state]}'
                        reply_markup = {'inline_keyboard': [[{'text': "Tarixga qo'shish", 'callback_data': f"A{meal}"}]]}
            requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id': update['callback_query']['from']['id'],'text': message, 'parse_mode': 'Markdown', 'reply_markup': reply_markup})
        elif data[0] == 'A':
            current_date_time = datetime.now()
            date_time_string = current_date_time.strftime("%Y-%m-%d %H:%M")
            with open(f"{update['callback_query']['from']['id']}_history.txt", 'a') as file:
                file.write(f'{data[1:]} {date_time_string}\n')
                print(data[1:], date_time_string)
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Tarixga qo'shildi ✅",'show_alert': False})
        else:
            with open(f"{update['callback_query']['from']['id']}_catalog.txt", 'a') as file:
                file.write(f'{data}\n')
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery",json={'callback_query_id': update['callback_query']['id'], 'text': "Mahsulot qo'shildi ✅",'show_alert': False})

#if __name__== '__main__':
#    random()

if __name__ == 'main':
    app.run(debug=False)
