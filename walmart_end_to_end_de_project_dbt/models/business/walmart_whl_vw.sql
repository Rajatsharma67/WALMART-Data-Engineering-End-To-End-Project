{{ config(
    materialized='view',
    schema='RPT_VIEWS'
) }}

SELECT
* 
FROM {{ ref('walmart_obt')}}