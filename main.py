# !usr/env/bin python3
# -*- coding: utf8 -*-

from scipy.stats.stats import pearsonr
import pprint

def pearsonCorr(arr_a, arr_b):
    return pearsonr(arr_a, arr_b)[0]


def tvData(f = 'tv'):
    result = {}
    all_channels = {}
    src = open(f, 'r', encoding='utf8').read().split('\n')
    for line in src:
        city, channel, date, tvr = line.split('\t')
        all_channels[channel] = 1
        if city in result.keys():
            pass
        else:
            result[city] = {}
        if channel in result[city].keys():
            pass
        else:
            result[city][channel] = {}
        date = date.replace('.', '')
        tvr = float(tvr.replace(',', '.'))
        result[city][channel][date] = tvr
    # f = open('tv_arr.txt', 'r', encoding='utf8').read()
    # result = eval(f)
    all_channels = list(all_channels.keys())
    return result, all_channels


def nwData(f = 'nw'):
    result = {}
    src = open(f, 'r', encoding='utf8').read().split('\n')
    for line in src:
        city, ts, date, trans, conv = line.split('\t')
        if city in result.keys():
            pass
        else:
            result[city] = {}
        if ts in result[city].keys():
            pass
        else:
            result[city][ts] = {}
        if 'trans' in result[city][ts].keys():
            # trans operation
            date = date.replace('.', '')
            result[city][ts]['trans'][date] = int(trans)
        else:
            result[city][ts]['trans'] = {}
        if 'conv' in result[city][ts].keys():
            # conv operation
            date = date.replace('.', '')
            result[city][ts]['conv'][date] = int(conv)
        else:
            result[city][ts]['conv'] = {}
    return result

    
def getOrder():
    return [
        '26052018',
        '27052018',
        '28052018',
        '29052018',
        '30052018',
        '31052018',
        '01062018',
        '02062018',
        '03062018',
        '04062018',
        '05062018',
        '06062018',
        '07062018',
        '08062018',
        '09062018',
        '10062018',
    ]


def arrByOrder(dict):
    result = []
    order = getOrder()
    for i in order:
        try:
            result.append(dict[i])
        except Exception as e:
            result.append(0)
    return result


def main():

    fres = open('RESULT.txt', 'w', encoding='utf8')
    print('Город\tТелеканал\tИсточник трафика\tКорреляция по переходам\tКорреляция по заявкам', file=fres)

    # city tv_channel ts corr_trans corr_conv

    tv_data, all_tv_channels = tvData()
    nw_data = nwData()

    all_cities = list(set(list(tv_data.keys()) + list(nw_data.keys())))
    all_tss = [
        'Direct', 
        'Organic Search',
        'Paid Search',
        'Social'
        ]

    for city in all_cities:
        for channel in all_tv_channels:
            try:
                tv_channel_data = tv_data[city][channel]
                tv_channel_order = arrByOrder(tv_channel_data)
                for ts in all_tss:
                    ts_trans_data = nw_data[city][ts]['trans']
                    ts_trans_data_order = arrByOrder(ts_trans_data)
                    ts_conv_data = nw_data[city][ts]['conv']
                    ts_conv_data_order = arrByOrder(ts_conv_data)
                    line = '%s\t%s\t%s\t%s\t%s'%(city, channel, ts, pearsonCorr(tv_channel_order, ts_trans_data_order), pearsonCorr(tv_channel_order, ts_conv_data_order))
                    print(line, file=fres)

            except Exception as e:
                print(e)

    fres.close()
                

if __name__ == '__main__':
    main()