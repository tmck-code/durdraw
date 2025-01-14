import curses

import durdraw.durdraw_ui_curses as ui_curses
from durdraw.durdraw_appstate import AppState

def init_ui():
    DURVIEW_VER = "0.1.0"
    DUR_FILE_VER = 7

    app = AppState()
    app.setDurVer(DURVIEW_VER)
    app.setDurFileVer(DUR_FILE_VER)
    app.configFileLoaded = False
    app.configFileLoaded = True
    app.colorMode = "256"
    app.width = 80
    app.height = 24
    app.showStartupScreen = False
    app.hasMouse = False
    app.hasHelpFile = False
    app.charEncoding = "utf-8"
    app.themesEnabled = False
    app.durhelp256_fullpath = 'durdraw/help/durhelp-256-long.dur'

    # app.durhelp256_fullpath = 'durdraw/help/durhelp-256-long.dur'
    # app.durhelp256_page2_fullpath = 'durdraw/help/durhelp-256-page2.dur'
    ui = ui_curses.UserInterface(app)
    return ui

class TestPixelChanges:
    def test_insert_char(self):
        'inserts a character at a specific position'
        # TODO: implement this test after extricating curses from the main UI code
        # ui = init_ui()
        # assert ui.mov.frames[0].content == [[' ']*80]*24
