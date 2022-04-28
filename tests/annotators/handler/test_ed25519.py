import json
import unittest
import datetime

from requests import Request

from alvarium.annotators.handler.contracts import CONTENT_LENGTH, CONTENT_TYPE, DerivedComponent
from alvarium.annotators.handler.factories import RequestHandlerFactory
from alvarium.sign.contracts import SignInfo, KeyInfo

class TestHandler(unittest.TestCase):

    def test_handler_should_return_correct_signature_headers(self):
        with open("./tests/mock-info.json", 'r') as file:
            b = file.read()
        
        ticks = datetime.datetime.now()
        url = 'http://example.com/foo?var1=&var2=2'
        headers = { "Date": str(ticks),
                    'Content-Type': 'application/json',
                    'Content-Length':'10'}

        req = Request(method='POST', url=url, headers=headers)

        info_json = json.loads(b) 
        keys = SignInfo(public = KeyInfo.from_json(json.dumps(info_json["signature"]["public"])),
                            private = KeyInfo.from_json(json.dumps(info_json["signature"]["private"])))

        fields = [DerivedComponent.Method, DerivedComponent.Path, DerivedComponent.Authority, CONTENT_TYPE, CONTENT_LENGTH]

        handler = RequestHandlerFactory().getRequestHandler(request=req,keys=keys)
        handler.AddSignatureHeaders(ticks=ticks, fields=fields, keys=keys)

        result = handler.request.headers['Signature-Input']
        expected = f'"@method" "@path" "@authority" "Content-Type" "Content-Length";created={str(int(ticks.timestamp()))};keyid="{str(keys.public.path)}";alg="{str(keys.public.type)}";'
        
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()