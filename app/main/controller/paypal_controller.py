from flask_restplus import Resource

from app.main.config import URL_API
from app.main.model.usuario import Usuario
from app.main.util.dto import PaypalDto
from app.main.service.producto_service import get_a_product, marcar_venta_realizada
from app.main.service.paypal_service import auth_token, realizar_compra, capturar_compra, realizar_pago_a_vendedor, ids

api = PaypalDto.api


@api.route('/venta_producto/<id_producto>/<public_id_comprador>')
class PaypalCompra(Resource):
    @api.response(200, 'OK.')
    @api.response(400, 'Bad request.')
    @api.response(404, 'Producto no encontrado')
    def post(self, id_producto, public_id_comprador):
        """Inicia la compra por Paypal del producto con id id_producto. Devuelve la url de compra y el id de transacción de paypal."""
        producto = get_a_product(id_producto)

        if 'id' in producto:
            email_vendedor = Usuario.query.filter_by(public_id=producto['vendedor']).first().email
            auth_token()
            if producto['tipo'] == 'normal':
                precio = producto['precioBase']
            else:
                precio = producto['precioAux']

            try:
                yaComprado = ids[id_producto]
                return {'id': yaComprado['id_paypal'], 'link': yaComprado['link']}
            except:
                pass

            respuesta = realizar_compra(id_producto=id_producto, precio=precio,
                                        return_url=URL_API + "/paypal/captura/" + str(id_producto))
            ids.setdefault('id_producto', {'id_paypal': respuesta['id'], 'link': respuesta['links'][1]['href'],
                                           'email': email_vendedor, 'producto_name': producto['titulo'],
                                           'precio': precio, 'public_id_comprador': public_id_comprador})
            print("PAYPALCOMPRA", str(respuesta))
            return {'id': respuesta['id'], 'link': respuesta['links'][1]['href']}
        else:
            return producto


@api.route('/captura/<id_producto>')
class PaypalVenta(Resource):
    @api.response(200, 'OK.')
    @api.response(400, 'Bad request.')
    def get(self, id_producto):
        """Captura la transacción de paypal con el id indicado, después de que se haya terminado, para pagar al vendedor la cantidad necesaria y completar la venta. """

        infopaypal = ids['id_producto']

        print("InfoPaypal:", str(infopaypal))

        capturar_compra(infopaypal['id_paypal'])
        respuesta = realizar_pago_a_vendedor(email=infopaypal['email'], producto_name=infopaypal['producto_name'],
                                             producto_id=id_producto, precio=infopaypal['precio'])

        print(respuesta.content)

        marcar_venta_realizada(prod_id=id_producto, comprador=infopaypal['public_id_comprador'], paypal=True)

        return ({'status': 'success', 'message': 'Venta realizada'}), 200
