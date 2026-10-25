from Menu import *
from MidiPlayer import *
from pathlib import Path
from time import sleep

class UiBuilder:
    def __init__(self):
        self.songSelectionMenuList: list[MenuItem] = []
        
        for path in Path("Songs").glob("*.mid"):
            menuTitle = str(path.stem)        
            self.songSelectionMenuList.append(MenuItem(
                title = menuTitle, 
                callback = lambda x = menuTitle: self.whenSongSelected(f"Songs/{x}.mid")
            )) 

        self.songPlayBackMenuList: list[MenuItem] = [
            MenuItem("Pause/Unpause", self.whenPlaybackPaused),
            MenuItem("Exit", self.whenPlaybackExited)
        ] 

        self.menu: Menu = Menu(self.songSelectionMenuList)
        self.player: MidiPlayer = MidiPlayer()

    def whenSongSelected(self, path: str):
        self.player.startPlayback(path)
        self.menu = Menu(self.songPlayBackMenuList)

        #Prevent doubled inputs in the menu
        sleep(0.5)

    def whenPlaybackPaused(self):
        if self.player.isPlaying:
            self.player.pausePlayback()
        else:
            self.player.startPlayback()


    def whenPlaybackExited(self):
        self.player.stopPlayback()
        self.menu = Menu(self.songSelectionMenuList)
        
        #Prevent doubled inputs in the menu
        sleep(0.5)
        
 
if __name__ == "__main__":
    ui: UiBuilder = UiBuilder()
    
    while True:
        ui.menu.update()
        ui.menu.render()

        sleep(0.1)
