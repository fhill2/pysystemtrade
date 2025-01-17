import logging
logargs = dict(
    format="%(asctime)s: %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
    # this will change loglevel for this script, and ib_insync API
    level=logging.INFO,
)
logging.basicConfig(**logargs)
logger = logging.getLogger(__name__)


import pandas as pd


# To keep in mind
# contractDates, in sysobjects/contract_dates_and_expiries - normal/VIX/Gas
# ignoreWeekly? loaded from data

# do we need to support multi leg contracts? and what are they?
# also, why does rob update the expiries of the contracts in the data ?

# do we need to:
# replace midnight with notional closing time
# everything in ib_price_client


# this is the execution flow of sysinit/futures/seed_price_data_from_IB.py
# files within this directory are part of the execution flow

from syscore.exceptions import missingData, missingContract
# from sysbrokers.IB.ib_futures_contract_price_data import (
    # futuresContract,
# )
from syscore.dateutils import DAILY_PRICE_FREQ, HOURLY_FREQ, Frequency
from sysdata.data_blob import dataBlob

from sysproduction.data.broker import dataBroker
from sysproduction.data.prices import updatePrices
from sysproduction.update_historical_prices import write_merged_prices_for_contract



# merged / added imports
from sysobjects.contract_dates_and_expiries import expiryDate, listOfContractDateStr

from sysobjects.futures_per_contract_prices import futuresContractPrices



from sysbrokers.IB.ib_connection import connectionIB
ibconnection = connectionIB(client_id=1,ib_ipaddress="127.0.0.1",ib_port=7496)

from sysbrokers.IB.client.ib_price_client import ibPriceClient
ib_price_client = ibPriceClient(ibconnection=ibconnection)

from sysbrokers.IB.client.ib_contracts_client import ibContractsClient
ib_contracts_client = ibContractsClient( ibconnection=ibconnection)

from sysbrokers.IB.ib_instruments_data import ibFuturesInstrumentData
from sysdata.data_blob import dataBlob
ib_futures_instrument_data = ibFuturesInstrumentData(ibconnection=ibconnection, data=dataBlob())


# imports to read csv
from sysbrokers.IB.ib_instruments import ibInstrumentConfigData, futuresInstrumentWithIBConfigData
from sysobjects.instruments import futuresInstrument

# imports to recreates futuresContract
from sysobjects.contract_dates_and_expiries import contractDate


from sysobjects.contracts import futuresContract
# all code used in execution flow from sysobjects/contracts.py
# class futuresContract(object):
#     def __init__(
#         self,
#         instrument_code: str,
#         contract_date_object: str,
#     ):
#         self.instrument_code = instrument_code
#         self.instrument_object = futuresInstrument(instrument_code)
#         self.contract_date_object = contractDate(contract_date_object)
#
#     def is_spread_contract(self):
#         return self.contract_date.is_spread_contract

# sysbrokers/IB/config/ib_instrument_config.py -> get_instrument_object_from_valid_config()

# imports for write_merged_prices_for_contract()
from sysproduction.data.prices import diagPrices, updatePrices
from syscore.pandas.frequency import merge_data_with_different_freq
from sysdata.futures.futures_per_contract_prices import futuresContractPriceData


from syscore.genutils import return_another_value_if_nan
from sysbrokers.IB.ib_instruments import NOT_REQUIRED_FOR_IB
def get_instrument_object_from_config(instrument_code: str
) -> futuresInstrumentWithIBConfigData:
    # config = pd.read_csv( "sysbrokers.IB.config.ib_config_futures.csv")
    config = pd.read_csv("/Users/f1/dev/app/trading/pysystemtrade/sysbrokers/IB/config/ib_config_futures.csv")
    config_row = config[config.Instrument == instrument_code]
    symbol = config_row.IBSymbol.values[0]
    exchange = config_row.IBExchange.values[0]
    currency = return_another_value_if_nan(
        config_row.IBCurrency.values[0], NOT_REQUIRED_FOR_IB
    )
    ib_multiplier = return_another_value_if_nan(
        config_row.IBMultiplier.values[0], NOT_REQUIRED_FOR_IB
    )
    price_magnifier = return_another_value_if_nan(
        config_row.priceMagnifier.values[0], 1.0
    )
    ignore_weekly = config_row.IgnoreWeekly.values[0]

    # We use the flexibility of futuresInstrument to add additional arguments
    instrument = futuresInstrument(instrument_code)
    ib_data = ibInstrumentConfigData(
        symbol,
        exchange,
        currency=currency,
        ibMultiplier=ib_multiplier,
        priceMagnifier=price_magnifier,
        ignoreWeekly=ignore_weekly,
    )

    futures_instrument_with_ib_data = futuresInstrumentWithIBConfigData(
        instrument, ib_data
    )

    return futures_instrument_with_ib_data


# sysbrokers/IB/ib_futures_contracts_data
def _get_actual_expiry_date_given_single_contract_with_ib_metadata(futures_contract_with_ib_data: futuresContract, allow_expired=False
) -> expiryDate:
    # log = futures_contract_with_ib_data.specific_log(self.log)
    if futures_contract_with_ib_data.is_spread_contract():
        logger.warning("Can't find expiry for multiple leg contract here")
        raise missingContract
    # print(futures_contract_with_ib_data.ib_data)
    expiry_date = ib_contracts_client.broker_get_single_contract_expiry_date(
        futures_contract_with_ib_data, allow_expired=allow_expired
    )
    print("expiry date: ", expiry_date)

    expiry_date = expiryDate.from_str(expiry_date)

    return expiry_date

# from ib_futures_contract_price_data
# _get_prices_at_frequency_for_contract_object_no_checking_with_expiry_flag(
def get_prices_at_frequency(
    contract: futuresContract,
    frequency: Frequency,
    config_instrument,
    allow_expired: bool = False,

    ):

    try:
        # this code might break functionality
        new_contract = contract.new_contract_with_replaced_instrument_object(config_instrument)
        # print("after: ", new_contract.instrument_code, new_contract.date_str)
                

        contract = new_contract.update_expiry_dates_one_at_a_time_with_method(
                  _get_actual_expiry_date_given_single_contract_with_ib_metadata,
                  allow_expired=allow_expired,
              )
    except missingContract:
        logger.warning("Can't get data for %s" % str(contract))
        raise missingData


    try:
        price_data = ib_price_client.broker_get_historical_futures_data_for_contract(
            new_contract,
            bar_freq=frequency,
            allow_expired=allow_expired,
        )
    except missingData:
        logger.warning(
            "Something went wrong getting IB price data for %s"
            % str(new_contract)
        )
        raise

    if len(price_data) == 0:
        logger.warning(
            "No IB price data found for %s"
            % str(new_contract)
        )
        return futuresContractPrices.create_empty()

    return futuresContractPrices(price_data)





def seed_price_data_from_IB(instrument_code):
    print("===================================================")
    data = dataBlob()

    config_instrument = get_instrument_object_from_config(instrument_code)

    # reqContractDetails() - get all contracts for instrument
    list_of_contracts = ib_contracts_client.broker_get_futures_contract_list(
        config_instrument, allow_expired=True
    )
    list_of_contracts = listOfContractDateStr(list_of_contracts)

    ## This returns yyyymmdd strings, where we have the actual expiry date

    for contract_date in list_of_contracts:
        ## We do this slightly tortorous thing because there are energy contracts
        ## which don't expire in the month they are labelled with
        ## So for example, CRUDE_W 202106 actually expires on 20210528

        date_str = contract_date[:6]
        contract = futuresContract(instrument_code, date_str)
        # log = contract_object.specific_log(data.log)
        list_of_frequencies = [HOURLY_FREQ, DAILY_PRICE_FREQ]
        for frequency in list_of_frequencies:
            data_broker = dataBroker(data)
            update_prices = updatePrices(data)

            try:
                prices = get_prices_at_frequency(contract, frequency=frequency, config_instrument=config_instrument, allow_expired=True)
            except missingData:
                return None


            if len(prices) == 0:
                logger.warning("No price data for %s" % str(contract))
            else:
                update_prices.overwrite_prices_at_frequency_for_contract(
                    contract_object=contract, frequency=frequency, new_prices=prices
                    )



        # sysproduction/update_historical_prices -> write_merged_prices_for_contract()
        ## note list of frequencies must have daily as last or groupby won't work with volume

        assert list_of_frequencies[-1] == DAILY_PRICE_FREQ

        diag_prices = diagPrices(data)
        price_updater = updatePrices(data)
        contract_price_data = futuresContractPriceData()

        list_of_data = [
            diag_prices.get_prices_at_frequency_for_contract_object( contract, frequency=frequency)
            for frequency in list_of_frequencies
        ]
        print("frequency price data")

        merged_prices = merge_data_with_different_freq(list_of_data)

        price_updater.overwrite_merged_prices_for_contract(
            contract_object=contract_object, new_prices=merged_prices
        )


seed_price_data_from_IB("CRUDE_W")
