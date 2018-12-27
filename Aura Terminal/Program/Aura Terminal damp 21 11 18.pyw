# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import json
import random
import pygame
import os.path
import datetime
import pyperclip

# ----------------------------------------------------------[Массивы
MAIN_DIR = os.getcwd()
CASPER = r"{}\Program files\casper.json".format(MAIN_DIR)
CONDUCTOR = r"{}\Program files\conductor.json".format(MAIN_DIR)
CUSTOM = r"{}\Program files\custom.txt".format(MAIN_DIR)
CONFIG = r"{}\Program files\config.txt".format(MAIN_DIR)
STATS = r"{}\Program files\stats.json".format(MAIN_DIR)
SELECTS = r"{}\Program files\selector.json".format(MAIN_DIR) 

config = json.load(open(CONFIG, mode="r"))

custom = json.load(open(CUSTOM, mode="r"))

stats = json.load(open(STATS, mode="r"))

# ----------------------------------------------------------[положения
botname = config["bot"]
version = config["версия"]
date = config["дата"]

# [размеры
size_window = config["размер окна"]

# [поле ввода
input_coordinate1 = config["поле ввода 1"]
input_coordinate2 = config["поле ввода 2"]
hint_coordinate1 = input_coordinate1
hint_coordinate2 = input_coordinate2
lenth_input = config["длина ввода"]

# [контактное окно
aura_coord_list = [(24, 26+20*x) for x in range(2, config["строки бота"]+3)]
lenth_output = config["длина вывода"]
session_time = config["время сессии"]
date_time = config["дата время"]

# [история
first_line_history = config["блок"]
head_history = config["шапка истории"]
page = config["фрейм истории"]
history_coord_list = [15 * i for i in range(1, config["строки истории"]+1)]

# [шапка
language = config["раскладка"]
curtain = config["главная шторка"]
build_version = config["положение версии"]
date_version = config["положение даты"]

# [цвета
black = config["цвет шрифта 1"]
white = config["цвет шрифта 2"]
gray = (150, 150, 150)

# [стиль текста
font_history = config["шрифт истории"]
font_waifu = config["шрифт бота"]
font_curtain = config["шрифт шторок"] 
font_language = config["шрифт раскладки"] 
font_user = config["шрифт ввода"]
font_date_time = config["шрифт времени"]

font_colour = (black) 

#[размер шрифта
size_head = config["размер шапки"]
size_version = config["размер версии"]
size_date = config["размер даты"]
size_shift = config["размер раскл."]
size_aura_font = config["размер шрифта бота"]
size_hint = config["размер подсказки"]
size_user_font = config["размер шрифта юзера"]
size_head_history = config["размер шапки истории"]
size_history = config["размер истории"]
size_page = config["размер фрейма"]
size_session_time = config["размер времени сессии"]
size_date_time = config["размер даты времени"]

#----------------------------------------------------------[облочные переменные
#[вывод
return_input = False
sound = True
return_to_input_step = 0
module_name = 'Main'

voice_input = False
voice_out = False
voice_answer_go = False

frame = 0             #прокрутка фрейма
number_page = 1

active_file = ''
space_append = False 

command_number = 0
time_out = 0
sleep_out = config["сон"]
#[ввод
keyboard = { 96:["ё","~"],   49:["1","!"],   50:["2","@"],  51:["3","#"],
             52:["4","$"],   53:["5","%"],   54:["6","^"],  55:["7","?"],
             56:["8","*"],   57:["9","("],   48:["0",")"],  45:["-","_"],
             61:["=","+"],  113:["й","q"],  119:["ц","w"], 101:["у","e"],
            114:["к","r"],  116:["е","t"],  121:["н","y"], 117:["г","u"],
            105:["ш","i"],  111:["щ","o"],  112:["з","p"],  91:["х","["],
             93:["ъ","]"],   92:["|","|"],   97:["ф","a"], 115:["ы","s"], 
            100:["в","d"],  102:["а","f"],  103:["п","g"], 104:["р","h"],
            106:["о","j"],  107:["л","k"],  108:["д","l"],  59:["ж",";"],
             39:["э","'"],  122:["я","z"],  120:["ч","x"],  99:["с","c"],
            118:["м","v"],   98:["и","b"],  110:["т","n"], 109:["ь","m"],
             44:["б",","],   46:["ю","."],   47:[".","?"],  32:[" "," "], }

hint_array = {    "Aura":{"добавь":"добавь|ваш вопрос|ответ бота|доп ответ|...",
                          "удали":"удали - удаляет предыдущий вопрос и ответы на него",
                          "история":"история - история переписки",
                          "скажи":"скажи <фраза для воспроизведения>"
                          },

                  "Main":{"проводник":"проводник - модуль быстрого доступа",
                          "селектор":"селектор - модуль работы с файлами (в разработке)",
                          "блокнот":"блокнот - модуль хранения текстовых файлов",
                          "аура":"аура - нейросетевой модуль",
                          "анализ":"анализ - голосовой ввод",
                          "синтез":"синтез - голосовой вывод (гуглобаба)",
                          "обзор":"обзор - статистика + содержимое модулей",
                          "тема":"тема - изменение оформления",
                          "включи":"включи <имя селекта> включает рандомный трек",
                          "открой":"открой <имя пути> открывает путь проводника"
                          },

                  "Conductor":{"добавь":"добавь|название пути|скопированный путь",
                               "удали":"удали <путь или цифра + пробел>"
                               },

                  "Notebook":{"добавь":"добавь <название листа>",
                              "удали":"удали <лист или цифра + пробел>",
                              "архив":"архив - переход в папку с листами"
                              },

                  "Selector":{"ап":"ап - добавляет теги",
                              "добавь":"добавь|название пути|скопированный путь",
                              "удали":"удали <имя селекта или цифра + пробел>",
                              "рандом":"рандом - воспроизведение рандомного файла",
                              "теги":"теги - вывод списка тегов",
                              "нм":"нм - поиск по имени или фрагменту",
                              "тг":"тг - поиск по тегу",
                              "новые":"новые - необработанные элементы",
                              "открой":"открой <имя селекта>",
                              "повтори":"повтори - повторное воспроизведение файла"
                              }              
              }

waifuname = ["aura", "аура"]

reference = ["",
             "DEL-очистка ввода",
             "",
             "ESC-предыдущий раздел",
             "",
             "TAB-вставить",
             "",
             "INS-копировать",
             "",
             "← →-последняя команда",
             "",
             "↑↓-переход к команде",
             "",
             "PU-прокрутка вверх",
             "",
             "PD-прокрутка вниз",
             "",
             "SHIFT-раскладка",
             "",
             "F1 - cправка"]


commands_for_level = ["проводник",
                  "блокнот",
                  "анализ",
                  "обзор",
                  "тема",
                  "открой",
                  "включи",
                  "синтез",
                  "аура",
                  "селектор"]

def overview_show():
    stats = j_load(STATS)
    statistics = ["* Aura:      " + str(stats["aura"]),
                  "* Notebook:  " + str(stats["notebook"]),
                  "* Selector:  " + str(stats["selector"]),
                  "* Conductor: " + str(stats["conductor"]),
                  "* Main:      " + str(stats["main"]),
                  "Enter in modul",
                  "",
                  "* Removed:   " + str(stats["del"]),
                  "* Words:     " + str(stats["words"]),
                  "* Return:    " + str(stats["return"]),
                  "* Letter:    " + str(stats["keycas"]),
                  "* Enter:     " + str(stats["enter"]),
                  "* Time work: " + str(stats["clock"]//60//60) + ':' + 
                                    str(stats["clock"]//60%60) + ':' + 
                                    str(stats["clock"]%60),
                  "Statistics",
                  "",
                  "* Records:   " + str(len(j_load(CASPER))),
                  "* Way:       " + str(len(j_load(CONDUCTOR))),
                  "* Selects:   " + str(len(j_load(SELECTS))),
                  "* Lists:     " + str(len(os.listdir(r".\Notebook"))),
                  "Content"]

    return(statistics)


emoji = ["101001", "Hay!", "Yo!", "( ._.)", "(._. )", "(>.<)", "(><)",
         "(^~^)", "(°^°)", "(^°^)", "(=^=)", "(°=°)", "(∆_∆)", "(=_=)"] #пережитки прошлого : D

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption("Aura Terminal")
pygame.image.get_extended()
image0 = pygame.image.load(r".\Program files\Image0.bmp").convert()
image1 = pygame.image.load(r".\Program files\Image1.bmp").convert() 
sleep = pygame.image.load(r".\Program files\sleep.bmp").convert()

if stats["theme"] == 1:
    theme = image1
    font_colour = (white)
    fatty_font = True

elif stats["theme"] == 0:
    theme = image0
    font_colour = (black)
    fatty_font = False


class Block:
    def __init__(self):
        self.right_block_show = []
        self.true_block = []
        self.dictionary_block = {}
        self.block_name = 'Commands'

    def load(self, name, object, enum):
        self.block_name = name
        self.clear()
        for i, box in enumerate(object):
            if enum == True:
                self.right_block_show.append(f"{i} {str(box)}")
                self.dictionary_block[i] = str(box)
                self.true_block.append(box)
            else:
                self.right_block_show.append(box)

    def clear(self):
        self.right_block_show.clear()
        self.right_block_show.extend([''] * 21)
        self.dictionary_block.clear()


aura_says = random.choice(custom["приветствие"])


class Entry:
    def __init__(self):
        self.history_cash = ['']
        self.all_cash = []
        self.return_to_input = ['']
        self.user_says_line1 = ''
        self.user_says_line2 = ''
        self.fatty_font = False
        self.user_says = ""
        self.user_hint = ""
        self.language_input = "Ru" 
        self.stick_point = 0 
        self.stick = " "
        self.copy_box = ''
        self.delete_last_letter = False

    def cut(self):    
        txt = self.user_says
        if len(txt) <= 28:
            self.user_says_line1 = txt + self.stick
            self.user_says_line2 = ''

        elif len(txt) >= 56:
            i = len(txt) - 56        
            self.user_says_line1 = txt[0+i:28+i]
            self.user_says_line2 = txt[28+i:56+i] + self.stick
    
        elif len(txt) >= 28:
            self.user_says_line1 = txt[0:28]
            self.user_says_line2 = txt[28:56] + self.stick
            
    def line_break(self, answer, land):
        ln = lenth_input
        if land == True:
            answer += self.stick
        enter_text = ['']*2
        lens = ''
        lens_test = ''
        a_split = answer.split()
        a_arr = []
        for wrd in a_split:
            if len(wrd) > ln:
                a_arr.append(wrd[:ln])
                a_arr.append(wrd[ln:])

            else:
                a_arr.append(wrd)

        for words in a_arr:

            lens_test += words + " "

            if len(lens_test) > ln:
                enter_text.append(lens)
                lens = ''
                lens_test = ''
                lens_test += words + " "
                lens += words + " "
                enter_text[-1] = lens
            else:
                lens += words + " "
                enter_text[-1] = lens

            if len(answer) < ln:
                enter_text[-2] = enter_text[-1] 
                enter_text[-1] = ''

        return(enter_text)

    def stick_switch(self):

        self.stick_point += 1
        if self.stick_point == 5:        
            if self.stick == "_":
                self.stick = " "
            
            elif self.stick == " ":
                self.stick = '_'

            self.stick_point = 0

    def entry(self, event):
        try:
            key = keyboard[event]
                        
        except KeyError:
            print(event.key)

        else:
            if self.language_input == "En":
                letter = key[1]
                            
            elif self.language_input == "Ru":
                letter = key[0]
                            
            if self.delete_last_letter == True: #правило для удалённой буквы
                self.user_says = ""
                self.delete_last_letter = False

            elif self.delete_last_letter == False: 
                self.user_says += letter
    
    def reentry(self):
        self.user_says = self.user_says[0:-1]
        overview_data("del", 1)
        if len(self.user_says) <= 0:
            pass

    def shift(self):
        if self.language_input == "En":
            self.language_input = "Ru"
                        
        elif self.language_input == "Ru":
            self.language_input = "En"

    def return_to_answer_save(self):
        try:
            self.return_to_input.remove(self.user_says)
        except ValueError:
            pass
        self.return_to_input.append(self.user_says)



def j_load(path):
    open_file = open(path, mode="r",encoding='utf8') 
    variable = json.load(open_file)
    return(variable)

def j_save(path, var):
    try:
        with open(path, 'w', encoding='utf8') as json_file:
            json.dump(var, json_file, ensure_ascii=False)
    except:
        pass

def switch_commands(key):
    global command_number 
    global user_says

    if key == 273:
        command_number += 1
        
    elif key == 274:
        command_number -= 1
    
    try:
        user_says = commands_for_level[command_number]
    except IndexError:
        if command_number > len(commands_for_level):
            command_number = -1

        elif command_number < 0:
            command_number = len(commands_for_level)
        switch_commands(key)

def aura_core(question, casper):
    
    user_say = question #ВОПРОС
    user_say_split = user_say.split()
    top_answer = [''] #ОТВЕТ
    top_coincidence = 0 #число совпадений
    coincidence_list = [] #список совпавших слов
    comparison = ''  #обрабатываемый вариант
    number = [0] * 2 #число совпадений
    for keys in casper.keys(): #keys - перебор ключей
        number.append(len(coincidence_list)) 
        
        if number[-1] == top_coincidence:
            top_answer.append(comparison) 
            
        elif number[-1] > top_coincidence: #проверка на увеличение совпадений
            top_coincidence = number[-1] 
            top_answer[0] = comparison 
            
        coincidence_list.clear() 
        comparison = keys 
        keys = keys.lower().split() 
        for words in keys: #words - проверка слов
            words = words.lower()
            
            for words1 in user_say_split: #проверка введёного варианта
                if words == words1:
                    coincidence_list.append(words)
                    
                elif words[0:-1] == words1:
                    coincidence_list.append(words)
                    
                elif words == words1[0:-1]:
                    coincidence_list.append(words)
                    
    number.append(len(coincidence_list))
    if number[-1] == top_coincidence:
            top_answer.append(comparison)
            
    elif number[-1] > top_coincidence:
            top_coincidence = number[-1]
            top_answer[0] = comparison
            
    if top_coincidence == 0:
        entry.user_hint = "Кладбище тысячи вопросов"
        return('')
        
    else:
        return(top_answer[0])

def voice_aura_says(answer):
    os.chdir(MAIN_DIR + ".\Program files")

    from gtts import gTTS
    from pygame import mixer
    mixer.init()
    mp3_nameold = '111'
    mp3_name = str(random.randint(4,10)) + ".mp3"

    ss = answer

    while ss:
        split_regex = re.compile(r'[.|!|?|…|^^]')
        sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(ss)])
        
        for x in sentences:
            if(x != ""):
                print(x)
                tts = gTTS(text=x, lang='ru')  
                try:
                    tts.save(mp3_name)                                                  # Иногда сервер отключает юзера
                except gTTSError:                                                       # до ноября всё работало
                    pass
                mixer.music.load(mp3_name)
                mixer.music.play()
                
                while mixer.music.get_busy():
                    time.sleep(0.1)
                    
                if(os.path.exists(mp3_nameold) and (mp3_nameold != "1.mp3")):
                    os.remove(mp3_nameold)
                mp3_nameold = mp3_name
                now_time = datetime.datetime.now()
                mp3_name = now_time.strftime("%d%m%Y%I%M%S")
                
        ss = ""
        
    mixer.music.load('1.mp3')
    mixer.stop
    mixer.quit
    
    if(os.path.exists(mp3_nameold)):
        try:
            os.remove(mp3_nameold)
        except PermissionError:
            pass

def history_cut(h):
    s = h[0:22]
    if len(h) >= 22:
        s = s + "~"
    return(s)

def overview_data(static, unit):
    stats[static] = stats[static] + unit
    j_save(STATS, stats)

def aura_line_break(answer):
    global otvet
    try:
        otvet = [""]*12
        ananas = answer.split()
        i1 = 0
        for i, pos in enumerate(otvet):
            for i2, element in enumerate(answer.split()):
                try:
                    line = otvet[i] + ' ' + ananas[i1]
                    if len(line) >= lenth_output:
                        pass
                    else:
                        otvet[i] = otvet[i] + ' ' + ananas[i1]
                        i1 += 1
                except:
                    pass
    except AttributeError:
        pass

#----------------------------------------------------------[ M A I N 
def main_inst():
    global module_name
    global aura_says
    global commands_for_level

    module_name = "Main"
    aura_says = random.choice(custom["мейн"])
    block.load("Commands",reference[::-1], False)
    overview_data("main", 1)
    commands_for_level = ["проводник",
                  "блокнот", "анализ","обзор", "тема", "открой",
                 "включи", "синтез", "аура", "селектор"]

def theme_go():
    global theme
    global font_colour
    global fatty_font

    if stats["theme"] == 0:
        theme = image1
        font_colour = (white)
        fatty_font = True
        stats["theme"] = 1

    elif stats["theme"] == 1:
        theme = image0
        font_colour = (black)
        fatty_font = False
        stats["theme"] = 0

    j_save(STATS, stats)

def overview_inst():
    global aura_says

    block.load("Overview",overview_show(), False)
    aura_says = random.choice(custom["обзор"])

def analisis_go():
    global voice_answer_go

    aura_says = random.choice(custom["голосовой ввод вкл"])
    if voice_answer_go == True:
        voice_answer_go = False
    elif voice_answer_go == False:
        voice_answer_go = True

def sintesis_go():
    global aura_says
    global voice_out

    if voice_out == False: 
        voice_out = True
        aura_says = random.choice(custom["синтез речи вкл"])        

    elif voice_out == True:
        voice_out = False
        aura_says = random.choice(custom["синтез речи выкл"])			                            

def manual_open():
    global aura_says

    os.system(r'start "" "справка.txt"')
    aura_says = random.choice(custom["справка"])

def voice_answer():
    global aura_says
    global voice_answer_go

    import speech_recognition as sr
    r = sr.Recognizer()
    
    with sr.Microphone() as source:                               # Внимание! только в питоне 3.7 не работает.
        print(botname + " готова выслушать тебя")
        audio = r.listen(source)

    try:
        voisanswer = r.recognize_google(audio, language="ru-RU")
        voisanswer = voisanswer.lower()
        if voisanswer.split()[0] == "aura" or voisanswer.split()[0] == "аура":
            if voisanswer[5:20] == "анализ":
                aura_says = random.choice(custom["голосовой ввод выкл"])

            else:
                entry.user_says = voisanswer[5:100]
                entry.user.hint = entry.user_says
                print(entry.user_says)
                output()
                return True
        else:
            aura_says = random.choice(custom["отсутствует префикс"])

        print(voisanswer)
            
    except sr.UnknownValueError:
        aura_says = random.choice(custom["речь не распознана"])
        print("не чёткая комманда")
            
    except sr.RequestError as e:
        print("Ошибка сервиса; {0}".format(e))

    except:
        aura_says = random.choice(custom["аут сервера"])
        voice_answer_go = False

    output()


#----------------------------------------------------------[ A U R A 
def aura_inst():
    global aura_says
    global module_name
    global commands_for_level

    module_name = "Aura"
    block.load("History",entry.history_cash, False)
    aura_says = random.choice(["Вызывали?"]) 
    entry.history_cash.append("A>>вызывали?")  
    overview_data("aura", 1)
    commands_for_level = ["добавь","скажи","удали"]

def aura_add():
    global aura_says

    casper = j_load(CASPER)
    if user_says[0:6] == "добавь":
        a_splt = user_says.split("|")
        if len(a_splt) < 3:
            aura_says = random.choice(custom["команда не верна"]) 
        else:
            try:
                for otvets in a_splt[2:]:
                    casper[a_splt[1]].append(otvets)
            except KeyError:
                casper[a_splt[1]] = []
                for otvets in a_splt[2:]:
                    casper[a_splt[1]].append(otvets)
                
            j_save(CASPER, casper)                
            aura_says = random.choice(custom["добавление вопрос ответ"]).format(a_splt[1], a_splt[2])

def aura_remove():
    global aura_says

    casper = j_load(CASPER)
    casper.pop(entry.all_cash[-1])
    j_save(CASPER, casper)
    aura_says = random.choice(custom["удаление вопроса"]).format(entry.all_cash[-1])

def aura_talk():
    global aura_says

    voice_aura_says(user_says[5:])
    aura_says = user_says[5:]

def aura_history():
    global aura_says

    block.load("History",entry.history_cash, False)
    aura_says = random.choice(custom["история"])

def aura_personality():
    global aura_says
    global user_hint

    casper = j_load(CASPER)
    entry.user_hint = aura_core(entry.user_says, casper)                            
    entry.all_cash.append(entry.user_hint)            
    aura_says = random.choice(casper[entry.user_hint])
    entry.history_cash.append("A>>" + aura_says)

#----------------------------------------------------------[ C O N D U C T O R 
def conducror_inst():
    global aura_says
    global space_append
    global module_name
    global commands_for_level

    space_append = True
    block.load("Conductor", j_load(CONDUCTOR).keys(), True)
    aura_says = random.choice(custom["проводник"])
    module_name = "Conductor"
    block.block_name = "Ways"
    commands_for_level = ["добавь", "удали"]
    overview_data("conductor", 1)

def conductor_add():
    global aura_says
    baltazar = j_load(CONDUCTOR)
    try:
        a_splt = user_says.split("|")
        baltazar[a_splt[1]] = a_splt[2]
        j_save(CONDUCTOR, baltazar)
        aura_says = random.choice(custom['добавление пути']).format(a_splt[1], a_splt[2]) 
        block.load("Conductor", j_load(CONDUCTOR).keys(), True)

    except IndexError:
        aura_says = random.choice(custom['команда не верна'])

def conductor_remove():
    global aura_says
    baltazar = j_load(CONDUCTOR)
    try:
        tagupper = True
        baltazar.pop(user_says[6:])
        j_save(CONDUCTOR, baltazar)
        block.load("Conductor", j_load(CONDUCTOR).keys(), True)
        aura_says = random.choice(custom['удаление пути']).format(user_says[6:])

    except KeyError:
        aura_says = random.choice(custom['путь отсутствует']).format(user_says[6:])

def conductor_open():
    global aura_says
    baltazar = j_load(CONDUCTOR)
    try:
        try:
            os.startfile(baltazar[dictionary_block[int(user_says)]])
            aura_says = random.choice(custom['открытие пути']).format(dictionary_block[int(user_says)]) 
            
        except ValueError:
            os.startfile(baltazar[user_says])
            aura_says = random.choice(custom['открытие пути']).format(user_says) 

    except KeyError:
        aura_says = random.choice(custom['путь отсутствует']).format(user_says)

#----------------------------------------------------------[ N O T E B O O K 

def notebook_inst():
    global aura_says
    global space_append
    global module_name
    global commands_for_level

    space_append = True
    block.load("Lists",os.listdir(r".\Notebook"),True)
    aura_says = random.choice(custom["блокнот"])          
    commands_for_level = ["добавь","архив","удали"]
    overview_data("notebook", 1)


def notebook_add():
    os.chdir(r".\Notebook")
    fname = user_says[7:]
    print(fname)
    if fname == '':
        aura_says = random.choice(custom['добавь и ничего'])
        os.chdir(MAIN_DIR)
    else:
        f = open(f"{fname}.txt", "w")
        f.close()
        aura_says = random.choice(custom["добавление листа"]).format(fname)
        os.startfile(fname + ".txt")
        os.chdir(MAIN_DIR)
        notebook_box_up()           
    
  

def notebook_remove():
    fname = user_says[6:]
    notebook_data = MAIN_DIR + "\\Notebook\\"
    if fname == '':
        aura_says = random.choice(custom['удали и ничего'])

    else:
        try:
            aura_says = random.choice(custom["удаление листа"]).format(int(fname))
            os.remove(r"{0}".format(notebook_data + str(dictionary_block[int(fname)])))
        except ValueError:
            aura_says = random.choice(custom["удаление листа"]).format(fname)
            os.remove(r"{0}".format(notebook_data + fname))

def notebook_archiv():
    os.system(r'start "" "{0}"'.format(MAIN_DIR + "\\Notebook"))
    aura_says = random.choice(custom["открытие архива"])

def notebook_open():
    global aura_says

    notebook_data = MAIN_DIR + "\\Notebook"

    try:
        number_in_box = int(user_says)                                
        os.startfile(notebook_data + "\\" + dictionary_block[number_in_box])                                                              
        aura_says = random.choice(custom["чтение листа"]).format(dictionary_block[number_in_box])

    except ValueError:
        os.startfile(notebook_data + "\\" + user_says)
        aura_says = random.choice(custom["чтение листа"]).format(user_says)

    except KeyError:
        aura_says = random.choice(["лист отсутствует"]).format(user_says)


#----------------------------------------------------------[ S E L E C T O R 
select_active = None
last_com = None
hi_lvl = False

def selector_inst():
    global aura_says
    global space_append
    global module_name
    global commands_for_level

    space_append = True
    block.load("Selects", j_load(SELECTS).keys(), True)
    aura_says = random.choice(custom["селектор"])          
    module_name = "Selector"
    commands_for_level = ["добавь","открой","удали"]

def selector_add():
    global aura_says
    try:
        add = user_says.split("|")
        slk_up = j_load(SELECTS)
        slk_up[add[1]] = {"path"  : add[2],
                          "tags"  : {},
                          "files" : {}}


        j_save(SELECTS, slk_up)
        aura_says = random.choice(custom["добавление селекта"]).format(add[1]) 

    except IndexError:
        aura_says = random.choice(custom["команда не верна"]) 

def selector_remove():
    global aura_says
    try:
        rem = user_says[6:]
        slk_up = j_load(SELECTS)
        slk_up.pop(rem)
        j_save(SELECTS, slk_up)
        aura_says = random.choice(custom["удаление селекта"]).format(rem) 
    except KeyError:
        pass

def select_open():
    global aura_says

    name = user_says[7:]
    path_file = j_load(SELECTS)[name]["path"]
    os.startfile(path_file)
    aura_says = random.choice(custom["открытие селекта"]).format(name)

def select_active_box_up():
    global aura_says
    global commands_for_level

    if entry.user_says not in block.true_block:
        pass

    block.clear()
    i = 0
    try:
        for filename in (os.listdir(j_load(SELECTS)[select_active]["path"])):
            if filename[0:9] == "AlbumArt_":
                pass
            else:
                block.dictionary_block[i] = filename
                block.right_block_show.append(f"{str(i)} {str(filename)}")
                block.true_block.append(filename)
                i +=1

    except KeyError:
        aura_says = random.choice(custom["отсутствует путь селектора"])

    commands_for_level = ["рандом", "новые", "нм", "тг","теги", "повтори","ап"]
    aura_says = random.choice(custom["селект выбран"]).format(select_active)

def select_tg_box_up():
    global aura_says

    block.clear()
    slk = j_load(SELECTS)
    i = 0
    tag_true = False
    for filename in (os.listdir(slk[select_active]["path"])):
        try:
            for tag in user_says[3:].split(","):
                if tag in slk[select_active]["files"][filename]:
                    tag_true = True

            if filename[0:9] == "AlbumArt_":
                pass

            elif tag_true == True:
                block.dictionary_block[i] = filename
                block.right_block_show.append(f"{str(i)} {str(filename)}")
                block.true_block.append(filename)
                i +=1
                tag_true = False
        except KeyError:
            pass

def select_nm_box_up():
    block.clear()
    i = 0
    for box in os.listdir(j_load(SELECTS)[select_active]["path"]):
        try:
            low = box.lower()
            low.index(user_says[3:])
            block.right_block_show.append(f"{i} {str(box)}")
            block.dictionary_block[i] = str(box)
            block.true_block.append(box)
            i +=1

        except ValueError:
            pass

        except AttributeError:
            pass

def select_new_box_up():
    global aura_says
    block.clear()
    i = 0
    for filename in (os.listdir(j_load(SELECTS)[select_active]["path"])):
        if filename[0:9] == "AlbumArt_":
            pass

        elif filename  in j_load(SELECTS)[select_active]["files"].keys():
            pass

        else:
            block.dictionary_block[i] = filename
            block.right_block_show.append(str(i) + str(filename))
            block.true_block.append(filename)
            i +=1
    aura_says = random.choice(custom["новые файлы"])

def select_active_file():
    global active_file
    global aura_says

    active_file = user_says
    path_file = j_load(SELECTS)[select_active]["path"] + "//" + user_says
    os.startfile(path_file)  
    aura_says = random.choice(custom["выбор файла"]).format(user_says)
    entry.copy_box = active_file

def select_tag_add():
    global aura_says
    slk = j_load(SELECTS)
    tags = set(user_says.split())
    tags.remove("ап")

    slk[select_active]["files"][active_file] = list(tags)
    slk[select_active]["tags"] = list(set(slk[select_active]["tags"])|tags)
    
    j_save(SELECTS, slk)
    aura_says = random.choice(custom["добавление тегов"]).format(str(list(tags))[1:-1])
    

def select_random_file():
    global active_file
    global aura_says
    global sound
    try:
        random_file = random.choice(true_block)
        active_file = random_file
        path_file = j_load(SELECTS)[select_active]["path"] + "//" + random_file
        os.startfile(path_file)  
        aura_says = random.choice(custom["выбор файла"]).format(random_file)
        entry.copy_box = random_file
    
    except:
        sound = False

#----------------------------------------------------------[ C I C L E
def output():

    screen.blit(theme, (0, 0))
    
    screen.blit(pygame.font.SysFont(font_curtain, size_head, True).render("Module:" + str(module_name), 1, white), curtain) #шапка

    screen.blit(pygame.font.SysFont(font_curtain, size_version, True).render(version, 1, white), build_version)
    screen.blit(pygame.font.SysFont(font_curtain, size_date, True).render(date, 1, white), date_version)
    
    screen.blit(pygame.font.SysFont(font_language, size_shift).render(str(entry.language_input), 1, font_colour), language)#шифт
    
    aura_line_break(aura_says)
    aura_print = pygame.font.SysFont(font_waifu, size_aura_font, fatty_font)

    for i, coord in enumerate(aura_coord_list):
        try:
            screen.blit(aura_print.render(otvet[i], 1, font_colour), coord) #ответ бота
        except:
            pass

    screen.blit(pygame.font.SysFont(font_user, size_hint).render(entry.line_break(entry.user_hint, False)[-2], 1, gray), hint_coordinate2)  #тень вопроса
    screen.blit(pygame.font.SysFont(font_user, size_hint).render(entry.line_break(entry.user_hint, False)[-1], 1, gray), hint_coordinate1)

    screen.blit(pygame.font.SysFont(font_user, size_user_font, True).render(entry.line_break(fatt, False)[-2], 1, font_colour), hint_coordinate2) #подсветка команды

    entry.cut()
    screen.blit(pygame.font.SysFont(font_user, size_user_font, entry.fatty_font).render(str(entry.line_break(entry.user_says, True)[-2]), 1, font_colour), input_coordinate2)  #текст пользователя
    screen.blit(pygame.font.SysFont(font_user, size_user_font, entry.fatty_font).render(str(entry.line_break(entry.user_says,True)[-1]), 1, font_colour), input_coordinate1) 

    screen.blit(pygame.font.SysFont(font_history, size_head_history, True).render(block.block_name, 1, font_colour), head_history)#история
    screen.blit(pygame.font.SysFont(font_history, size_page, entry.fatty_font).render("↓↑ {0}/{1}".format(str(number_page), str(len(block.right_block_show) // 21)), 1, font_colour), page)#история
    
    for i, coord in enumerate(history_coord_list):
        i += 1
        try:
            screen.blit(pygame.font.SysFont(font_history, size_history, fatty_font).render(str(history_cut(block.right_block_show[-i - frame])), 1, font_colour), (first_line_history[0],first_line_history[1] + coord))#1
        except:
            pass
    
    screen.blit(pygame.font.SysFont(font_date_time, size_date_time, fatty_font).render(str(time.ctime()), 1, font_colour), date_time)
    screen.blit(pygame.font.SysFont(font_date_time, size_session_time, fatty_font).render("Session time: " + str(int(time_clock)//60//60)
                                                                        + ":" + str(int(time_clock)//60%60)
                                                                        + ":" + str(int(time_clock) % 60), 1, font_colour), session_time)

    if time_out >= sleep_out:
        screen.blit(sleep, (0, 0))
        time.sleep(0.5)
    pygame.display.flip() #показать в окне


entry = Entry()
block = Block()


block.load("Commands",reference[::-1], False)
overview_data("enter", 1)
time_clock = 0
time_clock1 = 0



gg = True
while gg:

    time_clock = str(time.clock()).split('.')[0]
    if time_clock != time_clock1:
        stats["clock"] = stats["clock"] + 1
        time_clock1 = time_clock
        j_save(STATS, stats)
    try:
        if entry.user_says.split()[0] in commands_for_level:
            fatt =entry.user_says.split()[0]
        else:
            fatt = ""

    except IndexError:
        fatt = ''

    if return_input == True:
        return_input = False
        overview_data("return",1)
        space_append = False
        language_input = "Ru"
        command_number = 0
        overview_data("words",len(entry.user_says.split()))
        j_save(STATS, stats)
                
        try:
            number_tag = entry.user_says.split()[-1]
            entry.user_says = entry.user_says[0:-len(number_tag)] + block.dictionary_block[int(number_tag)]
        except:
            pass

        try:
            if entry.user_says[-1] == ' ':                        
                    entry.user_says = entry.user_says[0:-1]
        except IndexError:
            pass

        if entry.user_says == '':
            pass

        else:
            entry.user_hint = entry.user_says
            entry.history_cash.append("U>>" + entry.user_says)
            return_to_input_step = 0 
            answer_split = entry.user_says.split() 
            entry.language_input = "Ru" 
                    
# ----------------------------------------------------------[команды
            if entry.user_says == "меню" or entry.user_says == "мейн" or entry.user_says == "майн":
                main_inst()

            elif module_name == "Main":
                if entry.user_says == "синтез":
                    sintesis_go()
            
                elif entry.user_says == "анализ":
                    analisis_go()
    
                elif entry.user_says == "обзор":
                    overview_inst()
        
                elif entry.user_says == "проводник":
                    conducror_inst()

                elif entry.user_says == "блокнот":
                    notebook_inst()
        
                elif answer_split[0] == "аура":
                    aura_inst()
                        
                elif entry.user_says == "селектор":
                    overview_data("selector", 1)
                    selector_inst()                            

                elif entry.user_says == "тема":
                    theme_go()

                else:
                    if entry.user_says[0:6] == "открой":
                        entry.user_says = entry.user_says[7:]
                        conductor_open()
                    
                    elif entry.user_says[0:6] == "включи":
                        selector_inst()
                        select_active = entry.user_says[7:]
                        select_active_box_up()
                        select_random_file()
                        main_inst()
                        select_active = None

                        if sound != False:
                            aura_says = random.choice(custom["сейчас играет"]).format(active_file)
                            #aura_says = random.choice(custom["музыка"])
                        else:
                            aura_says = random.choice(custom["нет музыки"])
                    else:
                        aura_personality()

            elif module_name == "Aura":
                if entry.user_says[0:6] == "добавь":
                    aura_add()

                elif answer_split[0] == "удали":
                    aura_remove()

                elif entry.user_says[:5] == "скажи":
                    voice_aura_says(user_says[5:])

                else:
                    aura_personality()

                block.load("History",entry.history_cash, False)

            elif module_name == "Conductor":
                if entry.user_says[0:6] == "добавь":
                    conductor_add()

                elif answer_split[0] == "удали":
                    conductor_remove()

                else:
                    conductor_open()

                block.load("Conductor", j_load(CONDUCTOR).keys(), True)

            elif module_name == "Notebook":
                        
                if entry.user_says[0:6] == "добавь":
                    notebook_add()

                elif entry.user_says[0:5] == "удали":
                    notebook_remove()

                elif entry.user_says[0:5] == "архив":
                    notebook_archiv()

                else:
                    notebook_open()
                        
                notebook_box_up()

            elif module_name == "Selector":
                if select_active != None:
                    if entry.user_says == "теги": #вывод тегов для быстрого выбора
                        block.load("Tags",j_load(SELECTS)[select_active]["tags"], True)
                        aura_says = random.choice(custom["теги"])
                        hi_lvl = True

                    elif entry.user_says[0:2] == "ап": #добавление тега(ов)
                            select_tag_add()

                    elif entry.user_says == "рандом": # рандомный выбор файла из содержимого
                        select_random_file()
                            
                    elif entry.user_says == "новые":
                        last_com = entry.user_says
                        select_new_box_up()
                        hi_lvl = True

                    elif entry.user_says == "повтори": #повторное открытие файла
                        user_says = active_file
                        select_active_file()

                    elif entry.user_says[:2] == "тг":
                        select_tg_box_up()
                        hi_lvl = True

                    elif entry.user_says[:2] == "нм":
                        select_nm_box_up()
                        hi_lvl = True

                    else:                  #выбор файла или категории файлов  
                        if entry.user_says in true_block:
                            select_active_file()
                        else:
                            aura_says = random.choice(custom["нет файла"])
                else:
                    if entry.user_says[0:6] == "добавь":
                        selector_add()
                        selector_box_up()

                    elif entry.user_says[0:5] == "удали":
                        selector_remove()
                        selector_box_up()

                    elif entry.user_says[:6] == "открой":
                        select_open()

                    else:
                        select_active = entry.user_says
                        block_name = entry.user_says
                        select_active_box_up()

                            

            if voice_out == True:
                voice_aura_says(aura_says)

            entry.return_to_answer_save()
            entry.user_says = ''

    for event in pygame.event.get():
        if event.type == 12:
            print("Exit")
            gg = False

        if event.type == pygame.KEYDOWN:  
            overview_data("keycas", 1)

            entry.user_hint = ""

            if event.key == 32:                
                try:
                    number_tag = entry.user_says.split()[-1]
                    entry.user_says = entry.user_says[0:-len(number_tag)] + dictionary_block[int(number_tag)]
                except:
                    pass

            if event.key == pygame.K_RETURN:
                return_input = True
#----------------------------------------------------------[обработка поля ввода
            elif event.key == pygame.K_BACKSPACE:#удаление последней буквы
                entry.reentry()

            elif event.key == 27:          # ESC
                if hi_lvl == True:
                    select_active_box_up()
                    hi_lvl = False

                else:
                    select_active = None
                    main_inst()

            elif event.key == 127: #очистка поля ввода
                overview_data("del",len(entry.user_says))
                entry.user_says = ""

            elif  event.key == 273:
                switch_commands(273)

            elif  event.key == 274:
                switch_commands(274)

            elif event.key == 276: #Возврат к вопросу
                return_to_input_step = return_to_input_step - 1
                if len(return_to_input) == abs(return_to_input_step):
                    return_to_input_step = return_to_input_step + 1
                try:
                    user_says = return_to_input[return_to_input_step]
                except:
                    pass
                        
            elif event.key == 275:
                return_to_input_step = return_to_input_step + 1
                if return_to_input_step > -1:
                    return_to_input_step = -1
                try:
                    user_says = return_to_input[return_to_input_step]                        
                except:
                    pass

            elif event.key == 280:
                if number_page == 1:
                    pass
                else:
                    frame = frame - 21
                    number_page = number_page - 1
    
            elif event.key == 281:
                    
                if number_page == len(right_block_show) // 21:
                    pass
                        
                else:
                    number_page = number_page + 1
                    frame = frame + 21
                        
            elif event.key == 9:
                    user_says += pyperclip.paste()
            
            elif event.key == 277:
                pyperclip.copy(entry.copy_box)
                aura_says = random.choice(custom["копирование"]).format(entry.copy_box)

            elif event.key == 282:
                manual_open()

            elif event.key == pygame.K_LSHIFT: #смена раскладки
                entry.shift()
                
#----------------------------------------------------------[набор
            else:
                entry.entry(event.key) 
            time_out = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            time_out = 0

    if event.type == 4:
        time_out = 0

    else:
        time_out += 1

    try:
        entry.user_hint = hint_array[module_name][entry.user_says]
    except KeyError:
        pass     

    entry.stick_switch()

    if entry.user_says == "удали":
        space_append = True

    if voice_answer_go == True:
        entry.return_input = voice_answer()

    output()
    
pygame.quit()