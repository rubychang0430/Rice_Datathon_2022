from datetime import datetime, timedelta
import pandas as pd


def convert_to_df(target_url):
    df = pd.read_csv(target_url, sep='\s+')
    df = df[1:]
    df = df.drop(['WVHT', 'DPD', 'APD', 'MWD', 'PRES', 'WTMP', 'PTDY', 'TIDE', 'GST'], axis=1)
    df = df.replace(['MM'],'nan')
    rest = df.iloc[:,5:].astype(float)
    first = df.iloc[:,:5]
    df = pd.concat([first, rest],axis=1)
    df.rename(columns = {'#YY':'YY'},inplace=True)
    df['date'] = df['YY']+'-'+df['MM']+'-'+df['DD']
    df['time'] = df['hh']+':'+df['mm']
    df['datetime'] = pd.to_datetime(df['date']+' '+df['time'])
    df=df[1:]
    df.reset_index(drop = True, inplace = True)
    return df
    
def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
    
def generate_datetime(df):
    start_time = df['datetime'][len(df)-1]
    end_time = df['datetime'][0]
    dts = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in 
       datetime_range(start_time.to_pydatetime(), end_time.to_pydatetime(),timedelta(minutes=20))]
    dts.sort(reverse = True)
    df2=pd.DataFrame()
    df2['datetime'] = pd.to_datetime(dts)
    df1 = df2.merge(df, on='datetime', how='left')
    return df1
    
def final_df(target_url):
    df = convert_to_df(target_url)
    df1 = generate_datetime(df)
    df1 = df1.drop(['YY', 'MM', 'DD', 'hh', 'mm', 'time'], axis=1)
    df1['date'] = pd.to_datetime(df1['datetime']).dt.date
    df1.set_index('datetime', inplace = True)
    df1.interpolate(limit_direction="both",inplace=True)
    df1 = df1[::-1]
    return df1
