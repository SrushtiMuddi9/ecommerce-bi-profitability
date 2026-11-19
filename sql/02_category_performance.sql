
-- Top 10 product categories by item revenue

SELECT
    product_category_name_english AS product_category,
    ROUND(SUM(item_revenue), 2) AS total_revenue,
    COUNT(*) AS total_items_sold,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(item_revenue), 2) AS average_item_price
FROM sales
WHERE order_status NOT IN ('canceled', 'unavailable')
GROUP BY product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;
