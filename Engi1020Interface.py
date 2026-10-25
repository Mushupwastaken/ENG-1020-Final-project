from threading import Lock

'''
This class had to me made because the lib doesnt support threading by default
Shitty mutex impl
'''

class Arduino:
    import engi1020.arduino.api as Api
    __arduinoLock = Lock()

    @staticmethod
    def call(callback, *args, **kwargs):
        with Arduino.__arduinoLock:
            return callback(*args, **kwargs)