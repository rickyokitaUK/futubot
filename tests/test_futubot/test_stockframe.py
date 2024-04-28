import pandas as pd
from futu import SecurityFirm, TrdMarket

from futubot.accounts import Accounts
from futubot.robot import Robot


def test_create_frame():
    accounts = Accounts(
        host='127.0.0.1',
        port=11111,
        filter_trdmarket=TrdMarket.HK,
        security_firm=SecurityFirm.FUTUSECURITIES,
        paper_trading=True,
    )
    futubot = Robot(accounts=accounts)

    historical_quotes = futubot.get_historical_quotes(
        start_date='2022-08-08 09:30:00',
        end_date='2022-08-08 12:00:00',
        code_list=['HK.00700'])

    stockframe = futubot.create_stockframe(data=historical_quotes)
    assert isinstance(stockframe.frame, pd.DataFrame)

    accounts.close_quote_context()
    accounts.close_trade_context()


def test_add_rows():
    accounts = Accounts(
        host='127.0.0.1',
        port=11111,
        filter_trdmarket=TrdMarket.HK,
        security_firm=SecurityFirm.FUTUSECURITIES,
        paper_trading=True,
    )
    futubot = Robot(accounts=accounts)

    historical_quotes = futubot.get_historical_quotes(
        start_date='2022-08-08 09:30:00',
        end_date='2022-08-08 10:30:00',
        code_list=['HK.00700'])

    stockframe = futubot.create_stockframe(data=historical_quotes)
    length_before = len(stockframe.frame)

    data = [{
        'time_key': '2022-08-08 10:31:00',
        'code': 'HK.00700',
        'open': 312.4,
        'close': 313.6,
        'high': 314.4,
        'low': 312.2,
        'volume': 450500
    }]

    stockframe.add_rows(data=data)
    length_after = len(stockframe.frame)

    assert (length_after - length_before) == 1

    accounts.close_quote_context()
    accounts.close_trade_context()
