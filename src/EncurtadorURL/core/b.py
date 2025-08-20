from database.repositories.usuario import *
from database.repositories.short_url import *

print(get_users())
print(get_user('VitorRezendeSilva'))
print(verify_password('VitorRezendeSilva', '3684deug'))
print(verify_password('VitorRezendeSilva', 'aaaaaaaa'))

create_short_url('https://ufsj.edu.br/', 'VitorRezendeSilva')

print(get_short_urls())