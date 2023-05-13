# FTPClient
Develop functionality to work with FTP protocol using Python

---

Программа является реализацией FTP-клиента, способного обмениваться множеством файлов с сервером. Python-скрипт использует библиотеку *os* для работы с FTP-протоколом.

**API**:
* **`ftp_isdir(path)`** - проверяет, находится ли по заданному пути *path* каталог.

* **`ftp_makedirs(paths, ftp)`** - для заданного пути *path* создает не существующие каталоги, содержащиеся в пути.

* **`ftp_upload(path_local, path_server, file_name_time=False, upload_dirs=True)`** - Загружает на сервер по пути *path_server* локальные файлы, находящиеся по пути *path_local*. *file_name_time* – если `True`, то создает папку с уникальным именем в формате "%Дата% %Время%", куда будут загружены файлы. *upload_dirs* – если `True`, то помимо файлов из каталога path_local, на сервер будут также загружены и какталоги с их содержимым.

* **`ftp_download( path_local='ftp_downloaded', file_name_time=False, download_dirs=True)`** - Скачивает с текущего каталога на сервере содержиме на локальный путь path_local. *file_name_time* – аналогичен параметру функции *`ftp_upload(...)`*. *download_dirs* – если `True`, то помимо файлов с сервера будут также скачаны и какталоги с их содержимым.

#### Пример работы с API. Загрузка на сервер:

Код скрипта:
```Python
from ftp_client_updownload import *
# Переход в нужную папку на сервере и изменение кодировки
path_to_server = 'data_ftp'
ftp.encoding = 'utf-8'  # Оптимальная кодировка для Ru/En
ftp_upload('local_data/', path_to_server)
```

*Исходные данные локального каталога*

![Pasted image 20230512221723](https://github.com/rusanoph/FTPClient/assets/70108263/3a0d756a-893a-4864-9363-4a1c4f04e54b)

*Служебная информация о ходе загрузки*

![Pasted image 20230512221747](https://github.com/rusanoph/FTPClient/assets/70108263/9d7755ba-c99b-45fa-9964-5286c4c90401)

*Содержимое каталога на сервере*

![Pasted image 20230512221840](https://github.com/rusanoph/FTPClient/assets/70108263/46779f71-6fb1-4d09-93fc-59750b7a2292)


#### Пример работы с API. Скачивание с сервера:

Код скрипта:
```Python
from ftp_client_updownload import *
# Переход в нужную папку на сервере и изменение кодировки
path_to_server = 'data_ftp'
ftp.encoding = 'utf-8'  # Оптимальная кодировка для Ru/En
ftp.cwd(path_to_server)
path_to_local = 'ftp_dowloaded'
# Параметр download_dirs установлен как False => скачиваем только файлы
ftp_download(path_to_local, file_name_time=False, download_dirs=False)
```

*Содержимое каталога на сервере*

![Pasted image 20230512222322](https://github.com/rusanoph/FTPClient/assets/70108263/9f489d03-a5ea-4637-a6fa-b9ac29c0f32f)


*Служебная информация о ходе скачивания*

![Pasted image 20230512222329](https://github.com/rusanoph/FTPClient/assets/70108263/a2c732be-df24-4125-b1fc-c4f4ce522a8f)


*Содержимое локального каталога*

![Pasted image 20230512222401](https://github.com/rusanoph/FTPClient/assets/70108263/1a2bcb6d-3906-480b-9618-1341cce74574)


Видно, что содержимое совпадает с содержимым каталога data_ftp на FTP сервере.
