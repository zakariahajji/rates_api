import json
import logging
from datetime import datetime, timedelta
import os

from airflow.decorators import dag, task # DAG and task decorators for interfacing with the TaskFlow API
from plugins.operators.rates_api import GetRates

TARGET_CURR = "EUR"


@dag(
    schedule_interval=timedelta(minutes=30),  # Every 30 minutes
    start_date=datetime(2022, 1, 1),
    catchup=False,
    tags=['exchange_rates'])
def apply_currency_exchange_dag():

    @task()
    def extract_non_converted_rates():
        """
        Mocking a source interface, typically should be a source table
        """
        with open(f"{os.getcwd()}/sample_data/billing_and_expenses.json") as billing_and_expenses:
            data = json.load(billing_and_expenses)
            logging.info(f"Source rates : {data}")
            return data

    @task()
    def apply_exchange_rates(data):
        """
        Using class GetRates in plugins/operators/rates_api.py to exchange rates
        """
        def apply_rates(source, element):
            rate = (GetRates(source, element["amount"]).get_rates())
            return rate

        converted_rates = []

        for data_values in data:
            logging.info(f"Applying transformations")
            rates_payload = apply_rates(source=data_values["base"], element=data_values)
            data_values["base"], data_values["amount"] = TARGET_CURR, rates_payload[TARGET_CURR]

            converted_rates.append(dict(data_values).copy())

        return {"converted_rates" : converted_rates}

    @task()
    def load_converted_rates(converted_rates):

        """

        """
        logging.info(f"Converted rates : {converted_rates}")
        with open(f"{os.getcwd()}/sample_data/billing_and_expenses_converted.json", "w") as f:
            json.dump(converted_rates, f)

    data = extract_non_converted_rates()
    converted_rates = apply_exchange_rates(data)
    load_converted_rates(converted_rates)


apply_currency_exchange_dag = apply_currency_exchange_dag()