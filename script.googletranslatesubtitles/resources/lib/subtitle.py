from googletranslate.google_trans_new import google_translator
import xbmcvfs
import xbmcgui
import xbmcaddon
import os
from contextlib import closing

GT_CHAR_LENGTH = 4900
LINE_LENGTH = 45

ADDON = xbmcaddon.Addon()
__addon__     = xbmcaddon.Addon()
_  = __addon__.getLocalizedString

class Subtitle:
    def __init__(self, filename, file):
        self.filename = filename
        self.file = file
        self.sub_in_string = None
        self.rough_result = None
        self.translations = {}

    def create_sub_in_string(self):
        sub_in_string = []
        for x in range(len(self.file)):
            if len(self.file[x]) == 30 or len(self.file[x]) == 31:
                if self.file[x][0] == "0" and self.file[x][17] == "0":
                    sub_in_string.append("  @" + self.file[x-1].strip() + "@ ")
                    sub_in_string.append(" " + self.file[x+1].strip())
                    sub_in_string.append(" " + self.file[x+2].strip())
        self.sub_in_string = "".join(sub_in_string)

    def translate(self, dest_lang):
        translator = google_translator()
        new_lines = []
        lengths = [0]
        current_length = GT_CHAR_LENGTH

        while current_length < len(self.sub_in_string):
            for x in range(current_length, len(self.sub_in_string)):
                if self.sub_in_string[x] == "@":
                    lengths.append(x-1)
                    current_length = x + GT_CHAR_LENGTH
                    break
        lengths.append(len(self.sub_in_string))

        pDialog = xbmcgui.DialogProgress()
        pDialog.create(_(32018), _(32019))
        percentage = 0
        for n in range(1, len(lengths)):

            percentage += 100/len(lengths)
            pDialog.update(int(percentage))
            p, q = lengths[n-1], lengths[n]
            result = translator.translate(self.sub_in_string[p:q],lang_tgt=dest_lang)
            new_lines.append(result)
        self.rough_result = "".join(new_lines).split("@")

    def dictify_return(self):
        self.dict_of_sub = {}
        for x in range(len(self.rough_result)):
            stripped = self.rough_result[x].strip()
            if stripped.isdigit():
                self.dict_of_sub[int(stripped)] = self.rough_result[x+1].strip()

    def hackup_string(self, string):
        for x in range(LINE_LENGTH, -1, -1):
            if string[x] == " ":
                break
        if x == 0:
            return string
        return string[:x].strip() + "\n" + string[x:].strip()

    def create_new_sub(self):
        self.new_subtitlefile = []
        for line in range(len(self.file)):
            if len(self.file[line]) == 30 or len(self.file[line]) == 31:
                if self.file[line][0] == "0" and self.file[line][17] == "0":
                    self.new_subtitlefile.append(self.file[line-1])
                    self.new_subtitlefile.append(self.file[line])
                    try:
                        xxx = int(self.file[line-1])
                        if len(self.dict_of_sub[xxx]) > LINE_LENGTH:
                            xx = self.hackup_string(self.dict_of_sub[xxx])
                            self.new_subtitlefile.append(xx + "\n\n")
                        else:
                            self.new_subtitlefile.append(self.dict_of_sub[xxx] +"\n\n")
                    except:
                        pass
                    self.new_subtitlefile.append("\n")

    def save_the_file(self, language, destination):
        with closing(xbmcvfs.File(destination, 'w')) as e:
            e.write("".join(self.translations[language]))
        if xbmcvfs.exists(destination):
            # "Written to:"
            xbmcgui.Dialog().textviewer(_(32015), _(32015) + "\n" +
                                                str(os.path.dirname(destination)) +
                                                "\n" + _(32016) + str(os.path.basename(destination)) +
                                                "\n" + _(32017))
            return True
        return False

    def translate_sequence(self, language):
        if language in self.translations:
            return self.translations[language]
        if not self.sub_in_string:    
            self.create_sub_in_string()
        self.translate(language)
        self.dictify_return()
        self.create_new_sub()
        self.translations[language] = self.new_subtitlefile
        return self.new_subtitlefile
