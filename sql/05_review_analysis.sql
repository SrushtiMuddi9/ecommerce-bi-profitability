
-- Customer satisfaction by average order review score
SELECT
    ROUND(average_review_score, 0) AS review_score_group,
    COUNT(*) AS total_orders,
    ROUND(AVG(average_review_score), 2) AS average_score
FROM reviews
WHERE average_review_score IS NOT NULL
GROUP BY ROUND(average_review_score, 0)
ORDER BY review_score_group;

