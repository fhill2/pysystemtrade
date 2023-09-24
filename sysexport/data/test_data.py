from sysdata.arctic.arctic_futures_per_contract_prices import arcticFuturesContractPriceData
from syscore.dateutils import Frequency
from sysobjects.contracts import futuresContract


from sysinit.futures.seed_price_data_from_IB import seed_price_data_from_IB
from sysexport.simplified.seed_price_data_from_IB.seed_price_data_from_IB import seed_price_data_from_IB as seed_price_data_from_IB_simplified



from sysdata.data_blob import dataBlob
from sysproduction.data.prices import diagPrices, updatePrices

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
        # then read from arctic - this will be the data used to stitch the contracts
        # seed_price_data_from_IB(instrument_code)


        # 




    def read_frequency_from_mongodb(self, instrument_code):
        arctic_per_contract_prices = arcticFuturesContractPriceData()
        contracts = arctic_per_contract_prices.get_contracts_with_price_data_for_frequency(Frequency.Day)
        instrument_prices = []
        for contract in contracts:
            if contract.instrument_code == instrument_code:
                instrument_prices.append(arctic_per_contract_prices._get_prices_at_frequency_for_contract_object_no_checking(contract, frequency=Frequency.Day))
        return instrument_prices

    def test_seed_against_simplified(self):
        """
            execution path of seed_price_data_from_IB
        """
        instrument_code = "CRUDE_W"

        # TODO: test all instrument codes and see if they return the same data

        # PYSYSTEMTRADE
        seed_price_data_from_IB(instrument_code)
        prices = self.read_frequency_from_mongodb(instrument_code)
        # pysys_prices = read_frequency_from_mongodb(instrument_code)
        print("================================================= SIMPLIFIED ===========================================")
        # SIMPLIFIED
        seed_price_data_from_IB_simplified(instrument_code)
        # contract_object = futuresContract("CRUDE_W")
        simplified_prices = self.read_frequency_from_mongodb(instrument_code)
        assert prices == simplified_prices, "Prices do not match"

    def test_seed_simplified_pytower():
        pass


    def test_merge(self):
        """
            tests merge 
        """
        data = dataBlob()
        contract = futuresContract("CRUDE_W", "20320100")
        diag_prices = diagPrices(data)
        list_of_frequencies = [Frequency.Hour, Frequency.Day]
        list_of_data = [
                    diag_prices.get_prices_at_frequency_for_contract_object( contract, frequency=frequency)
                    for frequency in list_of_frequencies
                ]
        print(list_of_data)
        # merged_prices = merge_data_with_different_freq(list_of_data)
        


        





       
    def get_pytower_data():
        pass
