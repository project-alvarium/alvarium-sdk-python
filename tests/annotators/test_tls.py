import unittest

from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType
from alvarium.annotators.factories import AnnotatorFactory
from alvarium.utils import ImmutablePropertyBag
import ssl
import socket

class TlsAnnotatorTest(unittest.TestCase):
    def test_tls_annotator_with_tls_connection_should_return_is_satisfied_true(self):
        keyInfo = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        factory = AnnotatorFactory()
        annotator = factory.getAnnotator( kind = AnnotationType.TLS, hash = HashType.SHA256, signature = SignInfo(keyInfo, keyInfo))
        string = "test data"
        data = bytes(string, 'utf-8')

        hostname = 'google.com'
        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname, do_handshake_on_connect=False) as ssock:
                ctx = ImmutablePropertyBag({str(AnnotationType.TLS): ssock})
                annotation = annotator.execute(ctx, data)
        
        self.assertEqual(annotation.is_satisfied, True)
        self.assertEqual(type(annotation), Annotation)

        
    def test_tls_annotator_without_tls_connection_should_return_is_satisfied_false(self):
        keyInfo = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        factory = AnnotatorFactory()
        annotator = factory.getAnnotator( kind = AnnotationType.TLS, hash = HashType.SHA256, signature = SignInfo(keyInfo, keyInfo))
        string = "test data"
        data = bytes(string, 'utf-8')
        
        #Handshake fails in this website so tls shoudl be false
        hostname = 'googel.com'
        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname, do_handshake_on_connect=False) as ssock:
                ctx = ImmutablePropertyBag({str(AnnotationType.TLS): ssock})
                annotation = annotator.execute(ctx, data)

        self.assertEqual(annotation.is_satisfied, False)
        self.assertEqual(type(annotation), Annotation)