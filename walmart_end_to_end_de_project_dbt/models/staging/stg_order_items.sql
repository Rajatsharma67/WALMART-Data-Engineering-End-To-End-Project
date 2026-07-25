SELECT
{{ dbt_utils.star(
    from=source('raw', 'order_items'),
    except=['_DLT_LOAD_ID', '_DLT_ID']
) }}
FROM {{ source('raw', 'order_items') }}