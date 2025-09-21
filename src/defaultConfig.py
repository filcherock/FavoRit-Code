from pickledb import PickleDB

config = PickleDB('config.json')

# Config for window
config.set('font', 'Coloras 15')
config.set('bg', '#303030')
config.set('fg', '#FFFFFF')
# ====================================
config.set('num_color', '#808080')

# Config for syntax
config.set('syntax_normal', '#eaeaea')
config.set('syntax_keyword', '#ea5f5f')
config.set('syntax_func', '#00B2C2')
config.set('syntax_comment', '#5feaa5')
config.set('syntax_str', '#eaa25f')

# Save config to config.json
config.save()