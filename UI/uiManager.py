import _thread

from profileHelper import ProfileHelper
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

from UI import UIObject


class UIManager:
    def __init__(self, config, settings, brick, logger, settingsPath):

        # needed Stuff
        logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__settingsPath = settingsPath
        self.__click = 'assets/media/click.wav'
        self.__confirm = 'assets/media/confirm.wav'
        self.brick = brick
        self.logger = logger
        self.profileHelper = ProfileHelper(self.logger, self.__config)
        self.__sound_lock = _thread.allocate_lock()
        self.logger.info(self, 'UI initialized')

        # UI Stuff

        self.UIObjects = []
    
    def __sound(self, file):
        '''
        This private method is used for playing a sound in a separate thread so that other code can be executed simultaneously.

        Args:
            file (str / SoundFile): The path to the soundfile to play
        '''
        def __playSoundFile(soundFile):
            with self.__sound_lock:
                self.brick.speaker.play_file(soundFile)
        _thread.start_new_thread(__playSoundFile, (file, ))
    
    def addObject(self, UIObject):
        self.UIObjects.append(UIObject)

    def draw(self):
        for UIObject in self.UIObjects:
            UIObject.draw()