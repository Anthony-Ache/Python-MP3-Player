import pygame
import os
import time
assets_folder = os.listdir('Assets/UI')
assets = {}
class menu():
    screen = pygame.display.set_mode((100, 100))
    pygame.init()
    def __init__(self, screen, name):
        self.screen = screen
        self.name = name
        for i in assets_folder:
            if '.png' in i or '.jpg' in i:
                assets[i[:-4]] = pygame.image.load('assets/UI/'+i).convert_alpha()
        self.background = assets['bg']

    def launch_menu(self):
        if 'icon' in assets:
            pygame.display.set_icon(assets['icon'])
        pygame.display.set_caption(self.name)

    def menu_loop(self):
        if 'bg' in assets:
            self.screen.blit(self.background, (0,0))

    def change_background(self, surface):
        self.background = surface

class button(menu):
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface
        self.true_surface = surface
        self.rect = self.surface.get_rect(topleft = (self.x,self.y))

    def display(self, clicked_sprite=None):
        if clicked_sprite == None:
            clicked_sprite = self.surface
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse) and pygame.mouse.get_pressed() == (True, False, False):
            self.surface = clicked_sprite
        else:
            self.surface = self.true_surface
        self.screen.blit(self.surface, (self.x, self.y))

    def cursor_flag(self, cursor_flag):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            return 'Hand'
        else:
            return cursor_flag

    def on_click(self, action, click_sound=None, returns=False):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if click_sound == None:
                click_sound = 1
            else:
                sound = pygame.mixer.Sound('Assets/Audio/' + click_sound + '.mp3')
                sound.play(0)
            if returns == True:
                return action()
            else:
                action()

    def change_sprite(self, surface):
        self.surface = surface
        self.true_surface = surface


class searchbar(menu):
    def __init__(self, surface, x, y, search_string, font, text_color='black', text_offset_x=0, text_offset_y=0, max_length = 1000, hidden=False):
        self.surface = surface
        self.x = x
        self.y = y
        self.text_offset_x = text_offset_x + self.x
        self.text_offset_y = text_offset_y + self.y
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        self.active = False
        self.initial_time = time.time()
        self.search_string = search_string
        self.text_color = text_color
        self.font = font
        self.max_length = max_length
        self.hiddenstring = ''
        self.hidden = hidden

    def backspace(self):
        if self.active == True:
            self.search_string = self.search_string.replace("|", "")
            self.search_string = self.search_string[:-1]

    def enter(self, require_active=True):
        if require_active == True:
            if self.active == True:
                self.search_string = self.search_string.replace("|", "")
                return self.search_string
        else:
            self.search_string = self.search_string.replace("|", "")
            return self.search_string

    def add_character(self, key):
        if self.active == True:
            self.search_string = self.search_string.replace("|", "")
            if len(self.search_string) < self.max_length:
                self.search_string += key

    def display(self):
        self.string_text = self.font.render(self.search_string, True, self.text_color)
        self.screen.blit(self.surface, (self.x, self.y))
        if self.hidden == False:
            self.screen.blit(self.string_text, (self.text_offset_x, self.text_offset_y))
        else:
            self.hiddenstring = ''
            for i in self.search_string:
                if i == "|":
                    self.hiddenstring += "|"
                else:
                    self.hiddenstring += '*'
            self.string_text = self.font.render(self.hiddenstring, True, self.text_color)
            self.screen.blit(self.string_text, (self.text_offset_x, self.text_offset_y))

        self.current_time = time.time()
        if self.active == True:
            if self.current_time >= self.initial_time + 1:
                if "|" in self.search_string:
                    self.search_string = self.search_string.replace("|", "")
                else:
                    self.search_string += "|"
                self.initial_time = self.current_time
        else:
            self.search_string = self.search_string.replace("|", "")

    def on_click(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.active = True
        else:
            self.active = False

    def change_sprite(self, surface):
        self.surface = surface

    def cursor_flag(self, cursor_flag):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            return 'Ibeam'
        else:
            return cursor_flag
