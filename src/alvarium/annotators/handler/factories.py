from requests import Request
from alvarium.annotators.handler.ed25519 import Ed25519RequestHandler
from alvarium.annotators.handler.mock import NoneRequestHandler
from alvarium.sign.contracts import SignInfo, SignType
from .interfaces import RequestHandler
from .exceptions import RequestHandlerException

class RequestHandlerFactory():

    def getRequestHandler(self, request: Request, keys: SignInfo) -> RequestHandler:
        if keys.private.type == SignType.NONE:
            return NoneRequestHandler(request=request)
        if keys.private.type == SignType.ED25519:
            return Ed25519RequestHandler(request=request)
        else:
            raise RequestHandlerException("Key type is not supported")
