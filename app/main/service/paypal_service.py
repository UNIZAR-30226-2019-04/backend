import base64
import json

import requests
import sys

from app.main.config import PAYPAL_CLIENT_ID, PAYPAL_SECRET

auth_token_paypal = None
ids = {}


def auth_token():
    """
    Devuelve el token necesario para las llamadas a la API de PayPal
    """
    a = (base64.b64encode(bytes(PAYPAL_CLIENT_ID + ":" + PAYPAL_SECRET, "utf-8"))).decode("utf-8")

    sys.modules[__name__].auth_token_paypal = json.loads((requests.request(
        "POST", "https://api.sandbox.paypal.com/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        headers={
            'accept': "application/json",
            'accept-language': "en_US",
            'content-type': "application/x-www-form-urlencoded",
            'authorization': "Basic " + a
        }).content).decode("utf-8"))["access_token"]


def realizar_compra(id_producto, precio: float, return_url: str):
    auth_token_paypal = sys.modules[__name__].auth_token_paypal
    return json.loads((requests.request("POST", "https://api.sandbox.paypal.com/v1/checkout/orders", data="""{
        \"intent\": \"SALE\",
        \"purchase_units\": [
            {
                \"reference_id\": \"Venta""" + str(id_producto) + """\",
                \"amount\": {
                    \"currency\": \"EUR\",
                    \"total\": \"""" + str(precio) + """\"
                }
            }
        ],
        \"redirect_urls\": {
        \"return_url\": \"""" + return_url + """\",
        \"cancel_url\": \"http://paypal.com/\"
  }
    }""", headers={
        'content-type': "application/json",
        'authorization': "Bearer " + auth_token_paypal
    })).content.decode("utf-8"))


def capturar_compra(id):
    auth_token_paypal = sys.modules[__name__].auth_token_paypal
    return json.loads((requests.request("POST", "https://api.sandbox.paypal.com/v1/checkout/orders/" + id + "/capture",
                                        headers={
                                            'content-type': "application/json",
                                            'authorization': "Bearer " + auth_token_paypal
                                        })).content.decode("utf-8"))


def realizar_pago_a_vendedor(email: str, producto_name, producto_id, precio: float):
    auth_token_paypal = sys.modules[__name__].auth_token_paypal
    return requests.request("POST", "https://api.sandbox.paypal.com/v1/payments/payouts", data=("""{
        \"sender_batch_header\": {
            \"sender_batch_id\": \"Venta_final_Telocam_""" + str(producto_id) + """\",
            \"email_subject\": \"¡Has vendido un producto!\",
            \"email_message\": \"¡Enhorabuena, has vendido tu producto en Telocam!\"
        },
        \"items\": [
            {
                \"recipient_type\": \"EMAIL\",
                \"amount\": {
                    \"value\": \"""" + str(precio) + """\",
                    \"currency\": \"EUR\"
                },
                \"note\": \"Producto vendido: """ + producto_name + """\",
                \"sender_item_id\": \"""" + str(producto_id) + """\",
                \"receiver\": \"""" + email + """\"
            }
        ]
    }""").encode("utf-8"), headers={
        'content-type': "application/json",
        'authorization': "Bearer " + auth_token_paypal
    })
