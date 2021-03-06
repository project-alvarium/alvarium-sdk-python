import unittest

from alvarium.hash.contracts import HashType

from alvarium.hash.factories import HashProviderFactory
from alvarium.hash.interfaces import HashProvider

class TestHashProvider(unittest.TestCase):

    def test_none_provider_should_return_data(self):
        factory = HashProviderFactory()
        hash_provider: HashProvider = factory.get_provider(HashType.NONE)

        test_string = "this is a test"
        result = hash_provider.derive(data=bytes(test_string, "utf-8"))
        self.assertEqual(result, test_string)

    def test_sha256_provider_should_return_hex_of_hashed_data(self):
        factory = HashProviderFactory()
        hash_provider: HashProvider = factory.get_provider(HashType.SHA256)

        test_string = b"this is a test"
        test_string_hex = "2e99758548972a8e8822ad47fa1017ff72f06f3ff6a016851f45c398732bc50c" #ground truth
        result = hash_provider.derive(data=test_string)
        self.assertEqual(result, test_string_hex)

    def test_md5_provider_should_return_hex_of_hashed_data(self):
        factory = HashProviderFactory()
        hash_provider: HashProvider = factory.get_provider(HashType.MD5)

        test_string = b"this is a test"
        test_string_hex = "54b0c58c7ce9f2a8b551351102ee0938" #ground truth
        result = hash_provider.derive(data=test_string)
        self.assertEqual(result, test_string_hex)



if __name__ == "__main__":
    unittest.main()