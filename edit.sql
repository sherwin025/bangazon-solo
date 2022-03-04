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