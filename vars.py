import pygame
import PyUI
from PyUI import assets

song_playing = -1
menu_offset = 0
song_playing_list = -1
song_length = 0
time_init = 0
temp_init = 0
temp_buffer = 0
searchboxX, searchboxY = 41, 317
seekbar_y = 320
list_text_x = 375
list_text_y = 320
play_buttonY = 75
temp_percent = 0
time_offset = 0
seekbar_x = 75
easter_color = [255, 0, 0]
play_buttons = []

text_stage = 'red'
song_playing_name = ""
search_string = ''
search_buffer = ''

looped = False
shuffle = False
muted = False
search_visable = False
Exit = False
Rainbow_mode = False

font = pygame.font.Font('Assets/UI/W95FA.otf', 22)
clock = pygame.time.Clock()
font_digital = pygame.font.Font('Assets/UI/Digital.ttf', 20)
screen = pygame.display.set_mode((450, 350))
main_menu = PyUI.menu(screen, "MP3 Player")
main_menu.launch_menu()
mute_button = PyUI.button(assets['unmuted'], 40, 25)
shuffle_button = PyUI.button(assets['unshuffled'], 90, 25)
loop_button = PyUI.button(assets['unlooped'], 140, 25)
folder_button = PyUI.button(assets['folder'], 370, 25)
restart_button = PyUI.button(assets['refresh'], 190, 25)
up_button = PyUI.button(assets['arrow_up'], 415, 80)
down_button = PyUI.button(assets['arrow_down'], 415, 290)
search_button = PyUI.button(assets['arrow_up'], 5, 317)
search_bar = PyUI.searchbar(assets['searchbox'], 41, 317, search_string, font, text_color='black', text_offset_x=34, text_offset_y=5,)
seekbar = PyUI.button(assets['seekbar'], 75,320)
