{{ config(
    materialized='table',
    schema='GOLD'
) }}

SELECT
    o.ORDER_ID,
    o.ORDER_TIMESTAMP,
    o.PAYMENT_METHOD,
    o.ORDER_STATUS,
    o.TOTAL_AMOUNT,
    c.CUSTOMER_ID,
    c.FIRST_NAME AS CUSTOMER_FIRST_NAME,
    c.LAST_NAME AS CUSTOMER_LAST_NAME,
    c.EMAIL AS CUSTOMER_EMAIL,
    c.PHONE AS CUSTOMER_PHONE,
    c.CITY AS CUSTOMER_CITY,
    c.PROVINCE AS CUSTOMER_PROVINCE,
    c.COUNTRY AS CUSTOMER_COUNTRY,
    s.STORE_ID,
    s.STORE_NAME,
    s.CITY AS STORE_CITY,
    s.PROVINCE AS STORE_PROVINCE,
    s.COUNTRY AS STORE_COUNTRY,
    e.EMPLOYEE_ID,
    e.FIRST_NAME AS EMPLOYEE_FIRST_NAME,
    e.LAST_NAME AS EMPLOYEE_LAST_NAME,
    e.JOB_TITLE,
    e.SALARY,
    oi.ORDER_ITEM_ID,
    oi.QUANTITY,
    oi.UNIT_PRICE,
    oi.LINE_AMOUNT,
    p.PRODUCT_ID,
    p.PRODUCT_NAME,
    p.CATEGORY,
    p.BRAND,
    p.PRICE AS PRODUCT_PRICE
FROM {{ ref("stg_orders") }} o
INNER JOIN {{ ref("stg_customers") }} c
    ON o.CUSTOMER_ID = c.CUSTOMER_ID
INNER JOIN {{ ref("stg_stores") }} s
    ON o.STORE_ID = s.STORE_ID
INNER JOIN {{ ref("stg_employees") }} e
    ON s.STORE_ID = e.STORE_ID
INNER JOIN {{ ref("stg_order_items") }} oi
    ON o.ORDER_ID = oi.ORDER_ID
INNER JOIN {{ ref("stg_products") }} p
    ON oi.PRODUCT_ID = p.PRODUCT_ID
