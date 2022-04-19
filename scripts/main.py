import json
import logging
import os

from plugins.operators.rates_api import GetRates

TARGET_CURR = "USD" # Target currency we want to exchange to (Only variable to change!)

def extract_non_converted_rates():
    """
    Mocking a source interface of data, typically should be a source table
    """
    with open(
        f"{os.getcwd()}/scripts/sample_data/billing_and_expenses.json"
    ) as billing_and_expenses:
        data = json.load(billing_and_expenses)
        logging.info(f"Source rates : {data}")
        return data


def apply_exchange_rates(data):
    """
    Using class GetRates in plugins/operators/rates_api.py to exchange rates
    """

    def apply_rates(source, element):
        rate = GetRates(source, element["amount"]).get_rates()
        return rate

    converted_rates = []
    for data_values in data:
        logging.info(f"Applying transformations")
        rates_payload = apply_rates(source=data_values["base"], element=data_values)
        data_values["base"], data_values["amount"] = (
            TARGET_CURR,
            rates_payload[TARGET_CURR],
        )
        converted_rates.append(dict(data_values).copy())
    return converted_rates


def load_converted_rates(converted_rates):
    """
    Mocking load step in an ETL : typically Loading in a target table converted rates
    """
    logging.info(f"Converted rates : {converted_rates}")
    with open(
        f"{os.getcwd()}/scripts/sample_data/billing_and_expenses_converted.json", "w"
    ) as f:
        json.dump(converted_rates, f)
        f.write("\n")


if __name__ == "__main__":
    data = extract_non_converted_rates()
    converted_rates = apply_exchange_rates(data)
    load_converted_rates(converted_rates)
