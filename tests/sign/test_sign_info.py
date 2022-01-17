from os import path
import unittest
from alvarium.sign.contracts import SignInfo, SignType, KeyInfo
import json
class TestSignInfo(unittest.TestCase):

    def test_to_json_should_return_josn_representation(self):
        public_key_info = KeyInfo(type=SignType.ED25519, path="/path")
        private_key_info = KeyInfo(type=SignType.NONE, path="/path")
        
        sign_info = SignInfo(public=public_key_info, private=private_key_info)

        test_json = ""
        with open("./tests/sign/sign_info.json", "r") as file:
            test_json = json.loads(file.read())

        result = sign_info.to_json()
        
        self.assertEqual(json.loads(result), test_json)
    
    def test_from_json_should_return_sign_info(self):
        sign_json = ""
        with open("./tests/sign/sign_info.json", "r") as file:
            sign_json = file.read()

        sign_info = SignInfo.from_json(data=sign_json)

        self.assertEqual(sign_info.public.type, SignType.ED25519)