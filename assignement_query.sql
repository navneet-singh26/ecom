WITH LastYearOrders AS (
    SELECT
        o.order_id,
        o.customer_id,
        SUM(oi.quantity * oi.price_per_unit) AS total_spent
    FROM
        Orders o
        JOIN Order_Items oi ON o.order_id = oi.order_id
    WHERE
        o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    GROUP BY
        o.order_id, o.customer_id
),
CustomerSpending AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.email,
        SUM(lyo.total_spent) AS total_spent
    FROM
        Customers c
        JOIN LastYearOrders lyo ON c.customer_id = lyo.customer_id
    GROUP BY
        c.customer_id, c.customer_name, c.email
),
CustomerCategorySpending AS (
    SELECT
        c.customer_id,
        p.category,
        SUM(oi.quantity * oi.price_per_unit) AS category_spent
    FROM
        Customers c
        JOIN Orders o ON c.customer_id = o.customer_id
        JOIN Order_Items oi ON o.order_id = oi.order_id
        JOIN Products p ON oi.product_id = p.product_id
    WHERE
        o.order_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    GROUP BY
        c.customer_id, p.category
),
CustomerMostPurchasedCategory AS (
    SELECT
        customer_id,
        category AS most_purchased_category,
        RANK() OVER (PARTITION BY customer_id ORDER BY category_spent DESC) AS rank
    FROM
        CustomerCategorySpending
)
SELECT
    cs.customer_id,
    cs.customer_name,
    cs.email,
    cs.total_spent,
    cmc.most_purchased_category
FROM
    CustomerSpending cs
    JOIN CustomerMostPurchasedCategory cmc ON cs.customer_id = cmc.customer_id
WHERE
    cmc.rank = 1
ORDER BY
    cs.total_spent DESC
LIMIT 5;