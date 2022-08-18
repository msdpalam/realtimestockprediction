import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import json
import numpy as np

import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

connection_str = 'connection_str_for_eventhub_stockdatahub'
eventhub_name_2by1 = 'stockdatahub'


def get_stock_data(stockSymbol):
    x=datetime.now()
    date_N_days_ago = datetime.now() - timedelta(days=7)
    msft = yf.Ticker(stockSymbol)
    data_df = yf.download(stockSymbol,
    start=date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d"), interval="1m", end=x.strftime("%Y"+"-"+"%m"+"-"+"%d"))
    for chunk in np.array_split(data_df, len(data_df.index)):      
        row = chunk.to_dict('record')
        #print(row.columns)
        print(row)
        asyncio.sleep(5)

    return data_df



async def run(json_data):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    await asyncio.sleep(5)
    producer = EventHubProducerClient.from_connection_string(conn_str=connection_str, eventhub_name=eventhub_name_2by1)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()
        event_data_batch.add(EventData(json_data))
            # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        print("Successfully sent chunk data")
        
def download_stock_from(symbol):
    x=datetime.now()
    date_N_days_ago = datetime.now() - timedelta(days=7)
    msft = yf.Ticker(symbol)
    data_df = yf.download(symbol,
    start=date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d"), interval="1m", end=x.strftime("%Y"+"-"+"%m"+"-"+"%d"))
    # print(data_df)
    return data_df

def save_data_to_csv(symbol):
    x=datetime.now()
    date_N_days_ago = datetime.now() - timedelta(days=7)
    msft = yf.Ticker(symbol)
    data_df = yf.download(symbol,
    start=date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d"), interval="1m", end=x.strftime("%Y"+"-"+"%m"+"-"+"%d"))
    csv_fle_name = 'stock_data.csv'
    data_df.to_csv(csv_fle_name)

def load_data_from_csv(csv_fle_name):
    stock_data_from_csv = pd.read_csv(csv_fle_name)
    return stock_data_from_csv
    
if __name__ == '__main__':
    save_data_to_csv('msft')
    stock_data_df =load_data_from_csv('stock_data.csv')
    #for row in data_df.iterrows():
    for chunk in np.array_split(stock_data_df, len(stock_data_df.index)):
        row = chunk.to_dict('record')
        json_data = json.dumps(row)
        # Add events to the batch.
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(run(json_data))
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Loop Now")
            loop.close
