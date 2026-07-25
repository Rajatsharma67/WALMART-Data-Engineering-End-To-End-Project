SELECT
{{ dbt_utils.star(
    from=source('raw', 'products'),
    except=['_DLT_LOAD_ID', '_DLT_ID']
) }}
FROM {{ source('raw', 'products') }}