import pygame
from pygame.locals import *
import os, sys, time, math, random

pygame.init()
#==========class==================================================

class User(): # contains information that can be accessed globally
    PLAYER = None # contains player instance
    SKIN_EQUIPPED = 0
    MAP_ORIGIN = pygame.math.Vector2((0,0)) # contains map pos (0,0) in screen coordinates
    RESTART = False # True if restarting

    BACKGROUND_SURFACE = None # contains background surface of the screen

    # groups
    PLAYER_SPRITES = []
    HOOK_SPRITES = []
    TILE_SPRITES = []
    PARTICLE_SPRITES = []
    WEAPON_SPRITES = []
    INTERFACE_SPRITES = []
    ALL_SPRITES = [TILE_SPRITES, PARTICLE_SPRITES, HOOK_SPRITES, WEAPON_SPRITES, PLAYER_SPRITES, INTERFACE_SPRITES]
    ALL_UPDATES = []
    ALL_GROUPS = [x for x in ALL_SPRITES]
    ALL_GROUPS.append(ALL_UPDATES)

    class Level_Creator():
        TOOL_SELECTED = 0
        TELEPORTER_KEY = 0
        SAVE_AS_FILENAME = None

class UIEVENTHANDLER():

    @classmethod
    def instantiate_UI(cls):
        cls.SINGLEPLAYER_MENU_MAP = 0
        cls.SINGLEPLAYER_MAPS = [("Singleplayer Map 1", "single_player_long.csv"), ("Singleplayer Map Short", "single_player_map.csv"), ("Debug Map", "debug_map.csv"), ["Custom Map", None]]
        cls.DEF_FONT = pygame.font.Font(None, 48)
        cls.UI_LIST = []
        cls.EVENTS = {
            "title_screen" : cls.title_screen_event,
            "singleplayer_menu" : cls.singleplayer_menu_event,
            "singleplayer_menu_scroll_left" : cls.singleplayer_menu_scroll_left_event,
            "singleplayer_menu_scroll_right" : cls.singleplayer_menu_scroll_right_event,
            "start_singleplayer" : cls.start_singleplayer_event,
            "end_singleplayer" : cls.end_singleplayer_event,
            "singleplayer_menu_error" : cls.singleplayer_menu_error_event,
            "load_tutorial" : cls.load_tutorial_event,
            "tutorial_box" : cls.tutorial_box_event,
            "skins_menu" : cls.skins_menu_event,
            "change_skin_1" : cls.change_skin_1_event, "change_skin_2" : cls.change_skin_2_event, "change_skin_3" : cls.change_skin_3_event, "change_skin_4" : cls.change_skin_4_event, "change_skin_5" : cls.change_skin_5_event,
            "update_current_skin_image" : cls.update_current_skin_image_event,
            "load_level_creator" : cls.load_level_creator_event,
            "level_creator" : cls.level_creator_event,
            "editor_eraser" : cls.editor_erasor_event, "editor_unhook" : cls.editor_unhook_event, "editor_hook" : cls.editor_hook_event, "editor_hookthru" : cls.editor_hookthru_event, "editor_freeze": cls.editor_freeze_event,
            "editor_teleportto" : cls.editor_teleportto_event, "editor_teleportfrom" : cls.editor_teleportfrom_event, "editor_spawn" : cls.editor_spawn_event, "editor_start" : cls.editor_start_event, "editor_finish" : cls.editor_finish_event,
            "editor_kill" : cls.editor_kill_event, "editor_launcher" : cls.editor_launcher_event, "editor_remover" : cls.editor_remover_event,
            "editor_choose_teleporter_key" : cls.editor_choose_teleporter_key_event,
            "validate_teleporter_key" : cls.validate_teleporter_key_event,
            "invalid_teleporter_error" : cls.invalid_teleporter_error_event,
            "level_creator_save_menu" : cls.level_creator_save_menu_event,
            "level_creator_save_as" : cls.level_creator_save_as_event,
            "level_creator_load_menu" : cls.level_creator_load_menu_event,
            "level_creator_load_map" : cls.level_creator_load_map_event,
            "level_creator_load_error" : cls.level_creator_load_error_event,
            "end_level_creator" : cls.end_level_creator_event,
            "game" : cls.game_event,
            "game_pause" : cls.game_pause_event,
            "close_game" : cls.close_game_event,
        }

        User.ALL_UPDATES.append(cls)
        cls.handle_event("title_screen")

    @classmethod
    def handle_event(cls, event, refresh=True):
        if event != None:
            if refresh:
                cls.refresh()
            cls.EVENTS[event]()

    @classmethod
    def refresh(cls):
        for element in cls.UI_LIST[1:]:
            element.kill()
            cls.UI_LIST.pop(cls.UI_LIST.index(element))
        cls.UI_LIST = [None]

    @classmethod
    def update(cls): # for UI requiring updates
        if cls.UI_LIST[0] == None: # index 0 is UI update key
            return
        if cls.UI_LIST[0] == "game":
            cls.UI_LIST[1].clear_surface()
            cls.UI_LIST[2].update_text(str(format_time(User.PLAYER.speedrun_timer.time)))
            # debug
            cls.UI_LIST[3].clear_surface()
            #cls.UI_LIST[4].update_text("| Debug |        P to spawn Dummy")
            cls.UI_LIST[4].update_text(f"| Debug |  {len(User.ALL_UPDATES)}      ")
            cls.UI_LIST[5].update_text(f"fps: {round(FPS,0)}, playerpos: {round(get_pos(User.PLAYER.rect),1)}")
            if keys[K_ESCAPE]:
                cls.handle_event("game_pause")
        if cls.UI_LIST[0] == "singleplayer_menu":
            cls.UI_LIST[1].clear_surface()
            cls.UI_LIST[2].update_text(cls.SINGLEPLAYER_MAPS[cls.SINGLEPLAYER_MENU_MAP][0])
            if cls.SINGLEPLAYER_MENU_MAP == len(cls.SINGLEPLAYER_MAPS)-1: # if on custom map menu
                cls.SINGLEPLAYER_MAPS[-1][-1] = cls.UI_LIST[-1].text_input + ".csv" # update map file to access
                if cls.UI_LIST[-1].text_display != cls.UI_LIST[-1].default_text and cls.UI_LIST[-1].text_display[-4:] != ".map": # add .map to text display
                    cls.UI_LIST[-1].text_display += ".map" # add .map to end of text
                    cls.UI_LIST[-1].update_text_display()
        if cls.UI_LIST[0] == "level_creator_save_menu":
            User.Level_Creator.SAVE_AS_FILENAME = cls.UI_LIST[3].text_input + ".csv"
            if cls.UI_LIST[3].text_display != cls.UI_LIST[3].default_text and cls.UI_LIST[3].text_display[-4:] != ".map": # add .map to text display
                cls.UI_LIST[3].text_display += ".map" # add .map to end of text
                cls.UI_LIST[3].update_text_display()
        if cls.UI_LIST[0] == "level_creator_load_menu":
            if cls.UI_LIST[-3].text_display != cls.UI_LIST[-3].default_text and cls.UI_LIST[-3].text_display[-4:] != ".map": # add .map to text display
                cls.UI_LIST[-3].text_display += ".map" # add .map to end of text
                cls.UI_LIST[-3].update_text_display()

    # ===EVENTS===            
    @classmethod
    def title_screen_event(cls): # title screen
        User.BACKGROUND_SURFACE = create_sprite(TITLE_BACKGROUND, 750, 360, 3, sheet=False)
        title_img = Image(TITLE_IMG, 115, 69, 4, 960, 200)
        singleplayer_button = Button("Singleplayer", cls.DEF_FONT, "singleplayer_menu", 250, 75, 960, 440) # change event to start game
        multiplayer_button = Button("Multiplayer", cls.DEF_FONT, None, 240, 75, 960, 540)
        tutorial_button = Button("Tutorial", cls.DEF_FONT, "load_tutorial", 225, 75, 960, 640)
        skins_button = Button("Skins", cls.DEF_FONT, "skins_menu", 200, 75, 960, 740)
        exit_button = Button("Exit", cls.DEF_FONT, "close_game", 150, 75, 960, 840)
        accounts_button = Button("Account Login/Settings", cls.DEF_FONT, None, 400, 75, 250, 100)
        creator_button = Button("Level Creator", cls.DEF_FONT, "load_level_creator", 300, 75, 1720, 100)
        cls.UI_LIST = ["title_screen", title_img, singleplayer_button, multiplayer_button, tutorial_button, skins_button, exit_button, accounts_button, creator_button]

    @classmethod
    def singleplayer_menu_event(cls): # singleplayer menu
        cls.SINGLEPLAYER_MENU_MAP = 0
        menu_panel = Panel(400, 400, 960, 540)
        map_text = Text(cls.DEF_FONT, "Singleplayer Map", menu_panel, (menu_panel.dimensions[0]/2, 25))
        load_map_button = Button("Load Map", cls.DEF_FONT, "start_singleplayer", 200, 70, 960, 540)
        back_button = Button("Back", cls.DEF_FONT, "title_screen", 150, 75, 960, 1000)
        left_button = Button("<", cls.DEF_FONT, "singleplayer_menu_scroll_left", 50, 50, 30, 540, refresh_UI=False)
        right_button = Button(">", cls.DEF_FONT, "singleplayer_menu_scroll_right", 50, 50, 1890, 540, refresh_UI=False)
        cls.UI_LIST = ["singleplayer_menu", menu_panel, map_text, load_map_button, back_button, left_button, right_button]

    @classmethod
    def singleplayer_menu_scroll_left_event(cls): # scrolls singleplayer menu
        was_custom_menu = True if cls.SINGLEPLAYER_MENU_MAP == len(cls.SINGLEPLAYER_MAPS)-1 else False
        cls.SINGLEPLAYER_MENU_MAP -= 1
        if cls.SINGLEPLAYER_MENU_MAP < 0: cls.SINGLEPLAYER_MENU_MAP = len(cls.SINGLEPLAYER_MAPS)-1
        if cls.SINGLEPLAYER_MENU_MAP == len(cls.SINGLEPLAYER_MAPS)-1:
            text_field_test = Text_Field("Enter Map Name", cls.DEF_FONT, 300, 50, 960, 440)
            cls.UI_LIST.append(text_field_test)
        elif was_custom_menu:
            cls.UI_LIST[-1].kill()
            cls.UI_LIST.pop(-1)

    @classmethod
    def singleplayer_menu_scroll_right_event(cls): # scrolls singleplayer menu
        was_custom_menu = True if cls.SINGLEPLAYER_MENU_MAP == len(cls.SINGLEPLAYER_MAPS)-1 else False
        cls.SINGLEPLAYER_MENU_MAP += 1
        if cls.SINGLEPLAYER_MENU_MAP > len(cls.SINGLEPLAYER_MAPS)-1: cls.SINGLEPLAYER_MENU_MAP = 0
        if cls.SINGLEPLAYER_MENU_MAP == len(cls.SINGLEPLAYER_MAPS)-1:
            text_field_test = Text_Field("Enter Map Name", cls.DEF_FONT, 300, 50, 960, 440)
            cls.UI_LIST.append(text_field_test)
        elif was_custom_menu:
            cls.UI_LIST[-1].kill()
            cls.UI_LIST.pop(-1)

    @classmethod
    def start_singleplayer_event(cls): # starts up game
        try:
            load_singleplayer_map(cls.SINGLEPLAYER_MAPS[cls.SINGLEPLAYER_MENU_MAP][1])
        except: # custom map not found
            cls.handle_event("singleplayer_menu_error")

    @classmethod
    def end_singleplayer_event(cls): # end singleplayer 
        restart()
        cls.handle_event("title_screen")

    @classmethod
    def singleplayer_menu_error_event(cls): # singleplayer menu custom map not found error
        menu_panel = Panel(400, 300, 960, 540)
        error_text = Text(cls.DEF_FONT, "Error!", menu_panel, (menu_panel.dimensions[0]/2, 25))
        error_message_text = Text(cls.DEF_FONT, "Map not found.", menu_panel, (menu_panel.dimensions[0]/2, menu_panel.dimensions[1]/2))
        back_button = Button("Back", cls.DEF_FONT, "singleplayer_menu", 150, 75, 960, 1000)
        cls.UI_LIST = [None, menu_panel, error_text, error_message_text, back_button]

    "multiplayer menu stuff here pls"
    
    @classmethod
    def load_tutorial_event(cls):
        load_singleplayer_map("tutorial.csv", directory=os.path.dirname(os.path.realpath(__file__)) + "\\tutorial\\")

    @classmethod
    def tutorial_box_event(cls): # tutorial tip text box
        tutorial_text_box = Tutorial_Text_Box(600, 400, cls.DEF_FONT, 960, 540, User.PLAYER.tutorial_text)
        back_button = Button("Back", cls.DEF_FONT, "game", 150, 75, 960, 1000)
        cls.UI_LIST = [None, tutorial_text_box, back_button]

    @classmethod
    def skins_menu_event(cls): # change player skin menu
        menu_panel = Panel(700, 500, 960, 540)
        menu_text = Text(cls.DEF_FONT, "Skins Menu", menu_panel, (menu_panel.dimensions[0]/2, 25))
        skins_text = Text(cls.DEF_FONT, "Skins:", menu_panel, (100, 160))
        skin_button_1 = Button("", cls.DEF_FONT, "change_skin_1", 50, 50, 860, 450, refresh_UI=False)
        skin_button_2 = Button("", cls.DEF_FONT, "change_skin_2", 50, 50, 960, 450, refresh_UI=False)
        skin_button_3 = Button("", cls.DEF_FONT, "change_skin_3", 50, 50, 1060, 450, refresh_UI=False)
        skin_button_4 = Button("", cls.DEF_FONT, "change_skin_4", 50, 50, 1160, 450, refresh_UI=False)
        skin_button_5 = Button("", cls.DEF_FONT, "change_skin_5", 50, 50, 1260, 450, refresh_UI=False)
        skin_image_1 = Image(SKINS_SPRITESHEET, 25, 25, 1.5, 860, 450, sheet=True, frame=0)
        skin_image_2 = Image(SKINS_SPRITESHEET, 25, 25, 1.5, 960, 450, sheet=True, frame=1)
        skin_image_3 = Image(SKINS_SPRITESHEET, 25, 25, 1.5, 1060, 450, sheet=True, frame=2)
        skin_image_4 = Image(SKINS_SPRITESHEET, 25, 25, 1.5, 1160, 450, sheet=True, frame=3)
        skin_image_5 = Image(SKINS_SPRITESHEET, 25, 25, 1.5, 1260, 450, sheet=True, frame=4)
        current_skin_text = Text(cls.DEF_FONT, "Current Skin:", menu_panel, (150, 360))
        current_skin_image = Image(SKINS_SPRITESHEET, 25, 25, 5, 1060, 650, sheet=True, frame=User.SKIN_EQUIPPED)
        back_button = Button("Back", cls.DEF_FONT, "title_screen", 150, 75, 960, 1000)
        cls.UI_LIST = [None, menu_panel, menu_text, skins_text, skin_button_1, skin_image_1, skin_button_2, skin_image_2, skin_button_3, skin_image_3, skin_button_4, skin_image_4, skin_button_5, skin_image_5, current_skin_text, current_skin_image, back_button]

    @classmethod
    def change_skin_1_event(cls): # change skin
        User.SKIN_EQUIPPED = 0
        cls.handle_event("update_current_skin_image", refresh=False)
    
    @classmethod
    def change_skin_2_event(cls):
        User.SKIN_EQUIPPED = 1
        cls.handle_event("update_current_skin_image", refresh=False)
    
    @classmethod
    def change_skin_3_event(cls):
        User.SKIN_EQUIPPED = 2
        cls.handle_event("update_current_skin_image", refresh=False)
    
    @classmethod
    def change_skin_4_event(cls):
        User.SKIN_EQUIPPED = 3
        cls.handle_event("update_current_skin_image", refresh=False)
    
    @classmethod
    def change_skin_5_event(cls):
        User.SKIN_EQUIPPED = 4
        cls.handle_event("update_current_skin_image", refresh=False)

    @classmethod
    def update_current_skin_image_event(cls):
        current_skin_image = Image(SKINS_SPRITESHEET, 25, 25, 5, 1060, 650, sheet=True, frame=User.SKIN_EQUIPPED)
        cls.UI_LIST[-2].kill()
        cls.UI_LIST[-2] = current_skin_image

    @classmethod
    def load_level_creator_event(cls):
        load_level_creator()
        User.BACKGROUND_SURFACE = create_sprite(IN_GAME_BACKGROUND, 750, 360, 3, sheet=False)
        cls.handle_event("level_creator")

    @classmethod
    def level_creator_event(cls):
        title_panel = Panel(300,100,960,125)
        title_text = Text(cls.DEF_FONT, "Level Creator", title_panel, (title_panel.dimensions[0]/2, title_panel.dimensions[1]/2))
        taskbar_panel = Panel(1800,200,960,980)
        usability_text_1 = Text(cls.DEF_FONT, "Use WASD", taskbar_panel, (100,62))
        usability_text_2 = Text(cls.DEF_FONT, "to move", taskbar_panel, (100,97))
        usability_text_3 = Text(cls.DEF_FONT, "the camera!", taskbar_panel, (100,132))
        eraser_button = Button("Eraser", cls.DEF_FONT, "editor_eraser", 125, 125, 350, 980, refresh_UI=False)
        unhook_button, unhook_image = Button("", cls.DEF_FONT, "editor_unhook", 75, 75, 475, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 475, 980, sheet=True, frame=0)
        hook_button, hook_image = Button("", cls.DEF_FONT, "editor_hook", 75, 75, 550, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 550, 980, sheet=True, frame=1)
        hook_through_button, hook_through_image = Button("", cls.DEF_FONT, "editor_hookthru", 75, 75, 625, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 625, 980, sheet=True, frame=2)
        freeze_button = Button("F", cls.DEF_FONT, "editor_freeze", 75, 75, 700, 980, refresh_UI=False)
        teleporter_to_button = Button("T", cls.DEF_FONT, "editor_teleportto", 75, 75, 775, 980, refresh_UI=False)
        teleporter_from_button, teleporter_from_image = Button("", cls.DEF_FONT, "editor_teleportfrom", 75, 75, 850, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 850, 980, sheet=True, frame=5)
        spawn_point_button, spawn_point_image = Button("", cls.DEF_FONT, "editor_spawn", 75, 75, 925, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 925, 980, sheet=True, frame=6)
        kill_button, kill_image = Button("", cls.DEF_FONT, "editor_kill", 75, 75, 1000, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 1000, 980, sheet=True, frame=9)
        start_button, start_image = Button("", cls.DEF_FONT, "editor_start", 75, 75, 1075, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 1075, 980, sheet=True, frame=7)
        finish_button, finish_image = Button("", cls.DEF_FONT, "editor_finish", 75, 75, 1150, 980, refresh_UI=False), Image(TILE_SPRITESHEET, 20, 20, 2, 1150, 980, sheet=True, frame=8)
        launcher_button, launcher_image = Button("", cls.DEF_FONT, "editor_launcher", 75, 75, 1225, 980, refresh_UI=False), Image(WEAPONS_SPRITESHEET, 36, 10, 1.25, 1225, 980, sheet=True, frame=1)
        remover_button, remover_image = Button("", cls.DEF_FONT, "editor_remover", 75, 75, 1300, 980, refresh_UI=False), Image(CLOUD, 9, 7, 5, 1300, 980)
        save_as_button = Button("Save As", cls.DEF_FONT, "level_creator_save_menu", 150, 75, 1450, 980)
        load_button = Button("Load", cls.DEF_FONT, "level_creator_load_menu", 100, 75, 1600, 980)
        back_button = Button("Back", cls.DEF_FONT, "end_level_creator", 125, 75, 1750, 980)
        cls.UI_LIST = ["level_creator", title_panel, title_text, taskbar_panel, usability_text_1, usability_text_2, usability_text_3, load_button, eraser_button, save_as_button, back_button, unhook_button, unhook_image, hook_button, hook_image, hook_through_button, hook_through_image, freeze_button, teleporter_to_button, teleporter_from_button, teleporter_from_image, spawn_point_button, spawn_point_image, kill_button, kill_image, start_button, start_image, finish_button, finish_image, launcher_button, launcher_image, remover_button, remover_image]

    @classmethod
    def editor_choose_teleporter_key_event(cls):
        menu_panel = Panel(650,400,960,540)
        menu_text = Text(cls.DEF_FONT, "Choose a teleporter key (1-16)", menu_panel, (menu_panel.dimensions[0]/2, 25))
        teleporter_field = Text_Field("Key:", cls.DEF_FONT, 125, 75, 960, 540)
        teleporter_button = Button("Enter", cls.DEF_FONT, "validate_teleporter_key", 150, 75, 960, 650, refresh_UI=False)
        cls.UI_LIST = [None, menu_panel, menu_text, teleporter_field, teleporter_button]

    @classmethod
    def validate_teleporter_key_event(cls):
        try:
            if int(cls.UI_LIST[3].text_input) not in range(1,17):
                cls.handle_event("invalid_teleporter_error")
            else:
                User.Level_Creator.TELEPORTER_KEY = int(cls.UI_LIST[3].text_input)-1
                cls.handle_event("level_creator")
        except:
            cls.handle_event("invalid_teleporter_error")

    @classmethod
    def invalid_teleporter_error_event(cls):
        menu_panel = Panel(400, 300, 960, 540)
        error_text = Text(cls.DEF_FONT, "Error!", menu_panel, (menu_panel.dimensions[0]/2, 25))
        error_message_text = Text(cls.DEF_FONT, "Key invalid (1-16).", menu_panel, (menu_panel.dimensions[0]/2, menu_panel.dimensions[1]/2))
        back_button = Button("Back", cls.DEF_FONT, "level_creator", 150, 75, 960, 1000)
        cls.UI_LIST = [None, menu_panel, error_text, error_message_text, back_button]

    @classmethod
    def editor_erasor_event(cls):
        User.Level_Creator.TOOL_SELECTED = 0
    
    @classmethod
    def editor_unhook_event(cls):
        User.Level_Creator.TOOL_SELECTED = 1

    @classmethod
    def editor_hook_event(cls):
        User.Level_Creator.TOOL_SELECTED = 2

    @classmethod
    def editor_hookthru_event(cls):
        User.Level_Creator.TOOL_SELECTED = 3

    @classmethod
    def editor_freeze_event(cls):
        User.Level_Creator.TOOL_SELECTED = 4

    @classmethod
    def editor_teleportto_event(cls):
        cls.handle_event("editor_choose_teleporter_key")
        User.Level_Creator.TOOL_SELECTED = 5

    @classmethod
    def editor_teleportfrom_event(cls):
        cls.handle_event("editor_choose_teleporter_key")
        User.Level_Creator.TOOL_SELECTED = 6

    @classmethod
    def editor_spawn_event(cls):
        User.Level_Creator.TOOL_SELECTED = 7

    @classmethod
    def editor_start_event(cls):
        User.Level_Creator.TOOL_SELECTED = 8

    @classmethod
    def editor_finish_event(cls):
        User.Level_Creator.TOOL_SELECTED = 9

    @classmethod
    def editor_kill_event(cls):
        User.Level_Creator.TOOL_SELECTED = 10

    @classmethod
    def editor_launcher_event(cls):
        User.Level_Creator.TOOL_SELECTED = 11

    @classmethod
    def editor_remover_event(cls):
        User.Level_Creator.TOOL_SELECTED = 12

    @classmethod
    def level_creator_save_menu_event(cls):
        menu_panel = Panel(400, 400, 960, 540)
        map_text = Text(cls.DEF_FONT, "Choose map name", menu_panel, (menu_panel.dimensions[0]/2, 25))
        save_map_button = Button("Save Map", cls.DEF_FONT, "level_creator_save_as", 200, 70, 960, 540)
        map_text_field = Text_Field("Enter Map Name", cls.DEF_FONT, 300, 50, 960, 440)
        back_button = Button("Back", cls.DEF_FONT, "level_creator", 150, 75, 960, 1000)
        cls.UI_LIST = ["level_creator_save_menu", menu_panel, map_text, map_text_field, save_map_button, back_button]

    @classmethod
    def level_creator_save_as_event(cls):
        file_from_map(User.Level_Creator.SAVE_AS_FILENAME)
        restart()
        cls.handle_event("title_screen")

    @classmethod
    def level_creator_load_menu_event(cls):
        menu_panel = Panel(650,400,960,540)
        menu_text = Text(cls.DEF_FONT, "Enter custom map name", menu_panel, (menu_panel.dimensions[0]/2, 25))
        map_field = Text_Field("Enter map...", cls.DEF_FONT, 200, 75, 960, 540)
        load_button = Button("Load", cls.DEF_FONT, "level_creator_load_map", 150, 75, 960, 650, refresh_UI=False)
        back_button = Button("Back", cls.DEF_FONT, "level_creator", 150, 75, 960, 1000)
        cls.UI_LIST = ["level_creator_load_menu", menu_panel, menu_text, map_field, load_button, back_button]

    @classmethod
    def level_creator_load_map_event(cls):
        try:
            tutorial_create_map(cls.UI_LIST[-3].text_input + ".csv")
            cls.handle_event("level_creator")
        except:
            cls.handle_event("level_creator_load_error")

    @classmethod
    def level_creator_load_error_event(cls):
        menu_panel = Panel(400, 300, 960, 540)
        error_text = Text(cls.DEF_FONT, "Error!", menu_panel, (menu_panel.dimensions[0]/2, 25))
        error_message_text = Text(cls.DEF_FONT, "Map not found.", menu_panel, (menu_panel.dimensions[0]/2, menu_panel.dimensions[1]/2))
        back_button = Button("Back", cls.DEF_FONT, "level_creator", 150, 75, 960, 1000)
        cls.UI_LIST = [None, menu_panel, error_text, error_message_text, back_button]

    @classmethod
    def end_level_creator_event(cls):
        restart()
        cls.handle_event("title_screen")

    @classmethod
    def game_event(cls): # in-game UI
        User.BACKGROUND_SURFACE = create_sprite(IN_GAME_BACKGROUND, 750, 360, 3, sheet=False)
        try:
            User.PLAYER.paused = False
        except:
            pass # player not instantiated yet
        time_panel = Panel(200, 50, 960, 50)
        time_text = Text(cls.DEF_FONT, "00:00:00", time_panel, (time_panel.dimensions[0]/2, time_panel.dimensions[1]/2))

        # debug
        debug_panel = Panel(700,100, 1570, 1030)
        debug_text_1 = Text(cls.DEF_FONT, "debug!", debug_panel, (0,0), centered=False)
        debug_text_2 = Text(cls.DEF_FONT, "debug!", debug_panel, (0,50), centered=False)

        cls.UI_LIST = ["game", time_panel, time_text, debug_panel, debug_text_1, debug_text_2]

    @classmethod
    def game_pause_event(cls): # in-game paused
        User.PLAYER.paused = True
        menu_panel = Panel(350, 350, 960, 540)
        resume_button = Button("Resume", UIEVENTHANDLER.DEF_FONT, "game", 200, 75, 960, 440)
        menu_button = Button("Main Menu", UIEVENTHANDLER.DEF_FONT, "end_singleplayer", 200, 75, 960, 540)
        exit_button = Button("Exit Game", UIEVENTHANDLER.DEF_FONT, "close_game", 200, 75, 960, 640)
        cls.UI_LIST = [None, menu_panel, resume_button, menu_button, exit_button]
    
    @classmethod
    def close_game_event(cls): # close the game
        pygame.quit()
        sys.exit()

class Panel():

    AFFECTED_BY_CAMERA = False

    def __init__(self, width, height, x, y):
        self.dimensions = (width,height)
        self.clear_surface()
        self.rect = self.surface.get_rect()
        self.rect.center = (x,y)
        User.INTERFACE_SPRITES.append(self)

    def clear_surface(self, opacity=200):
        self.surface = pygame.surface.Surface(self.dimensions, pygame.SRCALPHA).convert_alpha()
        self.surface.set_alpha(opacity)
        self.surface.fill((0,0,0,200))
    
    def kill(self):
        User.INTERFACE_SPRITES.pop(User.INTERFACE_SPRITES.index(self))
        del self

class Button():

    AFFECTED_BY_CAMERA = False

    def __init__(self, text, font, type, width, height, x, y, refresh_UI=True):
        self.panel = Panel(width, height, x, y)
        self.text = Text(font, text, self.panel, (self.panel.dimensions[0]/2, self.panel.dimensions[1]/2))
        self.type = type
        self.pressed_last_frame = False
        self.refresh_UI = refresh_UI
        User.ALL_UPDATES.append(self)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if Rect(mouse_pos[0], mouse_pos[1], 1, 1).colliderect(self.panel):
            self.update_panel(opacity=225)
            if mouseup == 1 and self.pressed_last_frame: 
                UIEVENTHANDLER.handle_event(self.type, refresh=self.refresh_UI)
            if pygame.mouse.get_pressed()[0]:
                self.update_panel(opacity=255)
                self.pressed_last_frame = True
            else:
                self.pressed_last_frame = False
        else:
            self.update_panel()
    
    def update_panel(self, opacity=200):
        self.panel.clear_surface(opacity=opacity)
        self.panel.surface.blit(self.text.surface, self.text.rect)
    
    def kill(self):
        self.panel.kill()
        self.text.kill()
        User.ALL_UPDATES.pop(User.ALL_UPDATES.index(self))
        del self


class Text():

    AFFECTED_BY_CAMERA = False
    
    def __init__(self, font, text, panel, pos, centered=True):
        self.font = font
        self.text = text
        self.panel = panel
        self.pos = pos
        self.centered = centered
        self.update_text(self.text)

    def update_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, True, (255,255,255))
        self.rect = self.surface.get_rect()
        if self.centered:
            self.rect.center = self.pos
        else:
            self.rect.topleft = self.pos
        if self.rect.width > self.panel.rect.width: self.rect.right -= self.rect.width-self.panel.rect.width # if text wider than panel -> scroll
        self.panel.surface.blit(self.surface, self.rect)
    
    def kill(self):
        del self

class Text_Field():

    AFFECTED_BY_CAMERA = False

    def __init__(self, default_text, font, width, height, x, y):
        self.panel = Panel(width, height, x, y)
        self.text = Text(font, default_text, self.panel, (5,self.panel.dimensions[1]/4), centered=False)
        self.default_text = default_text
        self.text_display = default_text
        self.text_input = ""
        self.selected = False
        User.ALL_UPDATES.append(self)
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if mousedown == 1:
            if Rect(mouse_pos[0], mouse_pos[1], 1, 1).colliderect(self.panel):
                self.selected = True
            else:
                self.selected = False

        if keydown_unicode and self.selected: # if typing and textbox selected
            self.text_display = self.default_text # set to default text
            if keydown_unicode.isalnum() or keydown_unicode in ("(", ")", ",", ".", "-", "_", "*"): self.text_input += keydown_unicode # validate
            if keydown == K_BACKSPACE: self.text_input = self.text_input[:-1] # backspace key
            if self.text_input != "": self.text_display = self.text_input # change text display if text input not empty
        self.update_text_display()
    
    def update_text_display(self):
        if self.selected:
            self.panel.clear_surface(opacity=225)
        else:
            self.panel.clear_surface()
        self.text.update_text(self.text_display)

    def kill(self):
        User.ALL_UPDATES.pop(User.ALL_UPDATES.index(self))
        self.panel.kill()
        self.text.kill()
        del self

class Image():

    AFFECTED_BY_CAMERA = False

    def __init__(self, img, width, height, scale, x, y, sheet=False, frame=None):
        self.surface = create_sprite(img, width, height, scale, opacity=255, sheet=sheet, frame=frame)
        self.rect = self.surface.get_rect()
        self.rect.center = (x,y)
        User.INTERFACE_SPRITES.append(self)
    
    def kill(self):
        User.INTERFACE_SPRITES.pop(User.INTERFACE_SPRITES.index(self))
        del self

class Tutorial_Text_Box():

    def __init__(self, width, height, font, x, y, type): # type = number corresponding to text from file
        self.panel = Panel(width, height, x, y)
        self.title_text = Text(UIEVENTHANDLER.DEF_FONT, "Tutorial", self.panel, (self.panel.dimensions[0]/2, 50))
        self.tutorial_text = []
        self.type = type
        self.font = font
        self.fill_text()
    
    def fill_text(self):
        file_path = os.path.dirname(os.path.realpath(__file__)) + f"\\tutorial\\tutorial_text.txt"
        with open(file_path, "r") as file:
            current_text_type = 0 # contains current iteration of text box text
            completed = False
            text_y_pos = 100
            file_lines_list = [x.strip() for x in file.readlines()]
            for line in file_lines_list:
                if current_text_type == self.type and line != ".":
                    completed = True
                    self.tutorial_text.append(Text(UIEVENTHANDLER.DEF_FONT, line, self.panel, (50, text_y_pos), centered=False))
                    text_y_pos += 35
                if current_text_type != self.type and completed: break
                if line == ".": current_text_type += 1
    
    def kill(self):
        self.panel.kill()
        for text in self.tutorial_text:
            text.kill()
        del self

# contains methods for weapons to inherit
class Weapon():

    # rotate image to any angle    
    def rotate(self, angle, flip=False):
        rotation_angle = angle
        rotation_surface = self.default_surface.copy()
        if flip:
            rotation_surface = pygame.transform.flip(self.default_surface.copy(), True, False) # flip on x=True, y=False
            rotation_angle = -(180 - angle)
        self.surface = pygame.transform.rotate(rotation_surface, rotation_angle)
        self.current_angle = angle
        copy_rect = self.rect.copy()
        self.rect = self.surface.get_rect()
        self.rect.center = copy_rect.center

    def angle_to_mouse(self):
        return get_angle(pygame.mouse.get_pos()[0]-self.player.rect.center[0], pygame.mouse.get_pos()[1]-self.player.rect.center[1])
    
    def kill(self):
        User.WEAPON_SPRITES.pop(User.WEAPON_SPRITES.index(self))
        User.ALL_UPDATES.pop(User.ALL_UPDATES.index(self))
        del self

class Player():

    class Hook():

        class Chain():

            def __init__(self, spawn_point, angle, hook):
                # important
                self.surface = create_sprite(HOOK_WRAP, 8, 7, 2.5, opacity=255)
                self.surface = pygame.transform.rotate(self.surface, angle)
                self.rect = self.surface.get_rect()
                self.rect.center = spawn_point
                self.hook = hook

                User.HOOK_SPRITES.insert(0, self)           

            def kill(self):
                User.HOOK_SPRITES.pop(User.HOOK_SPRITES.index(self))
                self.hook.chains.pop(self.hook.chains.index(self))
                del self

        def __init__(self, player):

            # important
            self.player = player
            self.default_surface = create_sprite(HOOK_HEAD, 12, 9, 2.5, opacity=255)
            self.surface = self.default_surface.copy()
            self.rect = self.surface.get_rect()
            self.rect.center = self.player.rect.center
            self.origin = self.rect.center

            # physics constants
            self.speed = 50

            # other
            self.life_timer = Timer(0.12)
            self.initial_mouse = pygame.math.Vector2((pygame.mouse.get_pos()))
            self.chains = []
            self.attached = False
            self.frames_alive = 0

            # add to groups
            User.HOOK_SPRITES.insert(0, self)
            User.ALL_UPDATES.append(self)

            # set initial movement vector and angle
            self.angle = self.update_hook_direction()
            self.update_rotation()

        def update(self):
            self.frames_alive += 1
            self.update_hook_direction()

            # check if collided [experimental]
            if not self.attached:
                for tile in User.TILE_SPRITES:
                    if tile.rect.colliderect(self.rect.x + self.movement_vector.x, self.rect.y, 1, 1):
                        if tile.tile == 1:
                            self.kill()
                            return
                        if tile.tile == 2:
                            self.attached = True
                            if self.movement_vector.x > 0:
                                self.rect.right = tile.rect.left + 10
                            if self.movement_vector.x < 0:
                                self.rect.left = tile.rect.right - 10
                            break
                    
                    if tile.rect.colliderect(self.rect.x, self.rect.y + self.movement_vector.y, 1, 1):
                        if tile.tile == 1:
                            self.kill()
                            return
                        if tile.tile == 2:
                            self.attached = True
                            if self.movement_vector.y > 0:
                                self.rect.bottom = tile.rect.top + 10
                            if self.movement_vector.y < 0:
                                self.rect.top = tile.rect.bottom - 10
                            break

            # move hook head towards target
            if not self.attached:
                self.rect.center = self.player.rect.center + self.movement_vector*self.frames_alive

                # move points within world
                offset = pygame.Vector2((width/2, height/2)) - self.player.rect.center
                self.initial_mouse += offset
                self.origin += offset

                # update mouse position in world + movement vector + rotate head
                self.player.hooking = False
            else:
                self.player.hook_vector = self.get_player_hook_vector()
                self.movement_vector = pygame.math.Vector2((0,0))
                self.player.hooking = True

            # update rotation of the hook
            self.update_rotation()

            # clear current chain
            self.kill_chain()

            # create new chain given hook and player positions
            chain_vector = pygame.math.Vector2((16,0)).rotate(-self.angle)
            connected_to_player = False
            total_chains = 0

            # loop creates chain until player
            while not connected_to_player:
                total_chains += 1
                spawn = self.rect.center - total_chains*chain_vector
                self.chains.append(self.Chain(spawn, self.angle, self))
                if pygame.math.Vector2((self.chains[-1].rect.center)).distance_to(pygame.math.Vector2((self.player.rect.center))) < 32 or total_chains > 1000: # chain limit to stop crashing
                    connected_to_player = True

            # restrict length
            if self.life_timer.complete and not self.attached:
                self.kill()
        
        # i hate this code
        def update_hook_direction(self):
            dx, dy = self.initial_mouse.x - self.origin[0], self.initial_mouse.y - self.origin[1]
            angle = get_angle(dx,dy)
            self.movement_vector = pygame.math.Vector2((self.speed,0)).rotate(-angle) * 75 * delta_time
            return angle

        def get_player_hook_vector(self):
            dx, dy = self.rect.center[0] - self.player.rect.center[0], self.rect.center[1] - self.player.rect.center[1]
            angle = get_angle(dx,dy)
            movement_vector = pygame.math.Vector2((self.speed,0)).rotate(-angle) * 75 * delta_time
            return movement_vector

        def update_rotation(self):
            dx, dy = self.rect.center[0] - self.player.rect.center[0], self.rect.center[1] - self.player.rect.center[1]
            self.angle = get_angle(dx,dy)
            self.surface = create_sprite(HOOK_HEAD, 12, 9, 2.5, opacity=255)
            copy_rect = self.rect.copy()
            self.surface = pygame.transform.rotate(self.surface, self.angle)
            self.rect = self.surface.get_rect()
            self.rect.center = copy_rect.center

        def kill(self):
            self.life_timer.kill()
            self.kill_chain()
            User.ALL_UPDATES.pop(User.ALL_UPDATES.index(self))
            User.HOOK_SPRITES.pop(User.HOOK_SPRITES.index(self))
            self.player.hook = None
            self.player.hooking = False
            del self

        def kill_chain(self):
            while len(self.chains) != 0:
                self.chains[-1].kill()

    class Grenade_Launcher(Weapon):

        class Grenade(Weapon):

            def __init__(self, player, launcher, angle, facing_right):
                # important
                self.launcher = launcher
                self.player = player
                self.surface = create_sprite(PROJECTILES_SPRITESHEET, 8, 8, 2.5, sheet=True, frame=0, opacity=255)
                self.rect = self.surface.get_rect()
                
                # determine spawn point
                pre_vector_spawn = pygame.math.Vector2((self.player.rect.center)) + pygame.math.Vector2((self.launcher.OFFSET_X if facing_right else -self.launcher.OFFSET_X,0))
                vector = pygame.math.Vector2((36,0)).rotate(-angle)
                self.rect.center = pre_vector_spawn + vector
                self.vel = pygame.math.Vector2((20,0)).rotate(-angle)

                # other attributes
                self.life_timer = Timer(2)
                self.trail_timer = Timer(0.25)

                # add to groups
                User.WEAPON_SPRITES.append(self)
                User.ALL_UPDATES.append(self)

            def update(self):
                # update position
                self.vel.y += self.player.GRAVITY_ACC * PHYSICS_MULTIPLIER
                self.rect.center += self.vel * PHYSICS_MULTIPLIER

                if self.life_timer.complete:
                    self.explode()
                    return

                # collision detection
                for tile in User.TILE_SPRITES:
                    if tile.rect.colliderect(self.rect.x + self.vel.x, self.rect.y + self.vel.y, self.rect.width, self.rect.height):
                        if tile.tile in (1,2,3):
                            self.explode()
                            return
                # spawn trail
                if self.trail_timer.complete:
                    self.trail_timer.kill()
                    self.trail_timer = Timer(0.25)

            def explode(self):
                Particle(self.rect.center, type="explosion") # explosion
                if self.life_timer != None: self.life_timer.kill()
                if self.trail_timer != None: self.trail_timer.kill()

                # apply speed to nearby players
                for player in User.PLAYER_SPRITES:
                    dx = player.rect.center[0] - self.rect.center[0]
                    dy = player.rect.center[1] - self.rect.center[1]
                    distance = pygame.math.Vector2((dx,dy)).length()
                    if distance < 10: distance = 10
                    if distance < 250:
                        angle = get_angle(dx,dy)
                        player.external_vel += pygame.math.Vector2((200/(distance//10), 0)).rotate(-angle) * PHYSICS_MULTIPLIER

                self.kill()

        AFFECTED_BY_CAMERA = False # centered on player
        OFFSET_X = 35 # offset from player center

        def __init__(self, player):
            # important
            self.player = player
            self.default_surface = create_sprite(WEAPONS_SPRITESHEET, 36, 10, 2.5, sheet=True, frame=1, opacity=255)
            self.surface = self.default_surface
            self.rect = self.surface.get_rect()
            self.rect.center = self.player.rect.center
            self.rect.x += self.OFFSET_X

            # other attributes
            self.facing_right = True
            
            # rotate launcher
            self.check_for_flip()
            self.rotate(self.angle_to_mouse(), flip=False if self.facing_right else True)

            # add to groups
            User.WEAPON_SPRITES.append(self)
            User.ALL_UPDATES.append(self)

        def update(self):
            angle = self.angle_to_mouse()
            self.check_for_flip()
            self.rotate(angle, flip=False if self.facing_right else True)

            # spawn grenade
            if pygame.mouse.get_pressed()[0] and self.player.launcher_cooldown_timer.complete and not self.player.frozen and not self.player.paused:
                self.Grenade(self.player, self, angle, self.facing_right)
                self.player.launcher_cooldown_timer.kill()
                self.player.launcher_cooldown_timer = Timer(0.5)

        # rotate around player
        def check_for_flip(self):
            aiming_right = pygame.mouse.get_pos()[0] > self.player.rect.center[0]

            if not aiming_right:
                if self.facing_right:
                    self.rotate(self.angle_to_mouse())
                    self.rect.x -= 2*self.OFFSET_X
                self.facing_right = False
            elif aiming_right:
                if not self.facing_right:
                    self.rotate(self.angle_to_mouse(), flip=True)
                    self.rect.x += 2*self.OFFSET_X
                self.facing_right = True

    class Bat(Weapon):

        BAT_X_SPEED = 5
        BAT_Y_SPEED = -7
        BAT_SPEED_MULTIPLER = 1.5

        SWING_SPEED = 10 # degrees per frame [at target FPS]
        MAX_SWING_ANGLE_OFFSET = 90
        DEF_ANGLE = 68 # angle when idle
        OFFSET = (50,-35) # pixel offset on x and y from player center

        AFFECTED_BY_CAMERA = False # centered on player

        def __init__(self, player):
            # important
            self.player = player
            self.default_surface = create_sprite(WEAPONS_SPRITESHEET, 36, 10, 2.5, sheet=True, frame=0, opacity=255)
            self.surface = pygame.transform.rotate(self.default_surface.copy(), self.DEF_ANGLE)
            self.rect = self.surface.get_rect()
            self.rect.center = self.player.rect.center
            self.rect.center += pygame.math.Vector2((self.OFFSET[0], self.OFFSET[1]))

            # other attributes
            self.facing_right = True
            self.swinging = None
            self.hit_count = 0 # collisions per 1 swing
            self.current_angle = self.DEF_ANGLE

            # add to groups
            User.WEAPON_SPRITES.append(self)
            User.ALL_UPDATES.append(self)

        def update(self):

            # SWING
            if not self.swinging:
                self.hit_count = 0
                self.rotate_bat()
                if mousedown == 1 and not self.player.frozen and not self.player.paused:
                    self.swinging = "forwards"
            elif self.swinging == "forwards": # swinging
                angle_offset = -(self.SWING_SPEED * PHYSICS_MULTIPLIER) if self.facing_right else (self.SWING_SPEED * PHYSICS_MULTIPLIER)
                self.rotate(self.current_angle + angle_offset)
                if self.facing_right:
                    if self.current_angle < self.DEF_ANGLE-self.MAX_SWING_ANGLE_OFFSET:
                        self.swinging = "backwards"
                elif self.current_angle > (180-self.DEF_ANGLE)+self.MAX_SWING_ANGLE_OFFSET:
                    self.swinging = "backwards"
            elif self.swinging == "backwards": # retracting
                angle_offset = 2*(self.SWING_SPEED * PHYSICS_MULTIPLIER) if self.facing_right else -2*(self.SWING_SPEED * PHYSICS_MULTIPLIER) # comes back 2x as fast
                self.rotate(self.current_angle + angle_offset)
                if self.facing_right:
                    if self.current_angle > self.DEF_ANGLE:
                        self.swinging = None
                elif self.current_angle < (180-self.DEF_ANGLE):
                    self.swinging = None

            # SWING COLLIDE
            if self.hit_count < 1:
                for player_sprite in User.PLAYER_SPRITES:
                    if self.swinging == "forwards" and self.rect.colliderect(player_sprite.rect) and player_sprite != self.player:
                        self.hit_count += 1
                        player_sprite.grounded = False
                        player_sprite.external_vel.y = self.BAT_Y_SPEED * PHYSICS_MULTIPLIER # why is this so messed up
                        if -5 < player_sprite.external_vel.x < 5:
                            if self.facing_right:
                                player_sprite.external_vel.x += self.BAT_X_SPEED * PHYSICS_MULTIPLIER
                            else:
                                player_sprite.external_vel.x -= self.BAT_X_SPEED * PHYSICS_MULTIPLIER
                        else:
                            player_sprite.external_vel *= self.BAT_SPEED_MULTIPLER
                for weapon_sprite in User.WEAPON_SPRITES:
                    if type(weapon_sprite) == self.player.Grenade_Launcher.Grenade:
                        if self.swinging == "forwards" and self.rect.colliderect(weapon_sprite.rect):
                            weapon_sprite.explode()

        # rotation of bat
        def rotate_bat(self):
            aiming_right = pygame.mouse.get_pos()[0] > self.player.rect.center[0]

            if not aiming_right:
                if self.facing_right:
                    self.rotate(180-self.DEF_ANGLE)
                    self.rect.x -= 2*self.OFFSET[0]
                self.facing_right = False
                if self.current_angle != 180-self.DEF_ANGLE:
                    self.rotate(180-self.DEF_ANGLE)
            elif aiming_right:
                if not self.facing_right:
                    self.rotate(self.DEF_ANGLE)
                    self.rect.x += 2*self.OFFSET[0]
                self.facing_right = True
                if self.current_angle != self.DEF_ANGLE:
                    self.rotate(self.DEF_ANGLE)

    # PLAYER CLASS CONSTANTS
    # forces
    WALK_VEL = 7
    HOOK_ACC = 1.5
    GRAVITY_ACC = 0.5
    JUMP_VEL = -17    

    # limits
    TOTAL_VEL_LIMIT = 32.5

    # hook pull multipliers
    HOOK_PULL_WEAK = 0.5
    HOOK_PULL_STRONG = 1.5

    # friction
    FRICTION_WALK_GROUND = 0.5
    FRICTION_WALK_AIR = 0.05
    FRICTION_HOOK_GROUND_1 = 0.1 # walk in same direction
    FRICTION_HOOK_GROUND_2 = 0.25 # not walking
    FRICTION_HOOK_AIR_1 = 0.01 # walk in same direction as hook
    FRICTION_HOOK_AIR_2 = 0.065 # walk in opposite direction as hook

    def __init__(self, skin_frame):
        # frozen/unfrozen skin
        self.unfrozen_skin = create_sprite(SKINS_SPRITESHEET, 25, 25, 2.5, sheet=True, frame=skin_frame, opacity=255)
        self.frozen_skin = create_sprite(SKINS_SPRITESHEET, 25, 25, 2.5, sheet=True, frame=skin_frame, opacity=125)

        # important
        self.surface = self.unfrozen_skin
        self.rect = self.surface.get_rect()
        self.rect.center = pygame.math.Vector2((width/2,height/2))
        self.pos_obj = Pos(self.rect.center, self.rect.width/2)

        # hook-related
        self.hook_vector = pygame.math.Vector2((0,0)) # attribute updated by Hook class
        self.hook = None # contains hook instance
        self.hooking = False # bool if hook instance alive
        
        # equipment
        self.weapon = self.Bat(self)
        self.launcher_owned = False
        self.launcher_cooldown_timer = Timer(0.5)

        # main velocities
        self.total_vel = pygame.math.Vector2((0,0)) # total velocity
        self.base_vel = pygame.math.Vector2((0,0)) # base movement velocity
        self.hook_vel = pygame.math.Vector2((0,0)) # hook movement velocity
        self.external_vel = pygame.math.Vector2((0,0)) # velocity from environment
        self.velocities = (self.total_vel, self.hook_vel, self.base_vel, self.external_vel)

        # other attributes
        self.paused = False
        self.jump_count = 1
        self.jumps_count_last_frame = 1
        self.grounded = False
        self.frozen = False
        self.tutorial_boxes_read = [False for i in range(0,10)]
        self.walk_vel_list = [] # contains different walk speeds at different framerates during runtime
        self.speedrun_timer = Speedrun_Timer()
        self.trail_timer = Timer(0) # timer between trail effects
        self.freeze_timer = Timer(0) # timer until unfrozen

        # spawn at spawn point
        dx, dy = self.get_random_tile_offset(7)
        self.rect.center += pygame.math.Vector2((dx,dy))
        self.pos_obj.center += pygame.math.Vector2((dx,dy))

        # update groups
        User.PLAYER_SPRITES.append(self)
        User.ALL_UPDATES.append(self)

    
    def update(self):
        # determine physical values
        mean_walk_vel = self.calculate_mean_walk_velocity()
        x_friction, x_hook_friction = self.calculate_friction()

        # update frozen state
        if self.freeze_timer != None:
            if self.freeze_timer.complete:
                self.freeze_timer = self.freeze_timer.kill() # (returns None)
                self.unfreeze()
        else:
            self.unfreeze()

        # GRAVITY
        if not self.grounded:
            self.hook_vel.y += self.GRAVITY_ACC * PHYSICS_MULTIPLIER

        # SPAWN/KILL HOOK
        if mouseup == 3 and self.hook != None: # reset hook when mouseup
            self.hook.kill()
        if mousedown == 3 and not self.frozen and not self.paused: # hook when mousedown and not frozen
            self.hook = self.Hook(self)
        
        # CHANGE WEAPON
        if keydown == K_1 and not self.paused:
            self.weapon.kill()
            self.weapon = self.Bat(self)
        if keydown == K_2 and self.launcher_owned and not self.paused :
            self.weapon.kill()
            self.weapon = self.Grenade_Launcher(self)

        # HOOK PHYSICS
        hook_acc = pygame.math.Vector2((0,0)) # not hooking -> no hook acceleration
        if self.hooking: # hook vector updated from hook class update method
            hook_acc = self.hook_vector.normalize() * self.HOOK_ACC
            # aiming in 90 degree direction
            for i in range(0, len(self.hook_vector)):
                if self.hook_vector[i] == 0:
                    if self.hook_vector[i-1] > 0: # positive x/y
                        hook_acc[i-1] = self.HOOK_ACC
                    elif self.hook_vector[i-1] < 0: # negative x/y
                        hook_acc[i-1] = -self.HOOK_ACC
            # hook strength multipliers
            if same_sign(hook_acc.x, self.base_vel.x):
                # walking in different direction as hook -> weaker pull
                hook_acc.x *= self.HOOK_PULL_WEAK
            if hook_acc.y > 0:
                # downards -> weaker pull
                hook_acc.y *= self.HOOK_PULL_WEAK
            else:
                # upwards -> stronger pull
                hook_acc.y *= self.HOOK_PULL_STRONG
        else:
            hook_acc = pygame.math.Vector2((0,0))

        # add hook acceleration to velocity
        self.hook_vel += hook_acc * PHYSICS_MULTIPLIER

        # FRICTION (clamp friction to max 1)
        self.base_vel.x -= self.base_vel.x * clamp_value(x_friction * PHYSICS_MULTIPLIER)
        self.hook_vel.x -= self.hook_vel.x * clamp_value(x_hook_friction * PHYSICS_MULTIPLIER)
        self.external_vel.x -= self.external_vel.x * clamp_value(x_hook_friction*2 * PHYSICS_MULTIPLIER)
        self.external_vel.y -= self.external_vel.y * clamp_value(x_hook_friction*2 * PHYSICS_MULTIPLIER)

        # WALK PHYSICS
        if keys[K_d] and not self.frozen and not(keys[K_d] and keys[K_a]) and not self.paused : # move right
            self.base_vel.x = mean_walk_vel
        elif keys[K_a] and not self.frozen and not(keys[K_d] and keys[K_a]) and not self.paused: # move left
            self.base_vel.x = -mean_walk_vel

        # JUMP PHYSICS
        if ((keydown == K_SPACE and self.jump_count < 2)  or (keys[K_SPACE] and self.grounded and self.jump_count_last_frame == 2)) and not self.frozen and not self.paused:
            if self.jump_count == 1:
                Particle(self.rect.bottomleft, type="cloud") 
                Particle(self.rect.bottomright, type="cloud")
            self.jump_count += 1
            # jumping -> set total velocity (rather than adding)
            self.hook_vel.y = self.JUMP_VEL
        # create copy -> no jump spam
        self.jump_count_last_frame = self.jump_count

        # add components of velocity into total
        self.truncate_small_velocities()
        self.total_vel = pygame.math.Vector2((self.base_vel.x + self.hook_vel.x*PHYSICS_MULTIPLIER + self.external_vel.x, self.hook_vel.y*PHYSICS_MULTIPLIER + self.external_vel.y))

        # clamp velocity to 1/2 tile size -> no clipping through tiles
        self.total_vel.x = clamp_value(self.total_vel.x, min=-self.TOTAL_VEL_LIMIT, max=self.TOTAL_VEL_LIMIT)
        self.total_vel.y = clamp_value(self.total_vel.y, min=-self.TOTAL_VEL_LIMIT, max=self.TOTAL_VEL_LIMIT)

        # check if kill key pressed
        if keydown == K_o and not self.paused : 
            self.total_vel = pygame.math.Vector2((0,0))
            self.kill()

        # update position value [more accurate than rect obj]
        self.update_pos()
        self.rect.center = round(self.pos_obj.center)
        self.spawn_trail() # ground particle

        # test for ground
        self.grounded = False
        for tile in User.TILE_SPRITES:
            if tile.rect.colliderect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height) and tile.tile in (1,2,3):
                self.grounded = True
        if not self.grounded and self.jump_count == 0:
            self.jump_count = 1

        if keydown == K_p: Dummy() # spawn test dummy

    # if a velocity is extremely small round it down to 0
    def truncate_small_velocities(self):
        for vel in self.velocities[1:]:
            if abs(vel.x) < 0.01:
                vel.x = 0
            if abs(vel.y) < 0.01:
                vel.y = 0

    # smooth out base x-velocity despite spikes in framerate
    def calculate_mean_walk_velocity(self):
        # refresh list 
        if len(self.walk_vel_list) > 20:
            self.walk_vel_list = [self.walk_vel_list[i] for i in range(10,20)]

        x_velocity = self.WALK_VEL * PHYSICS_MULTIPLIER
        self.walk_vel_list.append(x_velocity)
        mean_x_velocity = sum(self.walk_vel_list) / len(self.walk_vel_list)
        return mean_x_velocity

    def freeze(self):
        self.frozen = True
        self.surface = self.frozen_skin
        if self.freeze_timer != None: self.freeze_timer.kill()
        self.freeze_timer = Timer(1)
    
    def unfreeze(self):
        self.frozen = False
        self.surface = self.unfrozen_skin

    # determine different friction
    def calculate_friction(self):
        same_direction = same_sign(self.hook_vel.x, self.base_vel.x)
        # change friction if grounded
        if self.grounded:
            # base x friction highest when grounded
            x_friction = self.FRICTION_WALK_GROUND

            # hook x friction when grounded
            if same_direction and ((keys[K_a] or keys[K_d]) and not self.frozen):
                # hook velocity friction lower if moving same direction as walk
                x_hook_friction = self.FRICTION_HOOK_GROUND_1
            else:
                # hook velocity friction higher if moving opposite direction as walk
                x_hook_friction = self.FRICTION_HOOK_GROUND_2
        else:
            # friction lower when grounded
            x_friction = self.FRICTION_WALK_AIR
            if same_direction:
                # friction lower when same direction as hook force
                x_hook_friction = self.FRICTION_HOOK_AIR_1
            else:
                # friction higher when different direction as hook force
                x_hook_friction = self.FRICTION_HOOK_AIR_2

        return x_friction, x_hook_friction

    # update position taking into account collisions
    def update_pos(self):
        dx, dy = self.total_vel.x, self.total_vel.y
        tp_dx, tp_dy = 0, 0
        teleporting = False

        # X-collision calculated first using pos object
        for tile in User.TILE_SPRITES:
            
            tile_pos_obj = Pos(pygame.math.Vector2((tile.rect.center)), tile.rect.width/2)
            tile_radius_copy = tile_pos_obj.radius

            if tile_pos_obj.collide_x(self.pos_obj, self.total_vel.x):
                
                tile_pos_obj.radius = tile_radius_copy

                # solid
                if tile.tile in (1,2,3):
                    # Left movement
                    if self.total_vel.x < 0:
                        dx = (tile_pos_obj.center.x+tile_pos_obj.radius) - (self.pos_obj.center.x-self.pos_obj.radius) # tile right - player left
                        self.clear_velocity(0)
                    # Right movement
                    elif self.total_vel.x > 0:
                        dx = (tile_pos_obj.center.x-tile_pos_obj.radius) - (self.pos_obj.center.x+self.pos_obj.radius) # tile left - player right
                        self.clear_velocity(0)
                
                if tile.tile == 11 and type(self) == Player:
                    self.weapon.kill()
                    self.weapon = self.Grenade_Launcher(self)
                    self.launcher_owned = True

                info = self.small_collision_handling(tile, tile_pos_obj)
                if info[0] != None: dx = info[0]
                if info[1] != None: dy = info[1]
                if info[2] != None: tp_dx = info[2]
                if info[3] != None: tp_dy = info[3]
                if info[4] != None: teleporting = info[4]
 
        # update position x
        self.pos_obj.center.x += dx

        # Y-collision calculated second using pos object
        for tile in User.TILE_SPRITES:
            tile_pos_obj = Pos(pygame.math.Vector2((tile.rect.center)), tile.rect.width/2)
            if tile_pos_obj.collide_y(self.pos_obj, self.total_vel.y):
                
                tile_pos_obj.radius = tile_radius_copy

                # if solid
                if tile.tile in (1,2,3):
                    # Upwards movement
                    if self.total_vel.y < 0:
                        dy = (tile_pos_obj.center.y+tile_pos_obj.radius) - (self.pos_obj.center.y-self.pos_obj.radius) # tile bottom - player top
                        self.clear_velocity(1)
                    # Downards movement
                    elif self.total_vel.y > 0:
                        dy = (tile_pos_obj.center.y-tile_pos_obj.radius) - (self.pos_obj.center.y+self.pos_obj.radius) # tile top - player bottom
                        self.clear_velocity(1)
                        self.jump_count = 0
                    
                if tile.tile == 11 and type(self) == Player:
                    self.weapon.kill()
                    self.weapon = self.Grenade_Launcher(self)
                    self.launcher_owned = True

                info = self.small_collision_handling(tile, tile_pos_obj)
                if info[0] != None: dx = info[0]
                if info[1] != None: dy = info[1]
                if info[2] != None: tp_dx = info[2]
                if info[3] != None: tp_dy = info[3]
                if info[4] != None: teleporting = info[4]

        # update position y
        self.pos_obj.center.y += dy

        # revert previous position correction + apply new vector2 if teleporting
        if teleporting:
            self.pos_obj.center -= pygame.math.Vector2((dx,dy))
            self.pos_obj.center += pygame.math.Vector2((tp_dx, tp_dy))  

    # handles collision of tiles smaller than 1 tile
    def small_collision_handling(self, tile, tile_pos_obj):
        dx, dy, tp_dx, tp_dy, teleporting = None,None,None,None,None
        tile_pos_obj.radius = 1
        if tile_pos_obj.collide_x(self.pos_obj, self.total_vel.x):

            if tile.tile == 4: # freeze
                if type(self) == Player: self.kill_hook()
                self.freeze()
                    
            if tile.tile == 5: # teleport
                if type(self) == Player: self.kill_hook()
                try:
                    tp_dx, tp_dy = self.get_random_tile_offset(6, tile.tp)
                    teleporting = True
                    self.unfreeze()
                except:
                    pass # no teleporter

            if tile.tile == 8: # start_line
                if type(self) == Player: self.speedrun_timer.reset()

            if tile.tile == 9: # finish_line
                if type(self) == Player:
                    if not self.speedrun_timer.complete:
                        time = self.speedrun_timer.time # use to save times in database
                        self.speedrun_timer.complete = True

            # kill
            if tile.tile == 10:
                dx, dy = (0,0)
                self.kill()
                self.unfreeze()
        
            # weapon remover
            if tile.tile == 12 and type(self) == Player:
                self.weapon.kill()
                self.weapon = self.Bat(self)
                self.launcher_owned = False
            
            # tutorial box
            if tile.tile == 13 and not self.tutorial_boxes_read[tile.tp]:
                self.paused = True
                self.tutorial_text = tile.tp
                self.tutorial_boxes_read[tile.tp] = True
                UIEVENTHANDLER.handle_event("tutorial_box")
                del self.tutorial_text

        return dx,dy,tp_dx,tp_dy,teleporting

    # reset hook
    def kill_hook(self):
        if self.hook != None:
            self.hook.kill()

    # kill player
    def kill(self):
        if type(self) == Player:
            self.weapon.kill()
            self.launcher_owned = False # reset weapon
            self.weapon = self.Bat(self)
            self.speedrun_timer.time = 0
            self.speedrun_timer.complete = True # reset speedrun timer
            self.kill_hook() # no hook
        particle_positions = (self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright, self.rect.center)
        for position in particle_positions: # spawn particles
            Particle(position, type="cloud")
        dx, dy = self.get_random_tile_offset(7) # find spawner
        self.pos_obj.center += pygame.math.Vector2((dx,dy)) # tp to spawner
        self.rect.center = self.pos_obj.center
        self.clear_velocity()

    # clear velocity -> | def = x,y | 0 = x | 1 = y
    def clear_velocity(self, vector=(0,1)):
        if type(vector) == int: vector = [vector] # convert to list if int
        for velocity in self.velocities:
            for v in vector:
                velocity[v]= 0

    # get distance to tile of random type or teleport ID
    def get_random_tile_offset(self, tile_type, tp=0):
        tp_tiles = []

        for tile in User.TILE_SPRITES:
            if tile.tile == tile_type and (tile.tp == tp if tile_type == 6 else True):
                tp_tiles.append(tile)
        
        random_tp_tile = tp_tiles[random.randint(0, len(tp_tiles)-1)].rect
        dx = random_tp_tile.x - self.rect.x
        dy = random_tp_tile.bottom - self.rect.bottom
        self.unfreeze()
        return dx, dy
    
    # spawn walking trail
    def spawn_trail(self):
        if abs(self.total_vel.x) > 1 and self.jump_count == 0 and self.trail_timer.complete:
            self.trail_timer.kill()
            x,y = self.rect.bottomleft if self.total_vel.x > 0 else self.rect.bottomright
            y -= 15
            Particle((x,y), type="trails")
            self.trail_timer = Timer(0.1)

# acts as another player
class Dummy(Player):

    def __init__(self):
        # frozen/unfrozen skin
        self.unfrozen_skin = create_sprite(SKINS_SPRITESHEET, 25, 25, 2.5, sheet=True, frame=4, opacity=255)
        self.frozen_skin = create_sprite(SKINS_SPRITESHEET, 25, 25, 2.5, sheet=True, frame=4, opacity=125)

        # important
        self.surface = self.unfrozen_skin
        self.rect = self.surface.get_rect()
        self.rect.center = pygame.math.Vector2((width/2,height/2))
        self.pos_obj = Pos(self.rect.center, self.rect.width/2)

        # main velocities
        self.total_vel = pygame.math.Vector2((0,0)) # total velocity
        self.hook_vel = pygame.math.Vector2((0,0)) # "gravity velocity"
        self.external_vel = pygame.math.Vector2((0,0)) # applied velocities
        self.velocities = [self.total_vel, self.hook_vel, self.external_vel]

        # other attributes 
        self.grounded = False
        self.freeze_timer = Timer(0) # timer until unfrozen

        # spawn at spawn point
        dx, dy = self.get_random_tile_offset(7)
        self.rect.center += pygame.math.Vector2((dx,dy))
        self.pos_obj.center += pygame.math.Vector2((dx,dy))

        # update groups
        User.PLAYER_SPRITES.append(self)
        User.ALL_UPDATES.append(self)

    def update(self):
        # determine new values
        x_friction = self.FRICTION_WALK_GROUND if self.grounded else self.FRICTION_WALK_AIR

        # GRAVITY
        if not self.grounded:
            self.hook_vel.y += self.GRAVITY_ACC * PHYSICS_MULTIPLIER

        # FRICTION clamp to a max of 1 (using base friction for now)
        self.external_vel.x -= self.external_vel.x * clamp_value(x_friction * PHYSICS_MULTIPLIER)
        self.external_vel.y -= self.external_vel.y * clamp_value(self.FRICTION_WALK_AIR * PHYSICS_MULTIPLIER)

        # add components of velocity into total
        self.truncate_small_velocities()
        self.total_vel = pygame.math.Vector2((self.external_vel.x, self.external_vel.y + self.hook_vel.y*PHYSICS_MULTIPLIER))

        # clamp velocity to 1/2 tile size -> no clipping through tiles
        self.total_vel.x = clamp_value(self.total_vel.x, min=-self.TOTAL_VEL_LIMIT, max=self.TOTAL_VEL_LIMIT)
        self.total_vel.y = clamp_value(self.total_vel.y, min=-self.TOTAL_VEL_LIMIT, max=self.TOTAL_VEL_LIMIT)

        # update position value [more accurate than rect obj]
        self.update_pos()
        self.rect.center = round(self.pos_obj.center)
        
        # test for ground
        self.grounded = False
        for tile in User.TILE_SPRITES:
            if tile.rect.colliderect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height) and tile.tile in (1,2,3):
                self.grounded = True

class Tile():

    def __init__(self, surf, rect, tile, tp):
        self.surface = surf
        self.rect = rect
        self.tile = tile
        if tp != None: self.tp = tp
        if self.tile == 12:
            self.particle = Particle((self.rect.center), type="cloud")
            self.particle_timer = Timer(0)
            self.new_particle()
            User.ALL_UPDATES.append(self)
        User.TILE_SPRITES.append(self)
        
    def update(self):
        if self.particle_timer.complete:
            self.new_particle()

    def new_particle(self): # weapon remover tile animation
        self.particle.kill()
        self.particle_timer.kill()
        x = random.randint(self.rect.left+15, self.rect.right-15)
        y = random.randint(self.rect.top+15, self.rect.bottom-15)
        self.particle = Particle((x,y) ,type="cloud")
        self.particle_timer = Timer(0.2)


class Level_Creator_Controller():

    vel = 20

    def __init__(self):
        self.rect = Rect(1,1,0,0)
        self.rect.center = (width/2,height/2)
        User.ALL_UPDATES.append(self)
    
    def update(self):
        if UIEVENTHANDLER.UI_LIST[0] == "level_creator":
            if keys[K_a]:
                self.rect.x -= self.vel
            if keys[K_d]:
                self.rect.x += self.vel
            if keys[K_w]:
                self.rect.y -= self.vel
            if keys[K_s]:
                self.rect.y += self.vel
            if pygame.mouse.get_pressed()[0]:
                mouse_rect = Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
                if not(mouse_rect.colliderect(UIEVENTHANDLER.UI_LIST[1].rect) or mouse_rect.colliderect(UIEVENTHANDLER.UI_LIST[3].rect)): # mouse not on UI
                    for tile in User.TILE_SPRITES:
                        if mouse_rect.colliderect(tile.rect) and type(tile) == Grid_Square:
                            tile.change_tile(User.Level_Creator.TOOL_SELECTED, User.Level_Creator.TELEPORTER_KEY)

class Grid_Square():

    class Non_Tile_Square():

        def __init__(self, surf, pos):
            self.surface = surf
            self.rect = self.surface.get_rect()
            self.rect.center = pos
            User.TILE_SPRITES.append(self)

        def kill(self):
            User.TILE_SPRITES.pop(User.TILE_SPRITES.index(self))
            del self

    def __init__(self, x, y):
        self.surface = self.tiles[0]
        self.rect = self.surface.get_rect()
        self.rect.topleft = (x,y)
        self.tile = 0
        self.tp=0
        self.non_tile_component = None
        User.TILE_SPRITES.append(self)

    def change_tile(self, tile, tp):
        if self.non_tile_component != None:
            self.non_tile_component.kill()
            self.non_tile_component = None
        self.surface = self.tiles[tile]
        self.tile = tile
        self.tp = tp
        if self.tile in (11, 12): # non-tile component (weapon spawner/remover)
            self.non_tile_component = self.Non_Tile_Square(self.surface, self.rect.center)
            self.surface = self.grid_surface()

    @classmethod
    def grid_surface(cls):
        surface = pygame.surface.Surface((65, 65), pygame.SRCALPHA).convert_alpha()
        surface.set_alpha(255)
        surface.fill((0,0,0,255))
        surface.fill((0,0,0,0), surface.get_rect().inflate(-2, -2))
        return surface

    @classmethod
    def tiles_surfaces(cls):
        cls.tiles = [cls.grid_surface()]
        for i in range(0,10):
            opacity = 255 if i <= 1 else 175 if (i > 1 and i < 5) else 120
            sprite = create_sprite(TILE_SPRITESHEET, 20, 20, 65/20, sheet=True, frame=i, opacity=opacity)
            cls.tiles.append(sprite)
        cls.tiles.append(create_sprite(WEAPONS_SPRITESHEET, 36, 10, 1.5, sheet=True, frame=1, opacity=200))
        cls.tiles.append(create_sprite(CLOUD, 9, 7, 3, opacity=200))

class Particle():

    def __init__(self, pos, type="trails"):

        match type:
            case "trails":
                self.img = TRAILS_SPRITESHEET
                self.dimensions = (4,7)
                self.scale = 3
                self.shrink_speed = 2
                self.sheet = True
                self.frame=random.randint(0,2)
            case "cloud":
                self.img = CLOUD
                self.dimensions = (9,7)
                self.scale = 5
                self.shrink_speed = 10
            case "explosion":
                self.img = EXPLOSION
                self.dimensions = (18,19)
                self.scale = 7
                self.shrink_speed = 20
        
        if type != "trails":
            self.sheet = False
            self.frame = None

        self.surface = create_sprite(self.img, self.dimensions[0], self.dimensions[1], self.scale, sheet=self.sheet, frame=self.frame, opacity=255)
        self.rect = self.surface.get_rect()
        self.rect.center = pos

        User.ALL_UPDATES.append(self)
        User.PARTICLE_SPRITES.append(self)

    def update(self):
        self.copy_rect = self.rect.copy()
        try:
            self.scale -= self.shrink_speed * (delta_time if self.shrink_speed*delta_time > 0 else self.scale)
            self.surface = create_sprite(self.img, self.dimensions[0], self.dimensions[1], self.scale, sheet=self.sheet, frame=self.frame, opacity=255)
            self.rect = self.surface.get_rect()
            self.rect.center = self.copy_rect.center
        except: # delete particle
            self.kill()

    def kill(self):
        User.ALL_UPDATES.pop(User.ALL_UPDATES.index(self))
        User.PARTICLE_SPRITES.pop(User.PARTICLE_SPRITES.index(self))
        del self

# time since started level
class Speedrun_Timer():

    def __init__(self):
        self.time = 0
        self.complete = True
        User.ALL_UPDATES.append(self)

    def update(self):
        if not self.complete:
            self.time += delta_time
    
    def reset(self):
        self.time = 0
        self.complete = False

# cooldown timer
class Timer():

    def __init__(self, duration):
        self.complete = False
        self.time = time.time()
        self.finish_time = self.time + duration
        User.ALL_UPDATES.append(self)
        
    def update(self):
        self.time += delta_time
        if self.time > self.finish_time:
            self.complete = True
    
    def kill(self):
        User.ALL_UPDATES.pop(User.ALL_UPDATES.index(self))
        del self
        

# for collisions without the stupid rect inaccuracy
class Pos():

    def __init__(self, center, side_length):
        self.center = center # vector2
        self.radius = side_length # int
    
    def collide_x(self, pos2, x_vel):
        # conditions:
        c1 = (self.center.x-self.radius) < (pos2.center.x+pos2.radius+x_vel) # left < right
        c2 = (self.center.y-self.radius) < (pos2.center.y+pos2.radius) # top < bottom
        c3 = (self.center.x+self.radius) > (pos2.center.x-pos2.radius+x_vel) # right > left
        c4 = (self.center.y+self.radius) > (pos2.center.y-pos2.radius) # bottom > top
        if c1 and c2 and c3 and c4:
            return True
        return False
    
    def collide_y(self, pos2, y_vel):
        # conditions:
        c1 = (self.center.x-self.radius) < (pos2.center.x+pos2.radius) # left < right
        c2 = (self.center.y-self.radius) < (pos2.center.y+pos2.radius+y_vel) # top < bottom
        c3 = (self.center.x+self.radius) > (pos2.center.x-pos2.radius) # right > left
        c4 = (self.center.y+self.radius) > (pos2.center.y-pos2.radius+y_vel) # bottom > top
        if c1 and c2 and c3 and c4:
            return True
        return False

#===========function=============================================

def same_sign(value1, value2):
    return abs(value1) + abs(value2) == abs(value1 + value2)

def clamp_value(value, min=-1, max=1):
    if value > max: return max
    if value < min: return min
    return value

def get_pos(rect):
    return (rect.topleft - User.MAP_ORIGIN) / 65

def get_angle(dx, dy):
            theta = math.atan(dy/dx)/(math.pi/180) if dx != 0 else 0 # angle of rotation

            # different rotation cases
            if dx > 0 and dy < 0:
                angle = -theta
            elif dx < 0 and dy < 0:
                angle = (180-theta)
            elif dx < 0 and dy > 0:
                angle = -(180+theta)
            elif dx > 0 and dy > 0:
                angle = (360-theta)
            elif dx == 0 and dy > 0:
                angle = 270
            elif dx == 0 and dy < 0:
                angle = 90
            elif dy == 0 and dx < 0:
                angle = 180
            else:
                angle = 0
            
            return angle

def format_time(time):
    hours, remainder = time // 3600, time % 3600
    minutes, remainder = remainder // 60, remainder % 60
    seconds = remainder // 1
    ms = remainder % 1
    hours, minutes, seconds = int(hours), int(minutes), int(seconds)
    ms = str(ms)[2:4]
    if ms == "": ms = 00
    if len(str(hours)) < 2: hours = f"0{hours}"
    if len(str(minutes)) < 2: minutes = f"0{minutes}"
    if len(str(seconds)) < 2: seconds = f"0{seconds}"
    if len(str(ms)) < 2: ms = f"0{ms}"
    return f"{hours}:{minutes}:{seconds}:{ms}"

def img_from_path(filename):
    return pygame.image.load(os.path.abspath(os.path.join(dir_path, filename)))

def create_sprite(img, width, height, scale, sheet=False, frame=0, opacity=False):
    if opacity != False:
        sprite_surface = pygame.surface.Surface((width,height), pygame.SRCALPHA).convert_alpha()
        sprite_surface.set_alpha(opacity)
    else:
        sprite_surface = pygame.surface.Surface((width,height)).convert()

    if sheet:
        sprite_surface.blit(img, (0,0), (frame*width, 0, width, height))
    else:
        sprite_surface.blit(img, (0,0))
    
    return pygame.transform.scale_by(sprite_surface, scale)

def map_from_file(filename, directory=os.path.dirname(os.path.realpath(__file__)) + "\\map\\"):
    file_path = directory + filename
    with open(file_path, "r") as file:
        lines = file.readlines()
        world = [[x for x in line.strip().split(",")] for line in lines]
        return world

def file_from_map(filename):
    file = ""
    tile_count = -1
    for tile in User.TILE_SPRITES:
        if type(tile) == Grid_Square:
            tile_count += 1
            if tile_count % 100 == 0 and tile_count != 0: # new line if end of tile row
                file = file[:-1] # get rid of final comma
                file+="\n"
            if tile.tile in (5,6):
                file += f"{'{:x}'.format(tile.tile)}{'{:x}'.format(tile.tp)},"
            else:
                file += f"{'{:x}'.format(tile.tile)},"
    file = file[:-1] # get rid of final comma
    # write to file
    file_path = os.path.dirname(os.path.realpath(__file__)) + f"\\map\\{filename}"
    with open(file_path, "w") as f:
        f.write(file)

def tutorial_create_map(filename, tile_size=65):
    map_space = map_from_file(filename)
    # reset current tiles
    while len(User.TILE_SPRITES) != 0:
        del User.TILE_SPRITES[0]
        User.TILE_SPRITES.pop(0)

    # fill tile blit group with tile data (surface, rect)
    current_row = 0
    for row in map_space:
        current_column = 0
        for column in row:
            column = str(column)
            loaded_tile = Grid_Square(current_column * tile_size, current_row * tile_size)
            tile_type = int(column[0], 16)
            tp = int(column[1], 16) if len(column) > 1 else None
            loaded_tile.change_tile(tile_type, tp)    
            current_column += 1 
        current_row += 1

def create_map(filename, directory=None, tile_size=65):
    if directory == None:
        map_space = map_from_file(filename)
    else:
        map_space = map_from_file(filename, directory=directory)
    # initialise tile images
    loaded_tiles = []
    for i in range(0,10):
        opacity = 255 if i <= 1 else 175 if (i > 1 and i < 5) else 120
        sprite = create_sprite(TILE_SPRITESHEET, 20, 20, tile_size/20, sheet=True, frame=i, opacity=opacity)
        loaded_tiles.append(sprite)
    loaded_tiles.append(create_sprite(WEAPONS_SPRITESHEET, 36, 10, 2.5, sheet=True, frame=1, opacity=200))

    # fill tile blit group with tile data (surface, rect)
    current_row = 0
    for row in map_space:
        current_column = 0
        for column in row:
            column = str(column)
            tile_type = int(column[0], 16)
            if tile_type not in (0, 12, 13):
                img = loaded_tiles[tile_type-1]
                img_rect = img.get_rect()
                img_rect.x = current_column * tile_size
                img_rect.y = current_row * tile_size
                if tile_type == 11: img_rect.center = current_column*(tile_size)+tile_size/2,current_row*tile_size+tile_size/2 # weapon
                tp = int(column[1], 16) if len(column) > 1 else None
                Tile(img, img_rect, tile_type, tp)
            if tile_type == 12:
                img = pygame.surface.Surface((tile_size, tile_size), pygame.SRCALPHA).convert_alpha()
                img.set_alpha(0)
                img_rect = img.get_rect()
                img_rect.x = current_column * tile_size
                img_rect.y = current_row * tile_size
                Tile(img, img_rect, tile_type, None)
            if tile_type == 13:
                img = pygame.surface.Surface((tile_size, tile_size)).convert_alpha()
                img.set_alpha(0)
                img_rect = img.get_rect()
                img_rect.x = current_column * tile_size
                img_rect.y = current_row * tile_size
                tp = int(column[1], 16) if len(column) > 1 else None
                Tile(img, img_rect, tile_type, tp)
            current_column += 1 
        current_row += 1

def create_tutorial_grid(tile_size=65, map_limit=100):
    column = 0
    Grid_Square.tiles_surfaces()
    while column < map_limit:
        row = 0
        while row < map_limit:
            Grid_Square(tile_size*row, tile_size*column)
            row+=1
        column+=1

def center_camera():
    offset = pygame.Vector2((width/2, height/2)) - User.PLAYER.rect.center
    User.MAP_ORIGIN += offset
    if type(User.PLAYER) == Level_Creator_Controller: User.PLAYER.rect.center += offset
    for blit_group in User.ALL_SPRITES:
        for sprite in blit_group:
            try:
                if type(sprite).AFFECTED_BY_CAMERA == False:
                    pass # not affected -> do nothing
            except:
                    sprite.rect.topleft += offset
            try:
                sprite.pos_obj.center += offset
            except:
                pass # no pos_obj attribute

def load_singleplayer_map(map, directory=None):
    User.MAP_ORIGIN = pygame.math.Vector2((0,0))
    create_map(filename=map, directory=directory)
    User.PLAYER = Player(User.SKIN_EQUIPPED)
    UIEVENTHANDLER.handle_event("game")

def load_level_creator():
    create_tutorial_grid()
    User.PLAYER = Level_Creator_Controller()

def restart():
    User.PLAYER = None
    User.TILE_SPRITES, User.WEAPON_SPRITES, User.PARTICLE_SPRITES, User.HOOK_SPRITES, User.PLAYER_SPRITES, User.INTERFACE_SPRITES, User.ALL_UPDATES  = [], [], [], [], [], [], [UIEVENTHANDLER]
    User.ALL_SPRITES = [User.TILE_SPRITES, User.WEAPON_SPRITES, User.PARTICLE_SPRITES, User.HOOK_SPRITES, User.PLAYER_SPRITES, User.INTERFACE_SPRITES]
    User.ALL_GROUPS = [x for x in User.ALL_SPRITES]
    User.ALL_GROUPS.append(User.ALL_UPDATES)
    User.RESTART = True

# load images (dimension comments = of 1 frame)
dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\img\\"
IN_GAME_BACKGROUND = img_from_path("in-game_bg.png")
TITLE_BACKGROUND = img_from_path("title_bg.png")
TITLE_IMG = img_from_path("title_img.png") # 115x69

TILE_SPRITESHEET = img_from_path("tile_spritesheet.png") # 20x20
SKINS_SPRITESHEET = img_from_path("skins_spritesheet.png") # 25x25

TRAILS_SPRITESHEET = img_from_path("trails_spritesheet.png") # 4x7
CLOUD = img_from_path("cloud.png") # 9x7
EXPLOSION = img_from_path("explosion.png") # 18x19

HOOK_HEAD = img_from_path("hook_head_sprite.png") # 12x9
HOOK_WRAP = img_from_path("hook_wrap_sprite.png") # 8x7

WEAPONS_SPRITESHEET = img_from_path("weapons_spritesheet.png") # 36x10
PROJECTILES_SPRITESHEET = img_from_path("projectiles_spritesheet.png") # 8x8

#=========declare constants================
width = 1920
height = 1080
FPS_limit = 75
Target_FPS = 75
frame = 0

# other
initial_time, previous_time = time.time(), time.time()
keydown, keydown_unicode, mousedown, mouseup = None, None, None, None
#========================main============================================
clock = pygame.time.Clock()
display = pygame.display.set_mode((1920,1080), pygame.SCALED, vsync=1)

# startup UI
UIEVENTHANDLER.instantiate_UI()
#===========| MAIN LOOP |===============
while True:
    if keydown: keydown = None
    if keydown_unicode: keydown_unicode = None
    if mousedown: mousedown = None # reset keydowns
    if mouseup: mouseup = None

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit event
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keydown = event.key
            keydown_unicode = event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN: mousedown = event.button # [mouse_left, mouse_middle, mouse_right]
        if event.type == pygame.MOUSEBUTTONUP: mouseup = event.button # [mouse_left, mouse_middle, mouse_right]

    keys = pygame.key.get_pressed()

    # update delta time
    delta_time = time.time() - previous_time
    previous_time = time.time()
    if delta_time > 1/30: delta_time = 1/30 # limit ridiculously high delta time [<30fps = unsupported]
    PHYSICS_MULTIPLIER = Target_FPS * delta_time

    frame += 1
    #FPS = frame/(time.time()-initial_time)
    if frame % 30 == 0: FPS = 1/delta_time
 
    # update display
    display.blit(User.BACKGROUND_SURFACE, (0,0))

    # refresh all sprites and update methods
    for group in User.ALL_GROUPS:
        for item in group:
            if User.RESTART:
                User.RESTART = False
                break
            if group != User.ALL_UPDATES:
                display.blit(item.surface, item.rect)
            else:
                item.update()

    if User.PLAYER != None: center_camera()

    pygame.display.update()
    clock.tick(FPS_limit)
