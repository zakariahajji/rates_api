## Task 1 - Exchange Rates Import

###  1 -



~~~~sql
CREATE TABLE `aggregated_revenues`
(
  extracted_at TIMESTAMP, -- extraction time, 
  amount NUMERIC,
  type STRING, -- expense or billing or .. 
  base STRING, -- base for amount column
  converted BOOL, -- state of column `amount`.
  convert_rate NUMERIC, -- rate of conversion, base reference should be fixed at api level
  conversion_ts TIMESTAMP, -- timestamp of conversion
)
~~~~



| extracted_at        | amount | type    | base | converted | convert_rate | conversion_ts       |
|---------------------|--------|---------|------|-----------|------------|---------------------|
| 2022-04-01 14:00:00 | 200    | expense | USD  | TRUE      |     0,93       | 2022-04-02 00:01:00 |

### 2 -

- Snippet to call this API is implemented within a class  in `plugins/operators/rates_api.py`, and will be used in another standalone script.

- To see this API in action, I have created sample data in `scripts/sample_data`.

To reproduce this :

1. Clone this repo : 

2. In your terminal execute the following : 

- ``export PYTHONPATH="${PWD}:${PYTHONPATH}:${PWD}/scripts:${PWD}/plugins"``

- ``python scripts/main.py ``

The script will read a source JSON from : ```scripts/sample_data/billing_and_expenses.json```

````
[
    {"base": "EUR", "amount": 100},
    {"base": "USD", "amount": 250},
    {"base": "CZK", "amount": "140,2"},
    {"base": "USD", "amount": 131},
    {"base": "CZK", "amount": 300},
    {"base": "EUR", "amount": 500},
    {"base": "USD", "amount": 800},
    {"base": "CZK", "amount": 600},
    {"base": "EUR", "amount": "20,6"}
]
````

And convert it to :
``scripts/sample_data/billing_and_expenses_converted.json``

```
[
    {"base": "USD", "amount": 108.78},
    {"base": "USD", "amount": 250},
    {"base": "USD", "amount": 6.236364},
    {"base": "USD", "amount": 131},
    {"base": "USD", "amount": 13.363636},
    {"base": "USD", "amount": 543.9},
    {"base": "USD", "amount": 800},
    {"base": "USD", "amount": 26.727273},
    {"base": "USD", "amount": 21.756},
]
```


## Task 2 - Data stack improvements

- This is the typical use-case of a scheduler, Airflow for example, an open source scheduler that can be run within instances like [_composer_](https://cloud.google.com/composer?hl=fr) , [MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html) , or simply a VM , or third party providers like [Astronomer](https://www.astronomer.io/) (recommended for small teams)
Can schedule executions of scripts ( like the one we have ) : calls from APIs, or queries and uses ( It's an orchestrator, it's not supposed to do the actual job) [Operators](https://registry.astronomer.io/providers/amazon) ( AWS,GCP services, Python scripts .. ) to trigger the relevant service that will do the job. ( We can allow small python scripts to be executed at run-time within airflow), but for big data throughput transformations we need to privilege a transformation cluster/instance in a processing server that we will "schedule" to run on our data.
---
- Ideally, in modern data engineering architectures we tend to avoid the E~~T~~L, where we become quickly dependent on transformation clusters, ELT is much more flexible, as tools like dbt on Redshift, BigQuery allow scalable transformation/processing using just SQL.
---
- Improvements for current script : 
  - The  ``/dag``, and ``/plugins`` structure of the repo should fit into an Airflow instance.
  - In the ``/dag`` file, we can find a dag containing tasks to orchestrate.
  - In our case ( needs testing ), a production implementation of this would mean 
    - Using an Operator like `RedshiftSQLOperator` to access data in Redshift
    - Use Jinja ( supported by airflow ) [templating](https://towardsdatascience.com/advanced-sql-templates-in-python-with-jinjasql-b996eadd761d) to pass rates that we get from previous script within query. rates will be evaluated at runtime and should be up to date.
  - ![alt text](https://github.com/zakariahajji/rates_api/blob/master/images/img.png)

