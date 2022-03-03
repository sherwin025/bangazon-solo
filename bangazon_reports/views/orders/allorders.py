from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all

class OrderListReport(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            db_cursor.execute("""
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
            """)


            dataset = dict_fetch_all(db_cursor)
            oders = []
            
            for row in dataset:
                order = {
                    "order_id": row["id"], "fullname": row["full_name"], "merchant_name": row["merchant_name"], "order_total": row["order_total"]
                }
                oders.append(order)
                
            
            db_cursor.execute("""
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
            """)


            dataset = dict_fetch_all(db_cursor)
            theorders = []
            
            for row in dataset:
                order = {
                    "order_id": row["id"], "fullname": row["full_name"], "created_on": row["created_on"], "order_total": row["order_total"]
                }
                theorders.append(order)

        template = 'products/orders.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "completed_orders": oders,
            "uncompleted_orders": theorders
        }

        return render(request, template, context)