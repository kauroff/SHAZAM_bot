# Документация по телеграм-боту

## Функционал
Телеграм бот получает на вход название трека/имя исполнителя/строчки(слова) из песни или фрагмент мелодии(посредством голосового сообщения), ищет совпадения и возвращает список треков с обложками(функция возврата обложек пока отключена для минимизации задержки отклика).
Обрабатывает исключения если трека по заданным параметрам найдено не было (такое возможно, тк бд, к которой подключается бот, неполная, или бот не смог распознать мелодию).
Предлагает найти еще какую-нибудь мелодию.

## Разработка
Бот использует сгенерированный телеграм токен.
Подключается к сервису [по поиску трека по ключевым словам](https://rapidapi.com) по API.\n
Подключается к сервису [по поиску трека по звучанию](https://audiotag.info/) по API.
Использует библиотеку Telebot.
Запускается на локальной машине.

## Принцип работы
В случае поиска по ключевым словам - просто подключается к бд и ищет совпадения (поэтому при запросе по ключевым словам возвращается до 5 совпадений).
В случае поиска по звучанию - бот скачивает аудиодорожку(голосовое сообщение) формата .ogg, отправляет файл на удаленный сервер, где аудиодорожка конвертируется сначала в необработанный аудиофайл, после в битовую строку base64, по этим данным строится спектрограмма, на спектрограмме находятся ключевые точки; по ключевым точкам ищутся совпадения.
Отчего поиск по аудиодорожке не всегда успешный. 
Причины неудачи при поиске:
1) запись на микрофон с шумами
2) оправка на удаленный сервер с возможной потерей данных
3) конвертация с возможной потерей данных
