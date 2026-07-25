import dlt

from sources import customers
from sources import employees
from sources import order_items
from sources import orders
from sources import products
from sources import stores


pipeline = dlt.pipeline(
    pipeline_name="walmart_pipeline",
    destination="snowflake",
    dataset_name="RAW"
)


def run_pipeline():

    info = pipeline.run(
        [
            customers(),
            employees(),
            order_items(),
            orders(),
            products(),
            stores(),
        ]
    )

    print(info)