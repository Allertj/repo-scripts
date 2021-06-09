import xbmcvfs
import xbmcgui
import xbmcaddon
import os
import xbmc
import sys
from .language_list import LANGUAGES

ADDON = xbmcaddon.Addon()
__addon__     = xbmcaddon.Addon()
_  = __addon__.getLocalizedString


class Menu:
    def __init__(self, subtitle):
        self.language = None
        self.saved = True
        self.subtitle = subtitle
        self.options = [(_(32022), self.scroll_original_subtitles),
                        (_(32023), self.pick_language),
                        (_(32026), self.quit)]

    def display_menu(self):
        self.update_menu()
        options = [names for names, functions in self.options]
        result = xbmcgui.Dialog().contextmenu(options)
        self.options[result][1]()

    def update_menu(self):
        if self.language:
            current = xbmc.convertLanguage(self.language, xbmc.ENGLISH_NAME)
            self.options[1] = (_(32023) + " (" + _(32135) + " " + current + ")", self.pick_language)
        if self.language and (_(32024), self.translate) not in self.options:
            self.options.insert(2, (_(32024), self.translate))
        if self.language in self.subtitle.translations:
            if (_(32027), self.view_translation) not in self.options:
                self.options.insert(3, (_(32027), self.view_translation))
                self.options.insert(-1, (_(32025), self.save_the_file))

     

    def scroll_original_subtitles(self):
        xbmcgui.Dialog().multiselect(_(32028), self.subtitle.file)
        self.display_menu()

    def pick_language(self):
        language_code = xbmc.getLanguage(xbmc.ISO_639_1)
        language = xbmc.getLanguage(xbmc.ENGLISH_NAME)
        # Translate to which language?, Current Language:, Select one manually
        result = xbmcgui.Dialog().select(_(32011), [_(32012)+ language, _(32013)])
        if result == -1:
            pass
            # return ""
        elif result == 0:
            self.language = language_code
        elif result == 1:
            options = [i for i, k in LANGUAGES.items()]
            read_options = [xbmc.convertLanguage(option, xbmc.ENGLISH_NAME) for option in options]
            choice = xbmcgui.Dialog().select(_(32010), read_options)
            if choice == -1:
                pass 
            else:    
                self.language = options[choice]
        self.display_menu()

    def view_translation(self):
        xbmcgui.Dialog().multiselect(_(32028), self.subtitle.translations[self.language])
        self.display_menu()

    def translate(self):
        self.subtitle.translate_sequence(self.language)
        self.saved = False
        self.display_menu()

    def save_the_file(self):
        destination_with_translate = self.subtitle.filename[:-4] + "." + self.language + "_translated.srt"
        # Save the file, Save the file to, "With translated added", "Save to custom filename",
        # "Exit to main menu", "Cancel and exit completely"
        resp = xbmcgui.Dialog().select(_(32039), [_(32040) +  self.language + "_" + _(32041) +
                                destination_with_translate, _(32042) , _(32043), _(32044)])
        if resp == 0:
            destination = destination_with_translate
        if resp == 1:
            new_filename = xbmcgui.Dialog().input(_(32045),
                                defaultt= os.path.basename(destination_with_translate),
                                type=xbmcgui.INPUT_ALPHANUM)
            if not new_filename:
                self.save_the_file()
            destination = os.path.dirname(self.subtitle.filename) + "/" + new_filename
        if resp == 2 or resp == -1:
            self.display_menu()
        if resp == 3:
            self.quit()
        if self.subtitle.save_the_file(self.language, destination):
            self.saved = True
            self.display_menu()

    def quit(self):
        if not self.saved and self.language in self.subtitle.translations:
            res = xbmcgui.Dialog().yesno(_(32034), _(32035), yeslabel=_(32003), nolabel=_(32004))
            if res:
                sys.exit()
            else:
                self.save_the_file()
        sys.exit()   
