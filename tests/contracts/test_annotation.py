import json
import unittest
from alvarium.contracts.annotation import Annotation, AnnotationType
from alvarium.hash.contracts import HashType

class TestAnnotation(unittest.TestCase):

    def test_to_json_should_return_json_representation(self):
        annotation = Annotation(key="KEY", hash=HashType.NONE, host="host",
                                kind=AnnotationType.MOCK,signature= "SIGN", is_satisfied=True)
        test_json = {} 
        with open("./tests/contracts/annotation.json", "r") as file:
            test_json = json.loads(file.read())
        
        result = json.loads(annotation.to_json())
        self.assertEqual(test_json["key"], result["key"])
        self.assertEqual(test_json["hash"], result["hash"])
        self.assertEqual(test_json["host"], result["host"])
        self.assertEqual(test_json["kind"], result["kind"])
        self.assertEqual(test_json["kind"], result["kind"])
        self.assertEqual(test_json["signature"], result["signature"])
        self.assertEqual(test_json["isSatisfied"], result["isSatisfied"])
    
    def test_to_json_should_omit_empty_signature(self):
        annotation = Annotation(key="KEY", hash=HashType.NONE, host="host",
                                kind=AnnotationType.MOCK, is_satisfied=True)
        
        annotation_json = json.loads(annotation.to_json())
        self.assertRaises(KeyError, lambda: annotation_json["signature"])

    
    def test_from_json_should_return_annotation_object(self):
        test_json = ""
        with open("./tests/contracts/annotation.json", "r") as file:
            test_json = file.read()

        result = Annotation.from_json(test_json)
        self.assertEqual(result.id, "01FE0RFFJY94R1ER2AM9BG63E2") 
        self.assertEqual(result.key, "KEY") 
        self.assertEqual(result.hash, HashType.NONE) 
        self.assertEqual(result.host, "host") 
        self.assertEqual(result.kind, AnnotationType.MOCK) 
        self.assertEqual(result.signature, "SIGN") 
        self.assertEqual(result.is_satisfied, True) 
        self.assertEqual(result.timestamp, "2021-08-24T12:22:33.334070489-05:00") 

if __name__ == "__main__":
    unittest.main()