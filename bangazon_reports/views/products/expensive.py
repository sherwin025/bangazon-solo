from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class ProductListReport(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            db_cursor.execute("""
                SELECT 
                    p.name,
                    s.name as store_name
                FROM bangazon_api_product as p
                Join bangazon_api_store as s ON
                p.store_id = s.id
                WHERE price >= 900
            """)


            dataset = dict_fetch_all(db_cursor)
            products = []
            
            for row in dataset:
                product = {
                    "product_name": row["name"], "store_name": row["store_name"]
                }
                products.append(product)
                
            db_cursor.execute("""
                SELECT 
                    p.name,
                    s.name as store_name
                FROM bangazon_api_product as p
                Join bangazon_api_store as s ON
                p.store_id = s.id
                WHERE price <= 900
            """)

            dataseta = dict_fetch_all(db_cursor)
            productsunder = []
            
            for row in dataseta:
                product = {
                    "product_name": row["name"], "store_name": row["store_name"]
                }
                productsunder.append(product)
            

        template = 'products/expensive_products.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "products_over_1000": products,
            "products_under_1000": productsunder
        }

        return render(request, template, context)