from Engi1020Interface import *
from typing import Callable
from time import sleep

class MenuItem:
    def __init__(self, title: str = "Lorem Ipsum", callback : Callable[[None], None] = lambda: print("Debug")) -> None:
        self.title: str = title
        self.callback: Callable[[None], None] = callback

class Menu:
    def __init__(self, items: list[MenuItem]) -> None:
        self.__items: list[MenuItem] = items

        self.__isButtonPressed: bool = False
        self.__isDirty: bool = False
        self.__selectedIdx: int = -1 
        self.__renderedRange: range = range(0, min(4, len(items)))
    
    def __updateScrolling(self) -> None:
        scrollPrecent: float = Arduino.call(Arduino.Api.analog_read, 0) / 1023
        newSelectedIdx: int = round(scrollPrecent * (len(self.__items) - 1))
        
        if newSelectedIdx == self.__selectedIdx:
            return

        #Modify scrolling like an IPod
        startIdx: int = self.__renderedRange.start
        endIdx: int = self.__renderedRange.stop
        
        if newSelectedIdx >= endIdx:
            endIdx = newSelectedIdx + 1
            startIdx = endIdx - 4
        elif newSelectedIdx < startIdx:
            startIdx = newSelectedIdx
            endIdx = startIdx + 4

        self.__renderedRange = range(max(0, startIdx), min(endIdx, len(self.__items)))
        self.__selectedIdx = newSelectedIdx
        self.__isDirty = True
    
    def __updateSelection(self) -> None:
        newIsButtonPressed: bool = Arduino.call(Arduino.Api.digital_read, 6)

        if newIsButtonPressed and not self.__isButtonPressed:
            self.__items[self.__selectedIdx].callback()

        self.__isButtonPressed = newIsButtonPressed

    def update(self) -> None:
        self.__updateScrolling()
        self.__updateSelection()

    def render(self) -> None:
        if not self.__isDirty:
            return

        Arduino.call(Arduino.Api.oled_clear)

        for i in self.__renderedRange:
            Arduino.call(Arduino.Api.oled_print, f"{'-' if i == self.__selectedIdx else ' '}{self.__items[i].title:.15}")

        self.__isDirty = False

#Menu test
if __name__ == "__main__":
    menuTest: Menu = Menu(items = [
        MenuItem("Song1", lambda: print("Song1 selected")), 
        MenuItem("Song2", lambda: print("Song2 selected")),
        MenuItem("Song3", lambda: print("Song3 selected")), 
        MenuItem("Song4", lambda: print("Song4 selected")), 
        MenuItem("Song5", lambda: print("Song5 selected")), 
        MenuItem("Song6", lambda: print("Song6 selected")), 
        MenuItem("Song7", lambda: print("Song7 selected")), 
        MenuItem("Song8", lambda: print("Song8 selected")), 
        MenuItem("Song9", lambda: print("Song9 selected")), 
        MenuItem("Song10", lambda: print("Song10 selected")), 
    ])

    while True:
        menuTest.update()
        menuTest.render()
        sleep(0.1)