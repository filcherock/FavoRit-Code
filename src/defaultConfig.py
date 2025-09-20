from pickledb import PickleDB

config = PickleDB('config.json')

config.set('font', 'Coloras 15')
config.set('bg', '#303030')
config.set('fg', '#FFFFFF')
config.save()