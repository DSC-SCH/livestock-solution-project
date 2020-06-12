import pandas as pd
import pymysql
import numpy as np

# data추출 - 수정
def select_all_weather():
    conn = pymysql.connect(host='localhost', user = 'root', password = 'seonga',db='ddd')
    try:
        with conn.cursor() as curs:
            sql = "select * from weather"
            curs.execute(sql)
            rs = curs.fetchall()
            date_lst = []
            avg_ta_lst = []
            max_ta_lst = []
            min_ta_lst = []
            sum_rn_lst = []
            sum_sshr_lst = []
            max_insws_lst = []
            max_ws_lst = []
            sum_gsr_lst = []
            avg_ts_lst = []
            min_rhm_lst = []
            avg_rhm_lst = []
            avg_ws_lst = []
            gr1_maxicsr_lst = []

            for row in rs:
                date_lst.append(row[0])
                avg_ta_lst.append(row[1])
                max_ta_lst.append(row[2])
                min_ta_lst.append(row[3])
                sum_rn_lst.append(row[4])
                sum_sshr_lst.append(row[5])
                max_insws_lst.append(row[6])
                max_ws_lst.append(row[7])
                sum_gsr_lst.append(row[8])
                avg_ts_lst.append(row[9])
                min_rhm_lst.append(row[10])
                avg_rhm_lst.append(row[11])
                avg_ws_lst.append(row[12])
                gr1_maxicsr_lst.append(row[13])

            date_df = pd.DataFrame(date_lst, columns=['date'])
            avg_ta_df = pd.DataFrame(avg_ta_lst, columns=['avg_ta'])
            max_ta_df = pd.DataFrame(max_ta_lst, columns=['max_ta'])
            min_ta_df = pd.DataFrame(min_ta_lst, columns=['min_ta'])
            sum_rn_df = pd.DataFrame(sum_rn_lst, columns=['sum_rn'])
            sum_sshr_df = pd.DataFrame(sum_sshr_lst, columns=['sum_sshr'])
            max_insws_df = pd.DataFrame(max_insws_lst, columns=['max_insws'])
            max_ws_df = pd.DataFrame(max_ws_lst, columns=['max_ws'])
            sum_gsr_df = pd.DataFrame(sum_gsr_lst, columns=['sum_gsr'])
            avg_ts_df = pd.DataFrame(avg_ts_lst, columns=['avg_ts'])
            min_rhm_df = pd.DataFrame(min_rhm_lst, columns=['min_rhm'])
            avg_rhm_df = pd.DataFrame(avg_rhm_lst, columns=['avg_rhm'])
            avg_ws_df = pd.DataFrame(avg_ws_lst, columns=['avg_ws'])
            gr1_maxicsr_df = pd.DataFrame(gr1_maxicsr_lst, columns=['gr1_maxicsr'])

            data = pd.concat([date_df,avg_ta_df, max_ta_df, min_ta_df, sum_rn_df, sum_sshr_df, max_insws_df, max_ws_df,
                              sum_gsr_df, avg_ts_df, min_rhm_df, avg_rhm_df, avg_ws_df, gr1_maxicsr_df],axis=1)

            data = data.fillna(method='ffill')

            data_group = data.group_by(['date']).mean()

    finally:
        conn.close()

    return data_group


def mean_week(data_group):

    day_7 = pd.date_range(start=data_group['date'][0], end=data_group['date'][len(data_group) - 1], freq='W')  # 주별 데이터 생성
    day_7 = pd.DataFrame(day_7, columns=['week_date'])

    avg_7 = []

    for x in range(len(day_['week_date']) - 1):

        a = []

        for i in range(len(data['date'])):

            if data_group['date'][i] >= day_['week_date'][x] and data_group['date'][i] < day_['week_date'][x + 1]:
                a.append(avg_column[i])

        avg_7.append(np.mean(a))

    return avg_7

features = ['avg_ta','max_ta','min_ta','sum_rn','sum_sshr','max_insws','max_ws','sum_gsr','avg_ts','min_rhm','avg_rhm','avg_ws','gr1_maxicsr']

df = pd.DataFrame()

for col_name in features:
    df[col_name] = mean_week(select_all_weather[col_name])

df = pd.concat([day_7,df],axis=1)