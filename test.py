from pysystemtrade.sysinit.futures.seed_price_data_from_IB import seed_price_data_from_IB
from pathlib import Path
from pysystemtrade.sysinit.futures.rollcalendars_from_arcticprices_to_csv import build_and_write_roll_calendar
# seed_price_data_from_IB("ETHANOL")

build_and_write_roll_calendar(
    instrument_code="ETHANOL",
    output_datapath=Path("~/ib_data_download").expanduser(),
    )