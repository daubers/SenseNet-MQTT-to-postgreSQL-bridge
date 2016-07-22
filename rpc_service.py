from pulsar import as_coroutine
from pulsar.apps import rpc, wsgi
from pulsar.utils.httpurl import JSON_CONTENT_TYPES
from models import get_session
from models.store import Store
from sqlalchemy import distinct, and_
from models.json_encoder import to_dict
import datetime


class RequestCheck:

    async def __call__(self, request, name):
        data = await as_coroutine(request.body_data())
        assert(data['method'] == name)
        return True


class Root(rpc.PulsarServerCommands):
    """Add two rpc methods for testing to the :class:`.PulsarServerCommands`
    handler.
    """
    rpc_check_request = RequestCheck()


class MQTTDatabase(rpc.JSONRPC):
    """
        Interface into mqtt database
    """
    def rpc_unique_topics(self, request):
        session = get_session()
        data = session.query(distinct(Store.topic)).all()
        session.close()
        return [topic[0] for topic in data]

    def rpc_last_payload_for_topic(self, request, topic):
        session = get_session()
        data = session.query(Store).filter(Store.topic == topic).order_by(Store.timestamp.desc()).first()
        session.close()
        return to_dict(data)

    def rpc_topic_data_between_dates(self, request, topic, from_date, to_date):
        session = get_session()
        from_date = datetime.datetime.fromtimestamp(from_date)
        to_date = datetime.datetime.fromtimestamp(to_date)
        data = session.query(Store).filter(Store.topic == topic).filter(and_(Store.timestamp >= from_date, Store.timestamp <= to_date)).all()
        print(data)
        return [to_dict(i) for i in data]


class Site(wsgi.LazyWsgi):
    """WSGI handler for the RPC server"""
    def setup(self, environ):
        """Called once to setup the list of wsgi middleware."""
        json_handler = Root().putSubHandler('db', MQTTDatabase())
        middleware = wsgi.Router('/', post=json_handler,
                                 accept_content_types=JSON_CONTENT_TYPES)
        response = [wsgi.GZipMiddleware(200)]
        return wsgi.WsgiHandler(middleware=[wsgi.wait_for_body_middleware,
                                            middleware],
                                response_middleware=response)


def server(callable=None, **params):
    return wsgi.WSGIServer(Site(), **params)


if __name__ == '__main__':  # pragma nocover
    server().start()
