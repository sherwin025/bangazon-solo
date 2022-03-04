from bangazon_api.models.payment_type import PaymentType
from bangazon_api.models.rating import Rating
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.core.management import call_command
from django.contrib.auth.models import User

from bangazon_api.models import Order, Product


class OrderTests(APITestCase):
    def setUp(self):
        """
        Seed the database
        """
        call_command('seed_db', user_count=3)
        self.user1 = User.objects.filter(store=None).first()
        self.token = Token.objects.get(user=self.user1)

        self.user2 = User.objects.filter(store=None).last()
        self.product = Product.objects.get(pk=1)

        # self.order1 = Order.objects.create(
        #     user=self.user1
        # )

        # self.order1.products.add(product)

        self.order2 = Order.objects.create(
            user=self.user2
        )

        self.order2.products.add(self.product)

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.payment = PaymentType.objects.create(
            merchant_name="visa",
            acct_number= 123412341234,
            customer=self.user1
        )

    def test_list_orders(self):
        """The orders list should return a list of orders for the logged in user"""
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # def test_delete_order(self):
    #     response = self.client.delete(f'/api/orders/{self.order1.id}')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_product_to_order(self):
        theorder = self.client.post(f'/api/products/{self.product.id}/add_to_order')
        self.assertEqual(theorder.status_code, status.HTTP_201_CREATED)
        
    def test_add_payment(self):
        theorder = self.client.get('/api/orders/current')
        theorder.data['payment_type'] = self.payment.id
        response = self.client.put(f'/api/orders/{theorder.data["id"]}/complete', theorder.data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        anorder = Order.objects.get(pk=theorder.data['id'])
        
        self.assertEqual(anorder.payment_type, self.payment)
        
    def test_delete_payment_type(self):
        paymenttype = self.client.delete(f'/api/payment-types/{self.payment.id}')
        self.assertEqual(paymenttype.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_rate_and_average_rating(self):
        product = self.client.get('/api/products/1')

        ratings = len(product.data["ratings"])
        
        rating = {
            "customer": self.user1,
            "product": Product.objects.get(pk=2),
            "score": 4,
            "review": "great product"
        }
        
        self.client.post(f'/api/products/{product.data["id"]}/rate-product', rating)
        
        updatedproduct = self.client.get('/api/products/1')
    
        self.assertNotEqual(product.data["average_rating"], updatedproduct.data["average_rating"])