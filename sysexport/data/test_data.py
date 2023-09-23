from sysinit.futures.seed_price_data_from_IB import seed_price_data_from_IB
from sysdata.arctic.arctic_futures_per_contract_prices import arcticFuturesContractPriceData
from syscore.dateutils import Frequency


from sysexport.simplified.seed_price_data_from_IB.seed_price_data_from_IB import seed_price_data_from_IB

class TestData:

    def test_data(self):
        """
            the dataframes read from the files downloaded using the pytower IB data downloader client
            should match the dataframes written to mongodb 
            this tests from downloading per contract prices, to get_merged_prices_per_instrument()
        """
        # get_pric
        instrument_code = "CRUDE_W"

        # convert_pysys_instrument_code(instrument_code)


        # pysys:
        # for every contract
        # seed_price_data_for_contract_at_frequency(
        # write_merged_prices_for_contract(
        # then read from arctic - this will be the data used to stitch the contracts
        # seed_price_data_from_IB(instrument_code)


        # 

        arctic_per_contract_prices = arcticFuturesContractPriceData()
        prices = arctic_per_contract_prices.get_contracts_with_price_data_for_frequency(Frequency.Day)
        print(prices)





    def test_download(self):
        """
            execution path of seed_price_data_from_IB
        """
        pass




       
    def get_pytower_data():
        pass
