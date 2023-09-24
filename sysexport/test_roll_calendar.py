# from sysexport.simplified.roll.multipleprices_from_arcticprices_and_csv_calendars_to_arctic import process_multiple_prices_single_instrument
# from sysexport.simplified.roll.rollcalendars_from_arcticprices_to_csv import build_and_write_roll_calendar as build_and_write_roll_calendar_simplified

# difference between:
# sysinit/futures/multipleprices_from_arcticprices_and_csv_calendars_to_arctic.py
# sysinit/futures/rollcalendars_from_arcticprices_to_csv.py


# used by roll param functions
# dict_of_futures_contract is { ts1: price1, ts2: price2}

import datetime
from pathlib import Path
from sysdata.arctic.arctic_futures_per_contract_prices import (
    arcticFuturesContractPriceData,
)

now = datetime.datetime.now()




class TestRollCalendar():

    def generate_test_data_for_pytower(self):
        """
            extracts data from arctic db 
            get_merged_prices_for_instrument() is used to get data to create the roll calendars
        """
        prices = arcticFuturesContractPriceData()
        instrument_codes = ["CRUDE_W"]
        for instrument_code in instrument_codes:
            dict_of_all_futures_contract_prices = prices.get_merged_prices_for_instrument(instrument_code)
            dict_of_futures_contract_prices = dict_of_all_futures_contract_prices.final_prices()
            for k, df in dict_of_futures_contract_prices.items():
                for a,b in df.items():
                    print(a,b)
                # output_path = Path(f'/Users/f1/Desktop/ib_data_download/test_data/get_merged_prices_for_instrument/{now.strftime("%Y-%m-%d-%H-%M-%S")}/{instrument_code}/{k}.parquet')
                # output_path.parent.mkdir(parents=True, exist_ok=True)
                # print(f"Writing File - {output_path}")
                # df.to_parquet(output_path)

    def test_roll(self):
        # process_multiple_prices_single_instrument("CRUDE_W")
        build_and_write_roll_calendar_simplified("CRUDE_W")


    def test_convert_to_final_prices(self):
        """what happens when dict_of_all_futures_contract_prices.final_prices() is called?"""
        prices = arcticFuturesContractPriceData()
        dict_of_all_futures_contract_prices = prices.get_merged_prices_for_instrument("CRUDE_W")
        dict_of_futures_contract_prices = dict_of_all_futures_contract_prices.final_prices()
        print(dict_of_futures_contract_prices.keys())
        print(dict_of_futures_contract_prices.values())
















test_roll = TestRollCalendar()
# test_roll.test_roll()
test_roll.test_convert_to_final_prices()
# test_roll.generate_test_data_for_pytower()

















    # def test_daily_roll_calendar_v_orig(self):
    #     """
    #     This is code from sysinit.futures.rollcalendars_from_arcticprices_to_csv
    #     This is tested against the original source code to check if hourly data affects the roll calendar
    #     """
    #     daily_roll_calendar = build_and_write_roll_calendar_daily(
    #                 "CRUDE_W",
    #                 output_datapath="/Users/f1/Desktop/roll-calendars",
    #                 roll_parameters_data=csvRollParametersData(),
    #                 check_before_writing=False,
    #     )
    #     source_code_merged_prices_calendar = build_and_write_roll_calendar(
    #                 "CRUDE_W",
    #                 output_datapath="/Users/f1/Desktop/roll-calendars",
    #                 roll_parameters_data=csvRollParametersData(),
    #                 check_before_writing=False,
    #     )
    #     print(daily_roll_calendar)
    #     print(source_code_merged_prices_calendar)
    #
    #
    # def test_my_strats_data_equals_pysys(self):
    #     """
    #         loads both datasets
    #     """
    #
    #     my_prices = load_data_for_pysys_instrument("CRUDE_W")
    #     # print(my_prices)
    #
    #
    #     # pysys data
    #     prices = arcticFuturesContractPriceData()
    #     dict_prices = prices.get_prices_at_frequency_for_instrument(
    #         "CRUDE_W",
    #         Frequency.Day
    #     )
    #     dict_prices_final = dict_prices.final_prices()
    #     # print(dict_of_futures_contract_prices)
    #
    #     print("MY CONTRACT DATES")
    #     print(sorted([price[0] for price in my_prices]))
    #     print("PYSYS CONTRACT DATES")
    #     print(sorted(dict_prices_final._get_and_set_sorted_contract_date_str()))
    #
    # def test_create_roll_calendar_my_data():
    #     """test creating the pysystemtrade roll calendar with my dataa"""
    #     my_prices = load_data_for_pysys_instrument("CRUDE_W")
    #     build_and_write_roll_calendar(
    #                 "CRUDE_W",
    #                 output_datapath="/Users/f1/Desktop/roll-calendars",
    #                 input_prices=my_prices,
    #                 roll_parameters_data=csvRollParametersData(),
    #                 check_before_writing=False,
    #     )






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


