import numpy as np
from flask import Flask, jsonify, abort, make_response

import pandas as pd
import translators as ts

app = Flask(__name__)

dtypes_dict = {  # админ коды с сс2 вроде неопределились в DataFrame вроде
    9: str,
    10: str,
    11: str,
    12: str,
    13: str,
}
f_df = pd.read_csv("RU.txt", sep="\t", header=None, names=['geonameid', 'name', 'asciiname', 'alternatenames',
                                                           'latitude', 'longitude', 'feature class', 'feature code',
                                                           'country code', 'cc2 ', 'admin1 code', 'admin2 code',
                                                           'admin3 code', 'admin4 code', 'population', 'elevation',
                                                           'dem', 'timezone', 'modification date'], dtype=dtypes_dict)
# так проще обращаться к файлу

data = f_df[f_df['feature code'].isin(['PPL', 'PPLC', 'PPLA'])]
# города, села, деревни. Мб feature class мог помочь но о нем не описано в readme


@app.route('/geonameid=<int:geo_id>')  # информация о городе по geonameid
def city_detail(geo_id):
    if len(data[data['geonameid'] == geo_id]) == 0:
        abort(404)
    return jsonify(data[data['geonameid'] == geo_id].to_dict('index'))
    # to_dict вместо to_json, просто чтобы ответ был все таки json, а не str


@app.route('/page=<int:page>/count=<int:count>')  # список городов с их информацией
def city_list(page, count):
    max_pages = len(data) // count
    if len(data) % count:
        max_pages += 1  # добавляем оставшуюся неполную страницу, что бы не усложнять вывод

    if page > max_pages:
        abort(404)
    elif page == max_pages:
        return jsonify(data[count * (page - 1):count * (page - 1) + len(data) % count].to_dict('index'))
    else:
        return jsonify(data[count * page:count * page + count].to_dict('index'))
    # to_dict вместо to_json, просто чтобы ответ был все таки json, а не str


@app.route('/compare/<first_city>/<second_city>')  # информация о результате сравнения
def compare_page(first_city, second_city):
    first_df = data[data['name'] == ts.google(first_city.capitalize())]
    second_df = data[data['name'] == ts.google(second_city.capitalize())]
    # названия в бд странные то переведеннве то транслитом

    first_df = first_df.sort_values('population', kind='mergesort', ascending=False)[:1]
    second_df = second_df.sort_values('population', kind='mergesort', ascending=False)[:1]
    # отбор из совпавшихся городов

    if len(first_df) and len(second_df):

        if first_df['latitude'].iloc[0] > second_df['latitude'].iloc[0]:
            north_city = first_df['name'].iloc[0]
        else:
            north_city = second_df['name'].iloc[0]
        # определение более северного города
        return jsonify(
            {'north_city': north_city, 'same_zone': first_df['timezone'].iloc[0] == second_df['timezone'].iloc[0]})
    else:
        abort(404)


@app.route('/proposed/<city_name>')  # список предложенных городов
def proposed_city(city_name):
    pr_df = data[data['name'].str.startswith(city_name.capitalize())]
    # отбор значений начинающихся с введенного занчения
    if len(pr_df):
        return jsonify(pr_df['name'].drop_duplicates().to_list())
    else:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

