# REST API для предоставления информации по географическим объектам.

_REST API-сервис для получения информации географических объектов_ — это интерфейс, который позволяет запрашивать информацию о городах с помощью http-запросов к специальному серверу. 

# Оглавление

1. [Установка зависимостей](#Установка_зависимостей)
2. [Запуск сервера](#Запуск_сервера)
3. [Запросы](#Запросы)


# Установка_зависимостей

Для установки зависимостей необходимо в терминале virtuallenv выполнить
	
```
pip3 install -r requirements.txt
```

# Запуск_сервера

Чтобы запустить сервер необходимо выполнить python-файл main.py

```
./python main.py
```	

# Запросы

Все запросы отправляются по адресу

```
http://127.0.0.1:8000/
```

Список запросов:
1. [Получение информации о городе по geonamedid](#Метод_1)
2. [Получение списка городов с их информацией](#Метод_2)
3. [Получение информаци о результате сравнения двух городов](#Метод_3)
4. [Получение списка предложенных городов](#Доп_метод)

## Метод_1

### Request

В запросе необходимо указать geonamedid нужного города России
 
`GET /geonameid=524901`

### Response

Сервер возвращает всю информацию о городе из предоставленного файла RU.txt

```
    200 OK
    {
    "64199": {
        "admin1 code": "48",
        "admin2 code":NaN,
        "admin3 code":NaN,
        "admin4 code":NaN,
        "alternatenames": "MOW,Maeskuy,Maskav,
        "asciiname": "Moscow",
        "cc2 ":NaN,
        "country code": "RU",
        "dem": 144,
        "elevation":NaN,
        "feature class": "P",
        "feature code": "PPLC",
        "geonameid": 524901,
        "latitude": 55.75222,
        "longitude": 37.61556,
        "modification date": "2020-03-31",
        "name": "Moscow",
        "population": 10381222,
        "timezone": "Europe/Moscow"
    	}
    }
```

## Метод_2

### Request

В запросе необходимо указать кол-во страниц и кол-во записей на странице
 
`GET /page=4/count=1`

### Response

Сервер возвращает список n-го кол-ва городов на k-ой странице

```
    200 OK
    {
    "4": {
        "admin1 code": "77",
        "admin2 code":NaN,
        "admin3 code":NaN,
        "admin4 code":NaN,
        "alternatenames":NaN,
        "asciiname": "Zhitnikovo",
        "cc2 ":NaN,
        "country code": "RU",
        "dem": 198,
        "elevation":NaN,
        "feature class": "P",
        "feature code": "PPL",
        "geonameid": 451751,
        "latitude": 57.20064,
        "longitude": 34.57831,
        "modification date": "2011-07-09",
        "name": "Zhitnikovo",
        "population": 0,
        "timezone": "Europe/Moscow"
    	}
   }
```

## Метод_3

### Request

В запросе необходимо указать два города для сравнения на русском языке

`GET /compare/Москва/томск`

### Response

Сервер возвращает результаты сравнения:
	1. Какой город севернее
	2. Одинакова ли у городов временная зона
	
```
200 OK
    {
    	"north_city": "Tomsk",
	"same_zone": false
    }
```

## Доп_метод

### Request

В запросе необходимо указать первые символы названия города
 
`GET /proposed/toms`

### Response

Сервер возвращает список возможных городов

```
 200 OK
    [
    	"Tomsharovo",
	"Tomskoye",
	"Tomskiy Khutor",
	"Tomskaya",
	"Tomsk",
	"Tomsyu",
	"Tomsino"
    ]
```