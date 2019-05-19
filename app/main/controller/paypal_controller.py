from flask_restplus import Resource
from app.main.model.usuario import Usuario
from app.main.util.dto import PaypalDto
from app.main.service.producto_service import get_a_product, marcar_venta_realizada
from app.main.service.paypal_service import auth_token, realizar_compra, capturar_compra, realizar_pago_a_vendedor, ids

api = PaypalDto.api


@api.route('/venta_producto/<id_producto>')
class PaypalCompra(Resource):
    @api.response(200, 'OK.')
    @api.response(400, 'Bad request.')
    @api.response(404, 'Producto no encontrado')
    def post(self, id_producto):
        """Inicia la compra por Paypal del producto con id id_producto. Devuelve la url de compra y el id de transacción de paypal."""
        producto = get_a_product(id_producto)

        if 'id' in producto:
            email_vendedor = Usuario.query.filter_by(public_id=producto['vendedor']).first().email
            auth_token()
            if producto['tipo'] == 'normal':
                precio = producto['precioBase']
            else:
                precio = producto['precioAux']
            respuesta = realizar_compra(id_producto=id_producto, precio=precio,
                                        return_url="http://155.210.47.51:5000/paypal/captura/" + str(id_producto))
            ids.setdefault('id_producto', {'id_paypal': respuesta['id'], 'email': email_vendedor,
                           'producto_name': producto['titulo'], 'precio': precio})
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

        capturar_compra(infopaypal['id_paypal'])
        respuesta = realizar_pago_a_vendedor(email=infopaypal['email'], producto_name=infopaypal['producto_name'],
                                             producto_id=id_producto, precio=infopaypal['precio'])

        print(respuesta.content)

        marcar_venta_realizada(paypal=True)

        return ({'status': 'success', 'message': 'Venta realizada'}), 200
