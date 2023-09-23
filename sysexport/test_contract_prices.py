# tests if pysystemtrade returns the same response and my f_strats scripts

# from sysbrokers.IB.client.ib_price_client import _get_generic_data_for_contract
import pytest



# from sysobjects.contracts import futuresContract
# from sysinit.futures.seed_price_data_from_IB import seed_price_data_from_IB







# seed_price_data_from_IB("CRUDE_W")
from sysinit.futures.rollcalendars_from_arcticprices_to_csv import build_and_write_roll_calendar
from sysexport.rollcalendar_daily_only import build_and_write_roll_calendar_daily
from sysdata.csv.csv_roll_parameters import csvRollParametersData

from sysdata.arctic.arctic_futures_per_contract_prices import (
    arcticFuturesContractPriceData,
)
from syscore.dateutils import Frequency



from sysexport.load_data import load_data_for_pysys_instrument



class TestRollCalendar():
    def test_daily_roll_calendar_v_orig(self):
        """
        This is code from sysinit.futures.rollcalendars_from_arcticprices_to_csv
        This is tested against the original source code to check if hourly data affects the roll calendar
        """
        daily_roll_calendar = build_and_write_roll_calendar_daily(
                    "CRUDE_W",
                    output_datapath="/Users/f1/Desktop/roll-calendars",
                    roll_parameters_data=csvRollParametersData(),
                    check_before_writing=False,
        )
        source_code_merged_prices_calendar = build_and_write_roll_calendar(
                    "CRUDE_W",
                    output_datapath="/Users/f1/Desktop/roll-calendars",
                    roll_parameters_data=csvRollParametersData(),
                    check_before_writing=False,
        )
        print(daily_roll_calendar)
        print(source_code_merged_prices_calendar)


    def test_my_strats_data_equals_pysys(self):
        """
            loads both datasets
        """

        my_prices = load_data_for_pysys_instrument("CRUDE_W")
        # print(my_prices)


        # pysys data
        prices = arcticFuturesContractPriceData()
        dict_prices = prices.get_prices_at_frequency_for_instrument(
            "CRUDE_W",
            Frequency.Day
        )
        dict_prices_final = dict_prices.final_prices()
        # print(dict_of_futures_contract_prices)

        print("MY CONTRACT DATES")
        print(sorted([price[0] for price in my_prices]))
        print("PYSYS CONTRACT DATES")
        print(sorted(dict_prices_final._get_and_set_sorted_contract_date_str()))

    def test_create_roll_calendar_my_data():
        """test creating the pysystemtrade roll calendar with my dataa"""
        my_prices = load_data_for_pysys_instrument("CRUDE_W")
        build_and_write_roll_calendar(
                    "CRUDE_W",
                    output_datapath="/Users/f1/Desktop/roll-calendars",
                    input_prices=my_prices,
                    roll_parameters_data=csvRollParametersData(),
                    check_before_writing=False,
        )





# TO CHECK:
# is lastContractTradeOrMonth from IB the contractDateStr used in pysystemtrade?


# for the instrument_code passed in to build_and_write_roll_calendar
# the roll parameter csv:
# data/futures/csvconfig/rollconfig.csv

# build_and_write_roll_calendar(
#             "CRUDE_W",
#             output_datapath=output_dir,
#             input_prices=sample_prices,
#             roll_parameters_data=csvRollParametersData(),
#             check_before_writing=False,
# )




# build_and_write_roll_calendar calls arcticFuturesContractPriceData().get_merged_prices_for_instrument()
# from sysdata.futures.futures_per_contract_prices import arcticFuturesContractPriceData


