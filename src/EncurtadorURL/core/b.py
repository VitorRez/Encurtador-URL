from database.repositories.usuario import *

print(get_users())
print(get_user('VitorRezendeSilva'))
print(verify_password('VitorRezendeSilva', '3684deug'))
print(verify_password('VitorRezendeSilva', 'aaaaaaaa'))