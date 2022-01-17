import json
from typing import List
import unittest

from alvarium.contracts.annotation import Annotation, AnnotationList, AnnotationType
from alvarium.hash.contracts import HashType

class TestAnnotationList(unittest.TestCase):

    def test_to_json_should_return_json_representation(self):
        annotation = Annotation(key="KEY", hash=HashType.NONE, host="host",
                                kind=AnnotationType.MOCK,signature= "SIGN" ,is_satisfied=True)
        annotation_list = AnnotationList(items=[annotation, annotation])
        result = annotation_list.to_json()
        self.assertEqual(type(result), str)
    
    def test_from_json_should_return_annotation_list_object(self):
        test_json = ""
        with open("./tests/contracts/annotation_list.json", "r") as file:
            test_json = file.read()

        annotation_list = AnnotationList.from_json(test_json)
        self.assertEqual(type(annotation_list.items[0]), Annotation) 


if __name__ == "__main__":
    unittest.main()