import json
import glob
import os
import pandas as pd
HOME = os.path.expanduser("~")
DESKTOP = os.path.join(HOME, "Desktop")
DATA_DIR = os.path.join(DESKTOP, "ib_data_download")
IB_DATA_DIR = os.path.join(DATA_DIR, "ib", "data")
PYTOWER = os.path.join(HOME, "dev", "app", "trading", "f_strats")



cfreq = "daily"
IB_DATA_FREQ_DIR = os.path.join(IB_DATA_DIR, cfreq)



# main pysys IB download entry point
# from sysinit.futures.seed_price_data_from_IB import seed_price_data_from_IB
#
# def get_pysys_data(instrument_code):
#     """
#         download new data for a pysys instrument into the mongodb
#         extract the dataframes from the mongodb for use in future tests
#     """
#     seed_price_data_from_IB(instrument_code)


def load_pytower_data(exchange, symbol):
    """ 
    loads data downloaded with pytower IB Data downloader in the pysystemtrade structure
    """

    path_glob = f"*-{exchange}-{symbol}-*.parquet"
    files_on_disk = glob.glob(os.path.join(IB_DATA_FREQ_DIR,path_glob))
    dict_of_prices = [
            (
                file.split("-")[3],
                pd.read_parquet(file)
            )
            for file in files_on_disk
    ]
    return dict_of_prices



def convert_pysys_instrument_code(instrument_code):
    with open(os.path.join(PYTOWER, "strats", "tests", "pysys_inst_map.json"), "r") as f:
        pysys_inst_map = json.load(f)
    return pysys_inst_map[instrument_code]


def load_data_for_pysys_instrument(instrument_code):
    cinst = convert_pysys_instrument_code(instrument_code)
    return load_pytower_data(cinst[0], cinst[1])



# load_data()



# load_data_for_pysys_instrument("CRUDE_W")


def extract_per_contract_prices():
    """
        used to test stitching
        extracts the per contract prices for the instrument_code from mongodb
    """


