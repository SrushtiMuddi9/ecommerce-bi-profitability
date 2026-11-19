
-- Monthly item revenue and month-over-month growth

WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', order_purchase_timestamp) AS sales_month,
        ROUND(SUM(item_revenue), 2) AS monthly_revenue,
        COUNT(DISTINCT order_id) AS total_orders
    FROM sales
    WHERE order_status NOT IN ('canceled', 'unavailable')
      AND order_purchase_timestamp IS NOT NULL
    GROUP BY strftime('%Y-%m', order_purchase_timestamp)
),
revenue_with_previous_month AS (
    SELECT
        sales_month,
        monthly_revenue,
        total_orders,
        LAG(monthly_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_month_revenue
    FROM monthly_sales
)
SELECT
    sales_month,
    monthly_revenue,
    total_orders,
    previous_month_revenue,
    ROUND(
        100.0 * (monthly_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0),
        2
    ) AS revenue_growth_pct
FROM revenue_with_previous_month
ORDER BY sales_month;
