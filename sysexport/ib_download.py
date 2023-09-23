



# this class is DataBlob().broker_futures_contract_data
# from sysbrokers.IB.ib_futures_contracts_data import ibFuturesContractData
from sysbrokers.IB.ib_instruments_data import ibFuturesInstrumentData
from sysbrokers.IB.client.ib_contracts_client import ibContractsClient
import pandas as pd
from dataclasses import dataclass
from ib_insync import Future

class listOfContractDateStr(list):
    def sorted_date_str(self):
        return listOfContractDateStr(sorted(self))

    def final_date_str(self):
        return self.sorted_date_str()[-1]




def _resolve_multiplier(multiplier_passed):
    multiplier = float(multiplier_passed)
    multiplier_is_round_number = round(multiplier) == multiplier
    if multiplier_is_round_number:
        multiplier = str(int(multiplier_passed))
    else:
        multiplier = str(multiplier_passed)

    return multiplier


NOT_REQUIRED_FOR_IB = ""

def return_another_value_if_nan(x, return_value=None):
    """
    If x is np.nan return return_value
    else return x

    :param x: np.nan or other
    :return: x or return_value

    >>> return_another_value_if_nan(np.nan)

    >>> return_another_value_if_nan(np.nan, -1)
    -1

    >>> return_another_value_if_nan("thing")
    'thing'

    >>> return_another_value_if_nan(42)
    42

    """

    try:
        if np.isnan(x):
            return return_value
        else:
            pass
            # Not a nan will return x
    except BaseException:
        # Not something that can be compared to a nan
        pass

    # Either wrong type, or not a nan
    return x





@dataclass
class ibInstrumentConfigData:
    symbol: str
    exchange: str
    currency: str = NOT_REQUIRED_FOR_IB
    ibMultiplier: float = NOT_REQUIRED_FOR_IB
    priceMagnifier: float = 1.0
    ignoreWeekly: bool = False

    @property
    def effective_multiplier(self):
        return self.ibMultiplier / self.priceMagnifier

    def __repr__(self):
        return (
            "symbol='%s', exchange='%s', currency='%s', ibMultiplier='%s', priceMagnifier='%.2f', "
            "ignoreWeekly='%s', effective_multiplier='%.2f'"
            % (
                self.symbol,
                self.exchange,
                self.currency,
                self.ibMultiplier,
                self.priceMagnifier,
                self.ignoreWeekly,
                self.effective_multiplier,
            )
        )

    def as_dict(self):
        return dict(
            symbol=self.symbol,
            exchange=self.exchange,
            currency=self.currency,
            ibMultiplier=self.ibMultiplier,
            priceMagnifier=self.priceMagnifier,
            ignoreWeekly=self.ignoreWeekly,
            effective_multiplier=self.effective_multiplier,
        )







class IbDownload():
    def __init__(self):
        pass

    def contracts_for_instruments(self, instrument_code: str, allow_expired: bool=False):
        """
            
        """

        ibcontract_pattern = Future(ib_data.symbol, exchange=ib_data.exchange)
        print(ibcontract_pattern)

        if ib_data.ibMultiplier is NOT_REQUIRED_FOR_IB:
            pass
        else:

            ibcontract_pattern.multiplier = _resolve_multiplier(ib_data.ibMultiplier)

        if ib_data.currency is NOT_REQUIRED_FOR_IB:
            pass
        else:
            ibcontract_pattern.currency = ib_data.currency

        # END ib_futures_instrument()

        ibcontract_pattern.includeExpired = allow_expired
        contract_details = self.ib.reqContractDetails(ibcontract_pattern)

        assert len(contract_details) == 0, "missing contract"

        if allow_multiple_contracts:
            return contract_details

        elif len(contract_details) > 1:
            self.log.critical(
                "Multiple contracts and only expected one - returning the first"
            )

        ibcontract_list = [
            contract_details.contract for contract_details in contract_details
        ]

        # if no contracts found will be empty
        # Extract expiry date strings from these
        list_of_contracts = [ibcontract.lastTradeDateOrContractMonth for ibcontract in ibcontract_list]
        return listOfContractDateStr(list_of_contracts)



    def download(self, instrument_code: str):
        """
            download fn: sysbrokers/IB/client/ib_price_client.py
        """
        
        with open(os.path.join("/Users/f1ib_instruments.json"), "r") as f:
            ib_instruments = json.load(f)

        list_of_contracts = self.contracts_for_instruments(instrument_code)

        ## This returns yyyymmdd strings, where we have the actual expiry date
        for contract_date in list_of_contracts:
            ## We do this slightly tortorous thing because there are energy contracts
            ## which don't expire in the month they are labelled with
            ## So for example, CRUDE_W 202106 actually expires on 20210528
            date_str = contract_date[:6]
            contract_object = futuresContract(instrument_code, date_str)
            # seed_price_data_for_contract(data=data, contract_object=contract_object)

            # ==== seed_price_data_for_contract
            # log = contract_object.specific_log(data.log)
            # list_of_frequencies = [DAILY_PRICE_FREQ] # HOURLY_FREQ
            # for frequency in list_of_frequencies:
            prices_df = _get_generic_data_for_contract(contract_object, bar_freq=DAILY_PRICE_FREQ, whatToShow="TRADES")
            print(prices_df)
                
                
            # write_merged_prices_for_contract(
            #     data, contract_object=contract_object, list_of_frequencies=list_of_frequencies
            # )
            #



ib_download = IbDownload()
ib_download.contracts_for_instruments("BTC", True)


