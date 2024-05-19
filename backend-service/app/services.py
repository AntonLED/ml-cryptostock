<<<<<<< HEAD
import sklearn
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import torch.utils.data as data
=======
from binance.client import Client
import datetime
import pandas as pd
import psycopg2 
from sqlalchemy import create_engine 
import joblib
import tritonclient.http as httpclient
from tritonclient.utils import triton_to_np_dtype
import numpy as np

def GetHistoricalData(until_date = '2024-03-15'):

    api_key = ('5C9nlellYmjpT7hGY1RwtCqafHEiB718aYptf2gH233vVxAIc1XG1WEgwuss4sKb')
    api_secret = ('qEOCX9cOU4n3WMex3PTi8U8IlTEp2DQfKKlZYvHTFaQ3GB0AUTeos3P2Iff5CipA')
    client = Client(api_key, api_secret)

    since_date = '2020-01-01'
 
    candle = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, since_date, until_date)

    df = df = pd.DataFrame(candle, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])

    df.dateTime = pd.to_datetime(df.dateTime, unit='ms').dt.strftime('%Y-%m-%d %H:%m')

    df = df.drop(columns = ['high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol','takerBuyQuoteVol', 'ignore'])
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
>>>>>>> parent of 8db6c19 (added validation and precictqueries)


def create_dataset(dataset):
    """Transform a time series into a prediction dataset

<<<<<<< HEAD
    Args:
        dataset: A numpy array of time series, first dimension is the time steps
        lookback: Size of window for prediction
    """
    return torch.reshape(torch.Tensor(dataset), (1, 100, 1))
=======
    conn1 = psycopg2.connect( 
        database="test", 
        user='test_user',  
        password='test_password',  
        host='db',  
        port= '5432'
    ) 
    
    conn1.autocommit = True
    cursor = conn1.cursor()  
    
    sql = "SELECT * FROM btc_historical ORDER BY id desc LIMIT 100;"
    
    cursor.execute(sql)
    
    df = pd.DataFrame(cursor.fetchall())
    df.columns = ['id', 'open_date', 'open']
    df.drop(columns=['id', 'open_date'], inplace = True)
>>>>>>> parent of 8db6c19 (added validation and precictqueries)


<<<<<<< HEAD
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.2, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x + self.pe[: x.size(0), :]
        return self.dropout(x)
=======
    X = scaler.transform(df)
    X = X.astype(np.float32)
    X = X[::-1]

    for _ in range(100):
        client = httpclient.InferenceServerClient(url="inference-service:8000")

        inputs = httpclient.InferInput("input__0", X.shape, datatype="FP32")
        inputs.set_data_from_numpy(X)

        outputs = httpclient.InferRequestedOutput(
        "output__0"
        )

        # Querying the server
        results = client.infer(model_name="btcmodel", inputs=[inputs], outputs=[outputs])
        inference_output = results.as_numpy("output__0")

        X = np.append(X, inference_output)
        X = X[1:]
        X = np.reshape(X, (100, 1))


    
    return scaler.inverse_transform(pd.DataFrame(X))
>>>>>>> parent of 8db6c19 (added validation and precictqueries)


class BTCModel(nn.Module):
    def __init__(self, input_dim=1, d_model=256, nhead=4, num_layers=1, dropout=0.2):
        super(BTCModel, self).__init__()

        self.encoder = nn.Linear(input_dim, d_model)
        self.pos_encoder = PositionalEncoding(d_model, dropout)
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        self.decoder = nn.Linear(d_model, 1)

    def forward(self, x):
        x = self.encoder(x)
        x = self.pos_encoder(x)
        x = self.transformer_encoder(x)
        x = self.decoder(x[:, -1, :])
        return x


def predict(model, X):
    preds = model(X).flatten().tolist()
    return preds
