from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class FavoriteListReport(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            db_cursor.execute("""
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
            """)


            dataset = dict_fetch_all(db_cursor)
            stores = []
            
            for row in dataset:
                store = {
                    "store_name": row["store_name"]
                }
                user_dict = next((
                    customer for customer in stores
                    if customer['customer_id'] == row["customer_id"]
                ), None
                )
                if user_dict:
                    user_dict["store_name"].append(store)
                else:
                    stores.append({
                        "customer_id": row['customer_id'],
                        "customer_name": row["full_name"],
                        "stores": [store]
                    })
                
                
        template = 'products/favorites.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "stores": stores
        }

        return render(request, template, context)