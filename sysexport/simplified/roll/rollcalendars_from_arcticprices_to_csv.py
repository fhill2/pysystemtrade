from syscore.interactive.input import true_if_answer_is_yes
from syscore.constants import arg_not_supplied

from sysdata.arctic.arctic_futures_per_contract_prices import (
    arcticFuturesContractPriceData,
)


from syscore.exceptions import missingData

from sysobjects.rolls import rollParameters
from sysobjects.roll_calendars import rollCalendar
from sysdata.csv.csv_roll_calendars import csvRollCalendarData
from sysdata.csv.csv_roll_parameters import csvRollParametersData
from sysdata.futures.rolls_parameters import rollParametersData
from sysproduction.data.prices import get_valid_instrument_code_from_user
from sysobjects.dict_of_futures_per_contract_prices import (
    dictFuturesContractFinalPrices,
)

import pandas as pd


from sysexport.simplified.roll.roll_parameters_with_price_data import (
    find_earliest_held_contract_with_price_data,
    contractWithRollParametersAndPrices,
)

from sysexport.simplified.roll.build_roll_calendars import generate_approximate_calendar, adjust_to_price_series

"""
Generate a 'best guess' roll calendar based on some price data for individual contracts
https://github.com/robcarver17/pysystemtrade/blob/master/docs/data.md#generate-a-roll-calendar-from-actual-futures-prices
"""



def get_roll_params_data(instrument_code):
    filepath = resolve_path_and_filename_for_package("data.futures.roll_calendars_csv", f"{instrument_code}.csv")
    df = pd.read_csv(filepath, skiprows=0, skipfooter=0)
    ## timestamp as column -> timestamp as index
    df.index = pd.to_datetime(df["DATE_TIME"], format="%Y-%m-%d %H:%M:%S").values
    del df["DATE_TIME"]
    df.index.name = None
    return df



class rollParameters:
    """test to ensure none of the methods are used on the class, so I can remove"""
    def __init__(
        self,
        hold_rollcycle: str,
        priced_rollcycle: str,
        roll_offset_day: int = 0,
        carry_offset: int = -1,
        approx_expiry_offset: int = 0,
    ):


def get_roll_params(instrument_code):
    filepath = resolve_path_and_filename_for_package("data.futures.csvconfig", "rollconfig.csv")
    df = pd.read_csv(filepath)
    config_for_this_instrument = self.loc[instrument_code]
    roll_parameters_object = rollParameters(
        hold_rollcycle=config_for_this_instrument.HoldRollCycle,
        roll_offset_day=config_for_this_instrument.RollOffsetDays,
        carry_offset=config_for_this_instrument.CarryOffset,
        priced_rollcycle=config_for_this_instrument.PricedRollCycle,
        approx_expiry_offset=config_for_this_instrument.ExpiryOffset,
    )
    return roll_parameters_object





def build_and_write_roll_calendar(
    instrument_code,
    output_datapath=arg_not_supplied,
    write=True,
    check_before_writing=True,
    input_prices=arg_not_supplied,
    roll_parameters_data: rollParametersData = arg_not_supplied,
    roll_parameters: rollParameters = arg_not_supplied,
):

    if output_datapath is arg_not_supplied:
        print(
            "*** WARNING *** This will overwrite the provided roll calendar. Might be better to use a temporary directory!"
        )
    else:
        print("Writing to %s" % output_datapath)

    prices = arcticFuturesContractPriceData()
    # roll_parameters_data = csvRollParametersData()
    roll_parameters_data = read_roll_param_csv(instrument_code)
    roll_parameters = roll_parameters_data.get_roll_parameters(instrument_code)

    csv_roll_calendars = csvRollCalendarData(output_datapath)

    dict_of_all_futures_contract_prices = prices.get_merged_prices_for_instrument(
        instrument_code
    )


    dict_of_futures_contract_prices = dict_of_all_futures_contract_prices.final_prices()

    # might take a few seconds
    print("Prepping roll calendar... might take a few seconds")
    roll_calendar = rollCalendar.create_from_prices(
        dict_of_futures_contract_prices, roll_parameters
    )
    approx_calendar = generate_approximate_calendar(
        roll_parameters, dict_of_futures_contract_prices
    )

    adjusted_calendar = adjust_to_price_series(
        approx_calendar, dict_of_futures_contract_prices
    )

    # checks - this might fail
    roll_calendar.check_if_date_index_monotonic()

    # exit()
    roll_calendar.check_dates_are_valid_for_prices(dict_of_futures_contract_prices)

    # Write to csv
    # Will not work if an existing calendar exists
    exit()
    if write:
        if check_before_writing:
            check_happy_to_write = true_if_answer_is_yes(
                "Are you ok to write this csv to path %s/%s.csv? [might be worth writing and hacking manually]?"
                % (csv_roll_calendars.datapath, instrument_code)
            )
        else:
            check_happy_to_write = True

        if check_happy_to_write:
            print("Adding roll calendar")
            csv_roll_calendars.add_roll_calendar(
                instrument_code, roll_calendar, ignore_duplication=True
            )
        else:
            print("Not writing - not happy")

    return roll_calendar


def check_saved_roll_calendar(
    instrument_code, input_datapath=arg_not_supplied, input_prices=arg_not_supplied
):

    if input_datapath is None:
        print(
            "This will check the roll calendar in the default directory : are you are that's what you want to do?"
        )

    csv_roll_calendars = csvRollCalendarData(input_datapath)

    roll_calendar = csv_roll_calendars.get_roll_calendar(instrument_code)

    if input_prices is arg_not_supplied:
        prices = arcticFuturesContractPriceData()
    else:
        prices = input_prices

    dict_of_all_futures_contract_prices = prices.get_merged_prices_for_instrument(
        instrument_code
    )
    dict_of_futures_contract_prices = dict_of_all_futures_contract_prices.final_prices()


    # checks - this might fail
    roll_calendar.check_if_date_index_monotonic()

    # this should never fail
    roll_calendar.check_dates_are_valid_for_prices(dict_of_futures_contract_prices)

    return roll_calendar


if __name__ == "__main__":
    input("Will overwrite existing roll calendar are you sure?! CTL-C to abort")
    instrument_code = get_valid_instrument_code_from_user(source="single")
    ## MODIFY DATAPATH IF REQUIRED
    # build_and_write_roll_calendar(instrument_code, output_datapath=arg_not_supplied)
    build_and_write_roll_calendar(instrument_code, output_datapath="/home/rob/")