from binance.client import Client
import pandas as pd
import psycopg2 
from sqlalchemy import create_engine 
import joblib
import tritonclient.http as httpclient
import numpy as np

def GetHistoricalData(until_date = '2024-03-15'):

    api_key = ('5C9nlellYmjpT7hGY1RwtCqafHEiB718aYptf2gH233vVxAIc1XG1WEgwuss4sKb')
    api_secret = ('qEOCX9cOU4n3WMex3PTi8U8IlTEp2DQfKKlZYvHTFaQ3GB0AUTeos3P2Iff5CipA')
    client = Client(api_key, api_secret)

    since_date = '2020-01-01'
 
    candle = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, since_date, until_date)

    df = df = pd.DataFrame(candle, columns=['dateTime', 'open', 'high', 'low', 'close', 
                                            'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 
                                            'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])

    df.dateTime = pd.to_datetime(df.dateTime, unit='ms').dt.strftime('%Y-%m-%d %H:%m')

    df = df.drop(columns = ['high', 'low', 'close', 'volume', 
                            'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol',
                            'takerBuyQuoteVol', 'ignore'])
    df.reset_index(drop=False, inplace=True)
    df.columns = ['id', 'date_open', 'value_open']

    conn_string = 'postgresql+psycopg2://test_user:test_password@db:5432/test'

    db = create_engine(conn_string) 
    conn = db.connect() 
    conn1 = psycopg2.connect( 
        database="test", 
        user='test_user',  
        password='test_password',  
        host='db',  
        port= '5432'
    ) 
    
    conn1.autocommit = True
    cursor = conn1.cursor() 
    
    cursor.execute("drop table if exists btc_historical;") 
    
    sql = "CREATE TABLE btc_historical (id SERIAL PRIMARY KEY, date_open varchar(40), value_open numeric(10, 3));"
    
    cursor.execute(sql) 
    
    df.to_sql('btc_historical', conn, if_exists= 'replace', index=False) 
        
    conn1.commit() 
    conn1.close() 
    cursor.close()
    conn.commit()
    conn.close()


def GetPrediction():
    scaler = joblib.load("app/data/scaler.joblib")

    conn1 = psycopg2.connect( 
        database="test", 
        user='test_user',  
        password='test_password',  
        host='db',  
        port= '5432'
    ) 
    
    conn1.autocommit = True
    cursor = conn1.cursor()  
    
    sql = "SELECT * FROM btc_historical ORDER BY id desc LIMIT 200;"
    
    cursor.execute(sql)
    
    df = pd.DataFrame(cursor.fetchall())
    df.columns = ['id', 'open_date', 'open']
    df.drop(columns=['id', 'open_date'], inplace = True)

    conn1.commit() 
    conn1.close() 
    cursor.close()

    X = scaler.transform(df)
    X = X.astype(np.float32)
    X = X[::-1]
    
    X_val = X[:100]
    real = X[100:]
    X_test = X[100:]
    y_val = np.array(dtype = np.float32)

    for i in range(100):
        client = httpclient.InferenceServerClient(url="inference-service:8000")

        inputs = httpclient.InferInput("input__0", X_val.shape, datatype="FP32")
        inputs.set_data_from_numpy(X_val)

        outputs = httpclient.InferRequestedOutput(
        "output__0"
        )

        results = client.infer(model_name="btcmodel", inputs=[inputs], outputs=[outputs])
        inference_output = results.as_numpy("output__0")

        y_val = np.append(y_val, inference_output)
        X_test = np.append(X_test, real[i])
        X_test = X_test[1:]
        X_test = np.reshape(X_test, (100, 1))

    for _ in range(100):
        client = httpclient.InferenceServerClient(url="inference-service:8000")

        inputs = httpclient.InferInput("input__0", X_test.shape, datatype="FP32")
        inputs.set_data_from_numpy(X_test)

        outputs = httpclient.InferRequestedOutput(
        "output__0"
        )

        # Querying the server
        results = client.infer(model_name="btcmodel", inputs=[inputs], outputs=[outputs])
        inference_output = results.as_numpy("output__0")

        X_test = np.append(X_test, inference_output)
        X_test = X_test[1:]
        X_test = np.reshape(X_test, (100, 1))

    real_inversed = scaler.inverse_transform(pd.DataFrame(real))
    val_inversed = scaler.inverse_transform(pd.DataFrame(y_val))
    test_inversed = scaler.inverse_transform(pd.DataFrame(real))

    json_output = {
        'real' : np.reshape(real_inversed, (100)).tolist(),
        'val' : np.reshape(val_inversed, (100)).tolist(),
        'test' : np.reshape(test_inversed, (100)).tolist()
        }
    
    return json_output


