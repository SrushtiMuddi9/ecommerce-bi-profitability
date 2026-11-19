-- Revenue performance by seller state
SELECT
    seller_state,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(AVG(item_revenue), 2) AS average_item_price
FROM sales
WHERE order_status NOT IN ('canceled', 'unavailable')
GROUP BY seller_state
ORDER BY total_revenue DESC
LIMIT 10;