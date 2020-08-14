import os

import requests

TECHNICAL_ANALYSIS_SMA_KEY = "Technical Analysis: SMA"
SMA_KEY = "SMA"


def _prepare_api_url(symbol, time_period):
    function_param = "function=SMA"
    symbol_param = "symbol={}".format(symbol)
    interval_param = "interval=daily"
    time_period_param = "time_period={}".format(time_period)
    series_type_param = "series_type=close"
    alpha_vantage_api_key = os.environ["alphaVantageApiKey"]
    api_key_param = "apikey={}".format(alpha_vantage_api_key)
    api_url = "https://www.alphavantage.co/query?{}&{}&{}&{}&{}&{}".format(
        function_param,
        symbol_param,
        interval_param,
        time_period_param,
        series_type_param,
        api_key_param,
    )
    return api_url


def simple_moving_average(symbol, time_period=50):
    api_url = _prepare_api_url(symbol, time_period)
    results = []
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        api_result = response.json()
        if TECHNICAL_ANALYSIS_SMA_KEY in api_result:
            sma_dict = api_result[TECHNICAL_ANALYSIS_SMA_KEY]
            for date_key in sorted(sma_dict):
                sma_value = sma_dict[date_key][SMA_KEY]
                observation = {"date": date_key, "value": float(sma_value)}
                results.append(observation)

    return results
