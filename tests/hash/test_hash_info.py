import json
import unittest

from alvarium.hash.contracts import HashInfo, HashType

class TestHashInfo(unittest.TestCase):

    def test_to_json_should_return_json_representation(self):
        hash_info = HashInfo(type=HashType.MD5)
        test_json = ""
        with open("./tests/hash/hash_info.json", "r") as file:
            test_json = json.loads(file.read()) 

        result = hash_info.to_json()
        self.assertEqual(json.loads(result), test_json) 

    def test_from_json_should_return_hash_info(self):
        test_json = ""
        with open("./tests/hash/hash_info.json", "r") as file:
            test_json = file.read()
        
        hash_info = HashInfo.from_json(data=test_json)
        self.assertEqual(hash_info.type, HashType.MD5)

if __name__ == "__main__":
    unittest.main()