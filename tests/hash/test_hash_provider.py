import unittest

from alvarium.hash.contracts import HashType

from alvarium.hash.factories import HashProviderFactory
from alvarium.hash.interfaces import HashProvider

class TestHashProvider(unittest.TestCase):

    def test_none_provider_should_return_data(self):
        factory = HashProviderFactory()
        hash_provider: HashProvider = factory.getProvider(HashType.NONE)

        test_string = "this is a test"
        result = hash_provider.derive(bytes(test_string, "utf-8"))
        self.assertEqual(result, test_string)


if __name__ == "__main__":
    unittest.main()