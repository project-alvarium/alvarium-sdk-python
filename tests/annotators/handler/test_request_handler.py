import unittest
from requests import Request

from alvarium.annotators.handler.factories import RequestHandlerFactory
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType

class TestHandler(unittest.TestCase):

    def test_request_handler_should_add_signature_headers(self):
        key_info = KeyInfo(type=SignType.NONE,path="path")
        sign_info = SignInfo(key_info, key_info)
        req = Request(method='POST', url="")

        handler = RequestHandlerFactory().getRequestHandler(request=req,keys=sign_info)
        handler.AddSignatureHeaders()

        signature_input = handler.request.headers['Signature-Input']
        signature = handler.request.headers['Signature']

        self.assertEqual(signature_input,"")
        self.assertEqual(signature,"")