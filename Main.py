import os
from random import randrange
import time
from mutagen.mp3 import MP3
from sys import exit
from shutil import move as Move_File
from tkinter import filedialog
import threading
from vars import *

def easter_egg(easter_color):
    global text_stage
    if Rainbow_mode == True:
        match text_stage:
            case 'red':
                easter_color[1] += 1
                if easter_color[1] == 255:
                    text_stage = 'yellow'

            case 'yellow':
                easter_color[0] -= 1
                if easter_color[0] == 0:
                    text_stage = 'green'

            case 'green':
                easter_color[2] += 1
                if easter_color[2] == 255:
                    text_stage = 'cyan'

            case 'cyan':
                easter_color[1] -= 1
                if easter_color[1] == 0:
                    text_stage = 'blue'

            case 'blue':
                easter_color[0] += 1
                if easter_color[0] == 255:
                    text_stage = 'magenta'

            case 'magenta':
                easter_color[2] -= 1
                if easter_color[2] == 0:
                    text_stage = 'red'

        return tuple(easter_color)
    return 'black'

def reset_playbar_values():
    global time_init
    global temp_percent
    global temp_init
    global temp_buffer
    global song_percent
    global time_offset
    time_init = time.time()
    temp_percent = 0
    temp_init = 0
    temp_buffer = 0
    song_percent = 0
    time_offset = 0

def get_song_number(list, song):
    song = 'songs/' + song
    for i in range(len(list)):
        if song == list[i]:
            return i
    return 0

def get_song_playing_name(id, menu_offet=menu_offset):
    return song_array[id + menu_offset].replace('songs/', '')

song_array = os.listdir('songs')
def generate_list(song_array):
    temp_array = song_array
    count = 0
    path = "songs/"
    for i in temp_array:
        temp_array[count] = path + temp_array[count]
        count += 1
    return temp_array

song_array = generate_list(song_array)

def generate_search_list(search, songs):
    temp_array = []
    search = search.lower()
    for i in songs:
        temp_song = i
        temp_song = temp_song.replace("songs/", '')
        temp_song = temp_song.lower()
        temp_song = temp_song.replace(".mp3", '')
        if search in temp_song:
            temp_array.append(i)
    return temp_array

def get_song_length(song_id):
    song_length = MP3(song_id)
    song_length = song_length.info.length
    return song_length


def switch_track(shuffle, restart=False):
    global song_playing
    global song_playing_name
    global song_length
    reset_playbar_values()
    if looped == True or restart == True:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(song_array[song_playing])
        pygame.mixer.music.play(0)
        song_playing_name = get_song_playing_name(song_playing-menu_offset)
        song_length = get_song_length(song_array[song_playing])

    elif shuffle == True:
        song_playing = randrange(len(song_array))
        pygame.mixer.music.unload()
        pygame.mixer.music.load(song_array[song_playing])
        pygame.mixer.music.play(0)
        song_playing_name = get_song_playing_name(song_playing-menu_offset)
        song_length = get_song_length(song_array[song_playing])

    else:
        try:
            song_playing += 1
            pygame.mixer.music.unload()
            pygame.mixer.music.load(song_array[song_playing])
            pygame.mixer.music.play(0)
            song_playing_name = get_song_playing_name(song_playing-menu_offset)
            song_length = get_song_length(song_array[song_playing])
        except:
            song_playing = -1
            song_playing_name = ''


for i in range(8):
    play_buttons.append(PyUI.button(assets['selection'], 40, play_buttonY))
    play_buttonY += 30

def mute_button_fn():
    global muted
    global temp_percent
    global temp_init
    global temp_buffer
    if muted == False:
        mute_button.change_sprite(assets['muted'])
        pygame.mixer.music.pause()
        muted = True
        temp_init = time.time()
    else:
        mute_button.change_sprite(assets['unmuted'])
        pygame.mixer.music.unpause()
        muted = False
        temp_buffer += temp_percent

def loop_button_fn():
    global looped
    if looped == True:
        looped = False
        loop_button.change_sprite(assets['unlooped'])
    else:
        looped = True
        loop_button.change_sprite(assets['looped'])

def shuffle_button_fn():
    global shuffle
    if shuffle == True:
        shuffle = False
        shuffle_button.change_sprite(assets['unshuffled'])
    else:
        shuffle = True
        shuffle_button.change_sprite(assets['shuffled'])

def import_file(file_path):
    if file_path[-4:] == ".mp3":
        Move_File(file_path, os.path.abspath("songs"))
        refresh()

def folder_button_action():
        path = str(filedialog.askopenfilename(title='Select a song to be added to the list', filetypes=([("MP3", "*.mp3")])))
        import_file(path)
def folder_button_fn():
    if pressed[pygame.K_LSHIFT]:
        threading.Thread(target=folder_button_action).start()
    else:
        os.startfile('songs')

def refresh():
    global song_array
    if search_string == '':
        song_array = os.listdir('songs')
        song_array = generate_list(song_array)

def auto_refresh():
    buffer = os.listdir('songs')
    while Exit == False:
        list_check = os.listdir('songs')
        if list_check != buffer:
            refresh()
        time.sleep(0.5)
refresh_thread = threading.Thread(target=auto_refresh)
refresh_thread.start()

def search_button_fn():
    global search_string
    global search_visable
    if search_visable == True:
        search_visable = False
        search_button.change_sprite(assets['arrow_up'])
        search_string = ''
        search_bar.search_string = ''
    else:
        search_visable = True
        search_button.change_sprite(assets['arrow_down'])

def play_song(id, time=0):
    global muted
    global song_playing
    global song_playing_name
    global time_init
    global song_length
    if song_array[id + menu_offset] != "" and song_array[id + menu_offset] != "Media Not Found!....":
        pygame.mixer.music.unload()
        pygame.mixer.music.load(song_array[id + menu_offset])
        pygame.mixer.music.play(loops=0, start=time)
        muted = False
        mute_button.change_sprite(assets['unmuted'])
        song_playing = id + menu_offset
        song_playing_name = get_song_playing_name(id)
        song_length = get_song_length(song_array[id + menu_offset])
        reset_playbar_values()

def up_button_fn():
    global menu_offset
    if menu_offset > 0:
        menu_offset -= 1

def down_button_fn():
    global menu_offset
    if 8 + menu_offset < len(song_array):
        menu_offset += 1

def restart_button_fn():
    global muted
    if song_playing > -1:
        mute_button.change_sprite(assets['unmuted'])
        muted = False
        switch_track(shuffle=False, restart=True)

def get_song_percent(time_init):
    play_length = time.time() - time_init
    try:
        play_length_percent = play_length / song_length
        play_length_percent *= 100
        return round(play_length_percent, 4)
    except:
        return -1

def seek_bar_fn():
    global time_offset
    if muted == False and song_playing != -1:
        percent = pygame.mouse.get_pos()
        percent = int(percent[0] / 3) -25
        length = get_song_length(song_array[song_playing])
        percent = percent / 100
        position = length * percent
        reset_playbar_values()
        play_song(song_playing-menu_offset, position)
        time_offset = percent*100


while True:
    main_menu.menu_loop()
    fps = clock.tick(60)
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if song_playing >= 0:
                    mute_button.on_click(action=mute_button_fn)
                folder_button.on_click(action=folder_button_fn)
                restart_button.on_click(action=restart_button_fn)
                shuffle_button.on_click(action=shuffle_button_fn)
                loop_button.on_click(action=loop_button_fn)
                search_button.on_click(action=search_button_fn)
                up_button.on_click(action=up_button_fn)
                down_button.on_click(action=down_button_fn)
                if search_visable == True:
                    search_bar.on_click()
                else:
                    seekbar.on_click(action=seek_bar_fn)

                for i in range(8):
                    play_buttons[i].on_click(action=lambda i=i:play_song(i))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                search_bar.backspace()
                menu_offset = 0

            if event.key == pygame.K_RETURN:
                print(search_bar.search_string)
                if search_bar.search_string.replace("|", "").lower() == "rainbowz":
                    Rainbow_mode = not Rainbow_mode

            elif search_visable == True and search_bar.string_text.get_width() < 235:
                if event.unicode != "":
                    search_bar.add_character(event.unicode)
                    menu_offset = 0

        if event.type == pygame.QUIT:
            Exit = True
            pygame.quit()
            exit()

        if event.type == pygame.DROPFILE:
            import_file(event.file)

        if event.type == pygame.MOUSEWHEEL:
            if event.y == True:
                up_button_fn()
            else:
                down_button_fn()


    if pressed[pygame.K_BACKSPACE] and search_visable == True:
        bspace_time = time.time()
        if bspace_time > bspace_start_buffer + 0.5:
            if bspace_time > bspace_char_buffer + 0.06:
                search_bar.backspace()
                menu_offset = 0
                bspace_char_buffer = time.time()
    else:
        bspace_start_buffer = time.time()
        bspace_char_buffer = time.time()

    if search_buffer != search_string:
        song_array = os.listdir('songs')
        song_array = generate_search_list(search_string, song_array)
        song_array = generate_list(song_array)
        if song_playing != -1:
            song_playing = get_song_number(song_array, song_playing_name)

    search_buffer = search_string

    if pressed[pygame.K_LSHIFT]:
        folder_button.change_sprite(assets['folder_add'])
    else:
        folder_button.change_sprite(assets['folder'])

    mute_button.display()
    shuffle_button.display()
    loop_button.display()
    folder_button.display(clicked_sprite=assets['folder_clicked'])
    up_button.display(clicked_sprite=assets['up_clicked'])
    down_button.display(clicked_sprite=assets['down_clicked'])
    search_button.display()
    seekbar.display()

    if song_playing != -1:
        restart_button.display(clicked_sprite=assets['refresh_clicked'])
    else:
        restart_button.display(clicked_sprite=None)

    if muted == True:
        temp_percent = get_song_percent(temp_init)
    else:
        song_percent = get_song_percent(time_init) + time_offset

    if song_percent != -1 and muted == False:
        seekbar_x = 75
        seekbar_x += (song_percent-temp_buffer) *3

    if seekbar_x < 75:
        seekbar_x = 75

    if search_visable == False and seekbar_y == 320:
        screen.blit(assets['seekbar_cover'], (int(seekbar_x), seekbar_y))
    screen.blit(assets['seekbar_cover_cover'], (373, 314))

    search_bar.display()
    search_string = search_bar.search_string
    search_string = search_string.replace("|", "")

    if search_visable == True:
        if search_bar.y > searchboxY:
            search_bar.y -= 5
        if seekbar_y > 290:
            seekbar_y -= 5
            seekbar.y -= 5
        if list_text_x > 345:
            list_text_x -= 5

    if search_visable == False:
        search_bar.active = False
        if search_bar.y != 357:
            search_bar.y += 5
            search_string = ""
        if seekbar_y < 320:
            seekbar_y += 5
            seekbar.y += 5
        if list_text_x < 375:
            list_text_x += 5

    for i in range(8):
        play_buttons[i].display()

    cursor_flag = 'Arrow'

    if song_playing == -1:
        mute_button.change_sprite(assets['no_muted'])
        restart_button.change_sprite(assets['refresh_disabled'])
        song_length = 0
        seekbar_x = 75
    else:
        restart_button.change_sprite(assets['refresh'])
        cursor_flag = restart_button.cursor_flag(cursor_flag)
        cursor_flag = mute_button.cursor_flag(cursor_flag)
    cursor_flag = shuffle_button.cursor_flag(cursor_flag)
    cursor_flag = loop_button.cursor_flag(cursor_flag)
    cursor_flag = folder_button.cursor_flag(cursor_flag)
    cursor_flag = up_button.cursor_flag(cursor_flag)
    cursor_flag = down_button.cursor_flag(cursor_flag)
    cursor_flag = search_button.cursor_flag(cursor_flag)
    if search_visable == True:
        cursor_flag = search_bar.cursor_flag(cursor_flag)
    elif song_playing != -1 and muted == False:
        cursor_flag = seekbar.cursor_flag(cursor_flag)

    for i in range(8):
        try:
            song = song_array[i + menu_offset].replace('songs/', '')
            if song_playing_name == song:
                y = 75
                y += (30 * (i))
                screen.blit(assets['played'], (40, y))
                song_playing_list = i
        except:
            song_playing_list = -1

    button_cursor_flags = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        button_cursor_flags[i] = play_buttons[i].cursor_flag(button_cursor_flags[i])

    for i in range(8):
        temp_flag = ''
        cursor_flag = play_buttons[i].cursor_flag(cursor_flag)
        temp_flag = play_buttons[i].cursor_flag(temp_flag)
        if temp_flag == "Hand":
            y = 75
            y += (30 * i)
            if i != song_playing_list:
                screen.blit(assets['selection_highlighted'],(40,y))
            else:
                song = song_array[i + menu_offset].replace('songs/', '')
                if song_playing_name == song:
                    screen.blit(assets['played_highlighted'],(40,y))
                else:
                    screen.blit(assets['selection_highlighted'], (40, y))

    if cursor_flag == 'Hand':
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif cursor_flag == 'Ibeam':
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def fill_list(song_list):
        while len(song_list) != 8:
            song_list.append("Media Not Found!....")
        return song_list

    if len(song_array) < 8:
        song_array = fill_list(song_array)

    text_color = easter_egg(easter_color)

    song_text_array = [0,0,0,0,0,0,0,0]
    for i in range(8):

       try:
           song_array[i+menu_offset]
       except:
           menu_offset -= 1
       if song_array[i+menu_offset] == "Media Not Found!....":
           if search_string == '':
               song_text_array[i] = font.render(str(song_array[i + menu_offset]), True, 'red')
           else:
               song_text_array[i] = font.render('', True, 'red')
       else:
           truncation = 4
           truncation_string = ''
           while song_text_array[i] == 0 or song_text_array[i].get_width() > 330:
               if button_cursor_flags[i] == "Hand" and pygame.mouse.get_pressed() == (True, False, False):
                   song_text_array[i] = font.render(str(song_array[i+menu_offset].replace('songs/', '')[:-truncation] + truncation_string), True,'white')
               else:
                    song_text_array[i] = font.render(str(song_array[i+menu_offset].replace('songs/', '')[:-truncation] + truncation_string), True, text_color)
               if song_text_array[i].get_width() > 330:
                   truncation += 1
                   truncation_string = '...'

    y = 81
    for i in range(8):
        screen.blit(song_text_array[i],(75, y+(30 * i)))

    color = ''
    if Rainbow_mode == True:
        color = text_color
    elif 8+menu_offset != len(song_array):
        color = 'orange'
    else:
        color = 'grey'

    list_count_text = font_digital.render(str(8+menu_offset)+'/'+str(len(song_array)), True, color)
    screen.blit(list_count_text,(list_text_x,list_text_y))

    playing_active = pygame.mixer.music.get_busy()
    if song_playing > -1 and playing_active == False and muted == False:
        switch_track(shuffle)
    pygame.display.update()
