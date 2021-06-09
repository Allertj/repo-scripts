import xbmc
import os
import xbmcgui
import xbmcvfs
import sys
import xbmcaddon
from .loading import FileLoader
from .subtitle import Subtitle
from .menu import Menu

ADDON = xbmcaddon.Addon()
__addon__     = xbmcaddon.Addon()
_  = __addon__.getLocalizedString

def start():
    if xbmc.Player().isPlayingVideo():
        current_subs = xbmc.Player().getAvailableSubtitleStreams()
        playingfile = xbmc.Player().getPlayingFile()
        if any(current_subs):
            active_sub_lang = xbmc.Player().getSubtitles()
            lang = xbmc.convertLanguage(active_sub_lang, xbmc.ISO_639_1)
            if not lang:
                filename = os.path.splitext(playingfile)[0] + ".srt"
            else:
                filename = os.path.splitext(playingfile)[0] + "." + lang + ".srt"
            if xbmcvfs.exists(filename):
                # Translate this subtitle?, Do you want to translate, Choose Another, Yes, No
                response = xbmcgui.Dialog().yesnocustom(_(32000), _(32001) + os.path.basename(filename) + "?",
                                                        customlabel= _(32002),
                                                yeslabel = _(32003), nolabel = _(32004))                                
                if response == 0:
                    sys.exit()
                elif response == 1:
                    load_file(filename)
                elif response == 2:
                    manual_choice(playingfile)
            else:
                manual_choice(playingfile)
    choose_file()

def manual_choice(playing_file):
    playing_dir = os.path.dirname(playing_file) + "/"
    # Select File
    filename = xbmcgui.Dialog().browse(1, _(32009), 'files', ".srt", False, False, playing_dir)
    if filename == playing_dir:
        sys.exit()
    load_file(filename)

def choose_file():
    xbmcgui.Dialog().ok(_(32020), _(32021))
    filename = xbmcgui.Dialog().browse(1, _(32028), 'video', ".srt")
    if not filename:
        sys.exit()
    else:
        load_file(filename)

def load_file(filename):
    fileloader = FileLoader(filename)
    file = fileloader.read_file()
    subtitle = Subtitle(filename, file)
    menu = Menu(subtitle)
    menu.display_menu()
