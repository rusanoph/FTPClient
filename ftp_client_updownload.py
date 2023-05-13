from config import *
import os
from datetime import datetime


def ftp_isdir(path):
    # Проверяет, находится ли по заданному пути папка
    try:
        ftp.cwd(path)
        ftp.cwd('..')
        return True
    except ftplib.error_perm:  # Permanent Error. Code 500 - 599
        return False


def ftp_makedirs(paths, ftp):
    paths = paths.replace('\\', '/').split('/')
    n = len(paths)
    init_path = ftp.pwd()

    for i in range(n):
        ftp.mkd(paths[i])
        ftp.cwd(paths[i])

    ftp.cwd(init_path)


def ftp_upload(path_local, path_server, file_name_time=False, upload_dirs=True):
    '''
    Загружает на сервер по пути path_server локальные файлы, находящиеся по пути path_local.
    file_name_time - если True, то создает папку с уникальным именем в формате "%Дата% %Время%", куда
    будут загружены файлы
    upload_dirs - если True, то помимо файлов из каталога path_local, на сервер будут также загружены
    и какталоги с их содержимым
    '''
    start_time = datetime.now()  # Начало отсчета передачи файлов
    datetime_now = ''
    count_uploaded_files = 0  # Кол-во переданных файлов
    ftp_start_path = ftp.pwd()  # Нужно, чтобы после всех переходов, вернуться в исходное положение

    # Если на сервере не существует указанного пути - создать и перейти в него
    if not ftp_isdir(path_server):
        ftp_makedirs(path_server, ftp)
    ftp.cwd(path_server)

    # Установка текущего времени в качестве имени папки
    if file_name_time:
        datetime_now = str(datetime.now().strftime("%Y-%m-%d %H;%M;%S"))
        ftp.mkd(datetime_now)
        ftp.cwd(datetime_now)

    # Формируем содержимое папки
    local_filenames = os.listdir(path_local)
    for local_filename in local_filenames:
        full_path_file = os.path.join(path_local, local_filename)
        count_uploaded_files += 1

        # Если текущий файл является папкой, то производится рекурсивный вызов закачки
        # файлов из данной локальной папки
        if os.path.isdir(full_path_file):
            if upload_dirs:
                print(f'{count_uploaded_files}) Download directory "{local_filename}":')
                ftp_upload(full_path_file, local_filename)  # Рекурсивный вызов
                print()
            else:
                print(f'{count_uploaded_files}) Directory "{local_filename}" is not a file.')
            continue

        # Закачка файла и вывод информации о нем
        with open(full_path_file, 'rb') as file:
            start_file_time = datetime.now()
            ftp.storbinary('STOR ' + local_filename, file, 1024)

            # Вывод информации о текущем файле в формате: (Время скачивания; Размер файла)
            print(f'{count_uploaded_files}) File "{local_filename}" successfully uploaded.',
                  f'\n(Time: {datetime.now() - start_file_time}; ',
                  f'Size: {os.path.getsize(full_path_file)} bytes)')

    ftp.cwd(ftp_start_path)  # Возврат в исходную папку, откуда функция начала работу

    print()
    print(f'Total download time: {datetime.now() - start_time} hh:mm:ss.')
    print(f'Number of transferred files: {count_uploaded_files}')
    print(f'Uploaded to path: {os.path.join(path_server, str(datetime_now))}')


def ftp_download(path_local='ftp_downloaded', file_name_time=False, download_dirs=True):
    '''
    Скачивает с текущего каталога на сервере содержиме на локальный путь path_local
    file_name_time - аналогичен параметру функции ftp_upload()
    download_dirs - если True, то помимо файлов с сервера будут также скачаны
    и какталоги с их содержимым
    '''
    start_time = datetime.now()
    datetime_now = ''
    count_downloaded_files = 0  # Кол-во переданных файлов

    # Установка текущего времени в качестве имени папки
    if file_name_time:
        datetime_now = str(datetime.now().strftime("%Y-%m-%d %H;%M;%S"))
        path_local = os.path.join(path_local, datetime_now)

    # Если указанной папки не существует - создать
    if not os.path.exists(path_local):
        # os.mkdir()  <- Создает одну папку
        os.makedirs(path_local)  # Создает указанный путь

    # Формируем содержимое папки
    server_filenames = ftp.nlst()
    for server_filename in server_filenames:
        full_path_file = os.path.join(path_local, server_filename)
        count_downloaded_files += 1

        # Если текущий файл является папкой, то производится переход в неё,
        # затем рекурсивный вызов выкачивания файлов из данной папки на сервере,
        # Возврат в исходное состояние
        if ftp_isdir(server_filename):
            if download_dirs:
                print(f'{count_downloaded_files}) Download directory "{server_filename}":')
                ftp.cwd(server_filename)
                ftp_download(full_path_file)  # Рекурсивный вызов
                ftp.cwd('..')
                print()
            else:
                print(f'{count_downloaded_files}) Directory "{server_filename}" is not a file.')
            continue

        # Скачивание файла и вывод информации о нем
        with open(full_path_file, 'wb') as file:
            start_file_time = datetime.now()  # Отсчет от начала скачиванияя текущего файла
            ftp.retrbinary('RETR ' + server_filename, file.write)

            # Вывод информации о текущем файле в формате: (Время скачивания; Размер файла)
            print(f'{count_downloaded_files}) File "{server_filename}" successfully downloaded.',
                  f'\n(Time: {datetime.now() - start_file_time}; ',
                  f'Size: {os.path.getsize(full_path_file)} bytes)')

    print()
    print(f'Total download time: {datetime.now() - start_time} hh:mm:ss.')  # Общее время скачивания
    print(f'Number of transferred files: {count_downloaded_files}')  # Общее число файлов и папок
    print(f'Downloaded to path: {os.path.join(path_local, str(datetime_now))}')

