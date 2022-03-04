                SELECT
                f.customer_id as id,
                u.first_name || " " || u.last_name as full_name,
                s.id as store_id,
                s.name as store_name
                FROM auth_user as u
                Join bangazon_api_favorite as f ON
                f.customer_id = u.id
                Join bangazon_api_store as s ON
                f.store_id = s.id

                                SELECT
                u.id as customer_id,
                u.first_name || " " || u.last_name as full_name,
                s.id as store_id,
                s.name as store_name
                FROM bangazon_api_favorite as f 
                Join auth_user as u ON
                f.customer_id = u.id
                Join bangazon_api_store as s ON
                f.store_id = s.id

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