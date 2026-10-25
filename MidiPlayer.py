from Engi1020Interface import *
from threading import Thread, Lock, current_thread
from time import time, sleep
from mido import MidiFile, Message



class MidiPlayer:
    def __init__(self) -> None:
        self.__player: Thread = Thread() 
        self.__playerLock: Lock = Lock()
        self.isPlaying: bool = True

    def __midiToFrequency(self, note: int) -> int:
        return max(31, min(65536, round(440.0 * (2.0 ** ((note - 69) / 12.0)))))

    def __busyWait(self, duration: float) -> None: 
            startTime: float = time()
            timeElapsed: float = 0.0
            
            while timeElapsed < duration:
                sleep(0.005)
                
                if not self.isPlaying:                    
                    startTime = time() - timeElapsed
                    continue
            
                timeElapsed = time() - startTime
    
    def __playMusic(self, path: str) -> None:
        try:
            midi = MidiFile(path)
            print(f"Loaded {path}")
        except Exception as e:
            print(f"err: {e}")
            return

        activeNotes: list[Message] = []
        
        for message in midi:
            if current_thread() != self.__player:
                return

            if message.time > 0.0:
                if activeNotes:
                    Arduino.call(Arduino.Api.buzzer_frequency, 5, self.__midiToFrequency(max(activeNotes)))
                else:
                    Arduino.call(Arduino.Api.buzzer_stop, 5)
                    
                self.__busyWait(message.time)

            if message.type == "note_on" and message.note not in activeNotes:
                activeNotes.append(message.note)
                
            elif message.type == "note_off" and message.note in activeNotes:
                activeNotes.remove(message.note)
                    
        Arduino.call(Arduino.Api.buzzer_stop, 5)


    def startPlayback(self, path: str | None = None) -> None:
        self.isPlaying = True

        with self.__playerLock:
            if not self.__player.is_alive():
                self.__player = Thread(target=self.__playMusic, args = [path])
                self.__player.start()
    
    def pausePlayback(self) -> None:
        self.isPlaying = False
        
        sleep(0.05)
        Arduino.call(Arduino.Api.buzzer_stop, 5)

    def stopPlayback(self) -> None:
        self.__player = Thread()
        self.isPlaying = False

        sleep(0.05)
        Arduino.call(Arduino.Api.buzzer_stop, 5)

#CLI Test
if __name__ == "__main__":
    playerTest : MidiPlayer = MidiPlayer()

    while True:
        command: str = input("Command:\t").lower()

        if command == "play":
            playerTest.startPlayback("Songs/test.mid")
        elif command == "pause":
            playerTest.pausePlayback()
        elif command == "stop":
            playerTest.stopPlayback()
        else:
            print("Unknown command")
