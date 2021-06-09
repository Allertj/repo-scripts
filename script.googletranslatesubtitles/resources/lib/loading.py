import xbmcvfs
import chardet
from contextlib import closing
import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()
__addon__     = xbmcaddon.Addon()
_  = __addon__.getLocalizedString

class FileLoader():
    def __init__(self, filename):
        self.filename = filename

    def standard_reader(self, filename):
        with closing(xbmcvfs.File(filename)) as file:
            lines = file.read().split("\n")
        return lines

    def chardet_reader(self, filename):
        with closing(xbmcvfs.File(filename)) as file:
            encoding_progress = xbmcgui.DialogProgress()
            encoding_progress.create(_(32136), _(32137))
            byte_string = bytes(file.readBytes())
            result = chardet.detect(byte_string)
            text_string = byte_string.decode(result["encoding"])
            encoding_progress.close()
        return text_string.split("\n")

    def standard_reader_with_errors(self, filename):
        with closing(xbmcvfs.File(filename)) as file:
            byte_string = bytes(file.readBytes())
            text_string = byte_string.decode("utf-8", errors="replace")
        return text_string.split("\n")

    def read_file_sequence(self):
        options = [self.standard_reader, self.chardet_reader, self.standard_reader_with_errors]
        for reader in options:
            try:
                sub = reader(self.filename)
                subtitlefile = [sentence+"\n" for sentence in sub] + ["", ""]
                return subtitlefile
            except:
                continue
        return None

    def read_file(self):
        subtitlefile = self.read_file_sequence()
        if not subtitlefile:
            raise TypeError("No subtitle found")
        else:
            return subtitlefile
