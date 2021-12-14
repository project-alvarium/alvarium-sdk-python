import unittest
import json

from alvarium.annotators.contracts import Signable

class TestContracts(unittest.TestCase):

    def test_signable_from_json_should_return_signable_object(self):
        seed = "this is a seed"
        signature = "signature"
        test_json = {
            "seed": seed,
            "signature": signature
        }

        result = Signable.from_json(json.dumps(test_json))
        self.assertEqual(result.seed, seed)
        self.assertEqual(result.signature, signature)

    def test_signable_to_json_should_return_right_representation(self):
        seed = "this is a seed"
        signature = "signature"

        signable = Signable(seed=seed, signature=signature)
        result = signable.to_json()
        result_json = json.loads(result)

        self.assertEqual(result_json["seed"], seed)
        self.assertEqual(result_json["signature"], signature)


if __name__ == "__main__":
    unittest.main()

