import configparser

parser = configparser.ConfigParser()
parser.read('config.cfg')

for sect in parser.sections():
   print('Section:', sect)
   #for k,v in parser.items(sect):
   #   print(' {} = {}'.format(k,v))
   print()