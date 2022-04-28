import unittest
import json
import datetime

from requests import Request

from alvarium.annotators.factories import AnnotatorFactory
from alvarium.annotators.handler.factories import RequestHandlerFactory
from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.contracts.config import SdkInfo
from alvarium.hash.contracts import HashInfo, HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType
from alvarium.annotators.handler.contracts import DerivedComponent, HttpConstants
from alvarium.utils import ImmutablePropertyBag
from alvarium.annotators.exceptions import AnnotatorException


class TestPkiHttp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestPkiHttp, self).__init__( *args, **kwargs)

        kind = AnnotationType.PKI_HTTP
        hash = HashType.SHA256
        pub_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/public.key")
        priv_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        sdk_info = SdkInfo(annotators=[], hash=HashInfo(type=hash), stream=None, 
                            signature=SignInfo(public=pub_key, private=priv_key))
        self.annotator = AnnotatorFactory().get_annotator(kind=kind, sdk_info=sdk_info)
        self.request = self.buildRequest(keys=sdk_info.signature)

    def test_httppki_execute_valid_test(self):

        ctx = ImmutablePropertyBag({HttpConstants().http_request_key: self.request})

        annotation = self.annotator.execute(data=bytes(self.request.json, 'utf-8'), ctx=ctx)
        
        self.assertTrue(annotation.is_satisfied)
        self.assertEqual(type(annotation), Annotation)


    def test_httppki_execute_invalid_algorithm_test(self):

        modified_request = self.request
        modified_request.headers['Signature-Input'] = '\"@method\" \"@path\" \"@authority\" \"Content-Type\" \"Content-Length\";created=1646146637;keyid=\"public.key\";alg=\"invalid\"'
        ctx = ImmutablePropertyBag({HttpConstants().http_request_key: modified_request})

        with self.assertRaises(AnnotatorException):
            self.annotator.execute(data=bytes(modified_request.json, 'utf-8'), ctx=ctx)
        

    def test_httppki_execute_invalid_key_test(self):

        modified_request = self.request
        modified_request.headers['Signature-Input'] = '\"@method\" \"@path\" \"@authority\" \"Content-Type\" \"Content-Length\";created=1646146637;keyid=\"invalid\";alg=\"ed25519\"'
        ctx = ImmutablePropertyBag({HttpConstants().http_request_key: modified_request})

        with self.assertRaises(AnnotatorException):
            self.annotator.execute(data=bytes(modified_request.json, 'utf-8'), ctx=ctx)



    def test_httppki_execute_empty_signature_test(self):

        modified_request = self.request
        modified_request.headers['signature'] = ""
        
        ctx = ImmutablePropertyBag({HttpConstants().http_request_key: modified_request})

        # with self.assertRaises(AnnotatorException):
        annotation = self.annotator.execute(data=bytes(modified_request.json, 'utf-8'), ctx=ctx)
        self.assertFalse(annotation.is_satisfied)
            
    
    def test_httppki_execute_invalid_signature_syntax_test(self):

        modified_request = self.request
        modified_request.headers['signature'] = "invalid"
        
        ctx = ImmutablePropertyBag({HttpConstants().http_request_key: modified_request})

        with self.assertRaises(AnnotatorException):
            self.annotator.execute(data=bytes(modified_request.json, 'utf-8'), ctx=ctx)

    def test_httppki_execute_incorrect_signature_test(self):

        modified_request = self.request
        modified_request.headers['signature'] = "123456"
        
        ctx = ImmutablePropertyBag({HttpConstants().http_request_key: modified_request})

        annotation = self.annotator.execute(data=bytes(modified_request.json, 'utf-8'), ctx=ctx)
        self.assertFalse(annotation.is_satisfied)


    def buildRequest(self, keys: SignInfo):
    
        payload = {'KeyA': 'This is some test data'}
        headers = {'Content-Type': 'application/json',
		        "Date":"Tue, 20 Apr 2021 02:07:55 GMT",
                'Content-Length':'18'}

        ticks = datetime.datetime.now()

        # The URL has to be a absolute
        url = 'http://example.com/foo?var1=&var2=2'
        
        data=json.dumps(payload)

        fields = [DerivedComponent.Method, DerivedComponent.Path, DerivedComponent.Authority, HttpConstants().content_type, HttpConstants().content_length]
        req = Request(method='POST',url=url,headers=headers,json=data)
        
        handler = RequestHandlerFactory().getRequestHandler(request=req,keys=keys)
        handler.AddSignatureHeaders(ticks=ticks, fields=fields, keys=keys)

        return handler.request


if __name__ == "__main__":
    unittest.main()