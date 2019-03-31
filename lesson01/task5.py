# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.

import subprocess
ya = subprocess.check_output(['ping', '-c1', 'yandex.ru']).decode()
print(ya)


you = subprocess.check_output(['ping', '-c1', 'youtube.com']).decode()
print(you)
