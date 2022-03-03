Delete FROM bangazon_api_favorite where id = 10

                SELECT 
                    p.name,
                    s.name as store_name
                FROM bangazon_api_product as p
                Join bangazon_api_store as s ON
                p.store_id = s.id
                WHERE price >= 500

                SELECT 
                o.id,
                u.first_name || " " || u.last_name as full_name,
                p.merchant_name,
                SUM(product.price) as order_total
                FROM bangazon_api_order as o
                Join bangazon_api_paymenttype as p ON 
                p.id = o.payment_type_id
                Join auth_user as u ON
                o.user_id = u.id
                Join bangazon_api_orderproduct as op ON
                o.id = op.order_id
                Join bangazon_api_product as product ON
                op.product_id = product.id
                GROUP BY op.order_id    

                SELECT 
                o.id,
                u.first_name || " " || u.last_name as full_name,
                o.created_on,
                SUM(product.price) as order_total
                FROM bangazon_api_order as o
                Join auth_user as u ON
                o.user_id = u.id
                Join bangazon_api_orderproduct as op ON
                o.id = op.order_id
                Join bangazon_api_product as product ON
                op.product_id = product.id
                WHERE o.completed_on IS NULL
                GROUP BY op.order_id    