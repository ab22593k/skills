import requests

class PaymentService:
    def __init__(self, api_key, gateway_url):
        self.api_key = api_key
        self.gateway_url = gateway_url

    def process_payment(self, order_id, amount, currency="USD"):
        resp = requests.post(
            f"{self.gateway_url}/charge",
            json={"order_id": order_id, "amount": amount, "currency": currency},
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def refund(self, transaction_id, amount):
        resp = requests.post(
            f"{self.gateway_url}/refund",
            json={"transaction_id": transaction_id, "amount": amount},
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()
