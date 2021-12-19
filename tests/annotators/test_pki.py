from typing import Type
import unittest

from alvarium.annotators.factories import AnnotatorFactory
from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.contracts.config import SdkInfo
from alvarium.hash.contracts import HashInfo, HashType
from alvarium.sign.contracts import KeyInfo, SignInfo, SignType
from alvarium.annotators.contracts import Signable

class TestPki(unittest.TestCase):

    def test_pki_execute_should_return_satisfied_annotation(self):
        kind = AnnotationType.PKI
        hash = HashType.SHA256
        pub_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/public.key")
        priv_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        sdk_info = SdkInfo(annotators=[], hash=HashInfo(type=hash), stream=None, 
                           signature=SignInfo(public=pub_key, private=priv_key))
        annotator = AnnotatorFactory().get_annotator(kind=kind, sdk_info=sdk_info)
        
        seed = "helloo"
        signature = "B9E41596541933DB7144CFBF72105E4E53F9493729CA66331A658B1B18AC6DF5DA991" + \
                    "AD9720FD46A664918DFC745DE2F4F1F8C29FF71209B2DA79DFD1A34F50C"

        test_data = Signable(seed=seed, signature=signature)
        annotation = annotator.execute(data=bytes(test_data.to_json(), 'utf-8'))

        self.assertTrue(annotation.is_satisfied)
        self.assertEqual(type(annotation), Annotation)
    
    def test_pki_execute_should_return_unsatisfied_annotation(self):
        kind = AnnotationType.PKI
        hash = HashType.SHA256
        pub_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/public.key")
        priv_key = KeyInfo(type=SignType.ED25519, path="./tests/sign/keys/private.key")
        sdk_info = SdkInfo(annotators=[], hash=HashInfo(type=hash), stream=None, 
                           signature=SignInfo(public=pub_key, private=priv_key))
        annotator = AnnotatorFactory().get_annotator(kind=kind, sdk_info=sdk_info)
        
        seed = "hello"
        signature = "B9E41596541933DB7144CFBF72105E4E53F9493729CA66331A658B1B18AC6DF5DA991" + \
                    "AD9720FD46A664918DFC745DE2F4F1F8C29FF71209B2DA79DFD1A34F50C"

        test_data = Signable(seed=seed, signature=signature)
        annotation = annotator.execute(data=bytes(test_data.to_json(), 'utf-8'))

        self.assertFalse(annotation.is_satisfied)
        self.assertEqual(type(annotation), Annotation)

if __name__ == "__main__":
    unittest.main()