import pandas as pd
import pmdarima as pm
from datetime import datetime, timedelta

def datetime_new_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
        
def generate_new_datetime(df):
    start_time = df.index[-1]
    end_time = start_time + timedelta(days=3)
    dts = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in 
       datetime_new_range(start_time.to_pydatetime(), end_time.to_pydatetime(),timedelta(minutes=20))]
    df1=pd.DataFrame(dts, columns=['datetime'])
    df1.set_index('datetime', inplace = True)
    return df1


def forecast(df):
    """
    WDIR
    """
    history = df.drop('date',axis=1)
    test = generate_new_datetime(df)
    tr_extro_WDIR = history.loc[:, history.columns != 'WDIR']
    xmodel_WDIR = pm.arima.auto_arima(y = history["WDIR"], X = tr_extro_WDIR, 
                           start_p = 2, max_p = 5,
                           start_q = 10, max_q = 25)
    
    # Forecast
    WDIR_pred, confit_WDIR = xmodel_WDIR.predict(n_periods = 72*3, X = tr_extro_WDIR.iloc[-72*3:],return_conf_int=True)

    # Make as pandas series
    fc_WDIR = pd.Series(WDIR_pred, index = test.index)
    lower_WDIR = pd.Series(confit_WDIR[:, 0], index = test.index)
    upper_WDIR = pd.Series(confit_WDIR[:, 1], index = test.index)
    
    """
    WSPD
    """
    tr_extro_WSPD = history.loc[:, history.columns != 'WSPD']
    xmodel_WSPD = pm.arima.auto_arima(y = history["WSPD"], X = tr_extro_WSPD, 
                               start_p = 2, max_p = 5,
                               start_q = 10, max_q = 25) 

    # xmodel_WSPD.summary()
    # Forecast
    WSPD_pred, confit_WSPD = xmodel_WSPD.predict(n_periods = 72*3, X = tr_extro_WSPD.iloc[-72*3:],return_conf_int=True)

    # Make as pandas series
    fc_WSPD = pd.Series(WSPD_pred, index = test.index)
    lower_WSPD = pd.Series(confit_WSPD[:, 0], index = test.index)
    upper_WSPD = pd.Series(confit_WSPD[:, 1], index = test.index)
    
    return fc_WDIR,lower_WDIR,upper_WDIR,fc_WSPD,lower_WSPD,upper_WSPD