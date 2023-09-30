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
from syscore.dateutils import Frequency
import pandas as pd
from syscore.fileutils import resolve_path_and_filename_for_package
import os

# from sysexport.simplified.seed_price_data_from_IB import seed_price_data_from_IB
from sysinit.futures.seed_price_data_from_IB import seed_price_data_from_IB
from sysinit.futures.rollcalendars_from_arcticprices_to_csv import build_and_write_roll_calendar

now = datetime.datetime.now()




class TestRollCalendar():

    def get_roll_calendar_instrument_codes(self):
        filepath = resolve_path_and_filename_for_package(
            "data.futures.csvconfig", f"rollconfig.csv" # data.futures.roll_calendars_csv
        )
        df = pd.read_csv(filepath, skiprows=0, skipfooter=0)
        return list(df.Instrument)

    def download_all_data_for_roll_calendars(self):
        """
            STEP 1
        """
        # get all instrument codes that have pre defined roll calendars
        for instrument_code in self.get_roll_calendar_instrument_codes():
            seed_price_data_from_IB(instrument_code)

    def extract_test_data_for_pytower_from_mongodb(self):
        """
            STEP 2: extract data from mongodb to a location that pytower reads from as input to roll calendar (tests)
            get_merged_prices_for_instrument() is used as the data source in build_and_write_roll_calendar() 
        """

        def write_all_prices(prices, dirname, instrument_code):
            output_root = f'/Users/f1/Desktop/ib_data_download/test_data/per_contract_prices/{now.strftime("%Y-%m-%d-%H-%M-%S")}'
            for k, df in prices.items():
                output_path = Path(f'{output_root}/{dirname}/{instrument_code}/{k}.parquet')
                output_path.parent.mkdir(parents=True, exist_ok=True)
                print(f"Writing File - {output_path}")
                print(df)
                df.to_parquet(output_path)

        prices = arcticFuturesContractPriceData()
        for instrument_code in self.get_roll_calendar_instrument_codes():
            # class returned -> dictFuturesContractPrices
            merged_prices = prices.get_merged_prices_for_instrument(instrument_code)
            daily_prices = prices.get_prices_at_frequency_for_instrument(instrument_code, Frequency.Day)
            hourly_prices = prices.get_prices_at_frequency_for_instrument(instrument_code, Frequency.Hour)
            write_all_prices(merged_prices, "merged", instrument_code)
            write_all_prices(daily_prices, "daily", instrument_code)
            write_all_prices(hourly_prices, "hourly", instrument_code)


    def test_convert_to_final_prices(self):
        """what happens when dict_of_all_futures_contract_prices.final_prices() is called?"""
        prices = arcticFuturesContractPriceData()
        dict_of_all_futures_contract_prices = prices.get_merged_prices_for_instrument("CRUDE_W")
        dict_of_futures_contract_prices = dict_of_all_futures_contract_prices.final_prices()
        print(dict_of_futures_contract_prices.keys())
        print(dict_of_futures_contract_prices.values())


    def generate_roll_calendars(self):
        """
            generates roll calendars for all instruments we have test data for
            TODO: Before using again, this function needs to READ the 
            because the database contents might have changed, always read the prices from the test files
        """
        prices_dir = "/Users/f1/dev/app/trading/pytower/pytower/tests/data/pysys/per_contract_prices/merged"
        instrument_codes = [item for item in os.listdir(prices_dir) if os.path.isdir(os.path.join(prices_dir, item))]
        for instrument_code in instrument_codes:
            build_and_write_roll_calendar(
                instrument_code=instrument_code,
                output_datapath="/Users/f1/Desktop/ib_data_download/test_data/roll_calendars",
                write=True,
                check_before_writing=False, # disable prompt

            )
        

test_roll = TestRollCalendar()
# test_roll.test_roll()
# test_roll.test_convert_to_final_prices()
# test_roll.extract_test_data_for_pytower_from_mongodb()
test_roll.download_all_data_for_roll_calendars()
# test_roll.generate_roll_calendars()

















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


