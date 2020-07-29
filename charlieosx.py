from robot import Charlie


def loadSettings():
    order = ['Debug Driving', 'Audio-Volume', 'EFX-Volume', 'Console-Log', 'Show Warnings', 'Show Errors']
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        sorted_settings = OrderedDict()
        sorted_settings['options'] = OrderedDict()
        for i in range(len(order)):
            sorted_settings['options'][order[i]] = settings['options'][order[i]]
        sorted_settings['values'] = settings['values']
        sorted_settings['types'] = settings['types']
        return sorted_settings

def storeSettings(data):
    with open('settings.json', 'w') as f:
        f.write(json.dumps(data, sort_keys = False))

def applySettings(settings):
    charlie.speaker.set_volume(settings['options']['Audio-Volume'] * 0.9, 'Beep')
    charlie.speaker.set_volume(settings['options']['EFX-Volume'] * 0.9, 'PCM')

settings = OrderedDict({'options': OrderedDict({'Debug Driving': 2, 'Audio-Volume': 80, 'EFX-Volume': 25, 'Console-Log': True, 'Show Warnings': True, 'Show Errors': True}),
            'values': {
                'min': {'Debug Driving': 0, 'Audio-Volume': 0, 'EFX-Volume': 0, 'Console-Log': False, 'Show Warnings': False, 'Show Errors': False},
                'max': {'Debug Driving': 2, 'Audio-Volume': 100, 'EFX-Volume': 100, 'Console-Log': True, 'Show Warnings': True, 'Show Errors': True}},
            'types': {'Debug Driving': 'int', 'Audio-Volume': 'int', 'EFX-Volume': 'int', 'Console-Log': 'bool', 'Show Warnings': 'bool', 'Show Errors': 'bool'}
            })


settings = loadSettings()