
# execution flow of stitch_multiple_prices(())
"""
stitch_multiple_prices() -> _panama_stitch()


_panama_stitch() -> only called from stitch_multiple_prices()
"""

# from sysinit.futures.adjustedprices_from_mongo_multiple_to_mongo import process_adjusted_prices_single_instrument

# process_adjusted_prices_single_instrument("CRUDE_W")
#
#
# from sysobjects.adjusted_prices import futuresAdjustedPrices
#
# # assuming we have some multiple prices
# print("GET MULTIPLE PRICES")
#
#
# # checks if there is a key in the mongodb for the data
# # does not get the data if the key does not exist AND does not error
from sysdata.arctic.arctic_multiple_prices import arcticFuturesMultiplePricesData
# arctic_multiple_prices = arcticFuturesMultiplePricesData()
#
# adjusted_prices = futuresAdjustedPrices.stitch_multiple_prices(multiple_prices)
#
#
# multiple_prices = arctic_multiple_prices._get_multiple_prices_without_checking("CRUDE_W")

# from sysdata.arctic.arctic_futures_per_contract_prices import arcticFuturesContractPriceData
# arctic_futures_contracts = arcticFuturesContractPriceData()
# data = arctic_futures_contracts.get_merged_prices_for_contract_object_no_checking()
# print(data)


from sysinit.futures.multipleprices_from_arcticprices_and_csv_calendars_to_arctic import process_multiple_prices_single_instrument as process_multiple_prices_single_instrument_pysys






class TestStitching:
    """
        tests the data process pipeline pytower vs pysys AFTER the per contract data has been downloaded:
            per contracts prices -> multiple price series using roll calendars -> stitching
        
    """
    def test_multiple_prices_against_simplified():
        """
            test if multiple prices returns
        """
        process_multiple_prices_single_instrument_pysys(instrument_code="CRUDE_W")
        # abgve only writes to mongodb, multiple prices have to be read again
        arctic_multiple_prices = arcticFuturesMultiplePricesData()
        multiple_prices = arctic_multiple_prices.get_multiple_prices("CRUDE_W")
