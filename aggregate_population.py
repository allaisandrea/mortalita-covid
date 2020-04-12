import pandas
import sys

YEARS = (2015, 2016, 2017, 2018, 2019)

population_table = pandas.DataFrame()
for year in YEARS:
    print('Processing year: {}'.format(year))
    orig_table = pandas.read_csv('population-{}.csv'.format(year), skiprows=1)
    city_id_key = orig_table.columns[0]
    assert city_id_key in ['Codice comune', 'Codice Comune'], 'city_id_key: {}'.format(city_id_key)
    city_name_key = orig_table.columns[1]
    assert city_name_key in ['Nome Comune', 'Denominazione'], 'city_name_key: {}'.format(city_name_key)
    agg_table = orig_table.loc[orig_table.iloc[:, 2] < 999][
            [city_id_key, city_name_key, 'Totale Maschi', 'Totale Femmine']].groupby(
            [city_id_key, city_name_key]).sum().reset_index()
    population_table = population_table.append(pandas.DataFrame({
        'year': year,
        'city_id': agg_table[city_id_key],
        'city_name': agg_table[city_name_key],
        'population': agg_table['Totale Maschi'] + agg_table['Totale Femmine']},
        columns = ('city_id', 'city_name', 'year', 'population')))
population_table.to_csv('population.csv', index=False)
