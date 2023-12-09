makedb test2
usedb test2
makedb test2
makedb test3
showdb
dropdb test3
usedb test2
make try COLUMNS a=int, b=str
make COPY try tryt
edit try insert a=1 b="abc"
MAKE BTC.csv COLUMNS candle_begin_time=datetime64, open=float, high=float, low=float, close=float, volume=float, quote_volume=float, trade_num=int, taker_buy_base_asset_volume=float, taker_buy_quote_asset_volume=float, Spread=float, symbol=str, avg_price_1m=float, avg_price_5m=float
EDIT BTC.csv INSERT FILE BTC.csv
MAKE BTCALL.csv COLUMNS candle_begin_time=datetime64, open=float, high=float, low=float, close=float, volume=float, quote_volume=float, trade_num=int, taker_buy_base_asset_volume=float, taker_buy_quote_asset_volume=float, Spread=float, symbol=str, avg_price_1m=float, avg_price_5m=float
EDIT BTCALL.csv INSERT FILE BTCALL.csv

FROM BTC.csv FIND candle_begin_time, volume, symbol CHARACTER volume < 1000
FROM BTC.csv FIND candle_begin_time, volume, symbol CHARACTER volume < 1000 LINE volume
FROM BTC.csv FIND candle_begin_time, volume, symbol CHARACTER volume < 1000 BUNCH symbol max(volume)
FROM BTC.csv FIND candle_begin_time, volume, symbol CHARACTER volume < 1000 CONNECT BTCALL.csv ON symbol


fetch BTC.csv *
edit try update id=0 b="abcdefg"
fetch try *
edit try delete id=0
fetch try *
drop try
show
usedb test2
fetch BTC.csv columns:high&close
fetch BTC.csv columns:high&close&volume SORT volume ASC
usedb test2
fetch BTC.csv * HAS volume < 1000
fetch BTC.csv columns high close volume SORT volume ASC
fetch BTC.csv columns volume symbol sum volume bunch symbol
fetch BTC.csv * HAS symbol = BTC-USDT
fetch BTC.csv columns volume symbol min volume bunch symbol
fetch BTC.csv columns volume symbol min volume bunch symbol SORT volume ASC
fetch BTC.csv columns volume symbol max volume bunch symbol SORT volume ASC



fetch BTC.csv columns:high&close&volume&symbol sum volume bunch symbol


usedb test_db
fetch test columns:col1&col2&col3 sum col1 bunch col3 sort col3 ASC


usedb REL test_db
fetch test columns col1 col2 col3 sum col1 bunch col3 sort col3 ASC
fetch real_estate *


usedb REL test_db
makedb REL test2
usedb REL test2
makedb REL test3
showdb REL
dropdb REL test3
usedb REL test2
make try COLUMNS a=int, b=str
make COPY try tryt
edit try insert a=a b="abc"
fetch BTC.csv *
edit try update id=0 b="abcdefg"
fetch try *
edit try delete id=0
fetch try *
drop REL try
show REL