    def contracts_for_instruments(self, instrument_code: str, allow_expired: bool=False):
        """
            this function is a flattened pysystemtrade function with header:
        def get_list_of_contract_dates_for_instrument_code(
            self, instrument_code: str, allow_expired: bool = False
        ) -> listOfContractDateStr:
        sysbrokers/IB/ib_futures_contracts_data.py
        """


        config = pd.read_csv("/Users/f1/dev/app/trading/pysystemtrade/sysbrokers/IB/config/ib_config_futures.csv")

        # POST PROCESS VALUES FROM CONFIG
        config_row = config[config["Instrument"] == instrument_code]
        print(config_row)
        symbol = config_row["IBSymbol"].values[0]
        exchange = config_row.IBExchange.values[0]
        currency = return_another_value_if_nan(
            config_row.IBCurrency.values[0], NOT_REQUIRED_FOR_IB
        )
        ib_multiplier = return_another_value_if_nan(
            config_row.IBMultiplier.values[0], NOT_REQUIRED_FOR_IB
        )
        price_magnifier = return_another_value_if_nan(
            config_row.priceMagnifier.values[0], 1.0
        )
        ignore_weekly = config_row.IgnoreWeekly.values[0]

        # We use the flexibility of futuresInstrument to add additional arguments
        # instrument = futuresInstrument(instrument_code)
        ib_data = ibInstrumentConfigData(
            symbol,
            exchange,
            currency=currency,
            ibMultiplier=ib_multiplier,
            priceMagnifier=price_magnifier,
            ignoreWeekly=ignore_weekly,
        )

        ibcontract_pattern = Future(ib_data.symbol, exchange=ib_data.exchange)

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

    # def contracts_for_instruments(self, instrument_code: str, allow_expired: bool=False):
    #     """
    #         this function is flattened pysystemtrade function with header:
    #     def get_list_of_contract_dates_for_instrument_code(
    #         self, instrument_code: str, allow_expired: bool = False
    #     ) -> listOfContractDateStr:
    #     """
    #
    #     # ========== get_futures_instrument_object_with_IB_data =====
    #     # ib_futures_instrument_data = ibFuturesInstrumentData()
    #     # ib_futures_instrument_data.get_futures_instrument_object_with_IB_data(
    #         # instrument_code
    #     # )
    #     # config = sysbrokers.IB.config.ib_config_futures.csv
    #     # futures_instrument_with_ib_data = ""
    #     # config = pd.read_csv("/Users/f1/dev/app/trading/pysystemtrade/sysbrokers/IB/config/ib_config_futures.csv")
    #     # print(config)
    #     # list_of_instruments = get_instrument_list_from_ib_config(config=config)
    #     # assert instrument_code in list_of_instruments, "instrument code not found in list of instruments"
    #
    #     futures_instrument_with_ib_data = _get_instrument_object_from_valid_config(
    #         instrument_code=instrument_code, config=config
    #     )
    #     exit()
    #
    #
    #     # ======== END =================
    #
    #
    #     # ib_contracts_client = ibContractsClient()
    #     # list_of_contracts = ib_contracts_client.broker_get_futures_contract_list(
    #     # futures_instrument_with_ib_data, allow_expired=allow_expired)
    #     ibcontract_pattern = ib_futures_instrument(futures_instrument_with_ib_data)
    #     contract_list = self.ib_get_contract_chain(
    #         ibcontract_pattern, allow_expired=allow_expired
    #     )
    #     # if no contracts found will be empty
    #     # Extract expiry date strings from these
    #     list_of_contracts = [ibcontract.lastTradeDateOrContractMonth for ibcontract in contract_list]
    #     return listOfContractDateStr(list_of_contracts)
