import unittest
from alvarium.sign.factories import SignProviderFactory
from alvarium.sign.contracts import SignType
from alvarium.sign.interfaces import SignProvider

class TestSignProvider(unittest.TestCase):
    
    def test_none_sign_provider_should_return_data_signed(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider  = factory.getProvider(SignType.NONE)

        test_string = "Signing test string"
        result = sign_provider.sign(bytes(test_string, "utf-8"))
        
        self.assertEqual(result,test_string)
    
    def test_none_sign_provider_should_verify_true_signed_content(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider  = factory.getProvider(SignType.NONE)

        test_string = bytes("Signed Test String", "utf-8")
        signed_test_string = bytes("Signed Test String", "utf-8")

        result = sign_provider.verify(test_string, signed_test_string)

        self.assertTrue(result)
    
    def test_none_sign_provider_should_verify_false_signed_content(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider  = factory.getProvider(SignType.NONE)

        test_string = bytes("Signed Test String", "utf-8")
        changed_signed_test_string = bytes("Changed Signed Test String", "utf-8")

        result = sign_provider.verify(test_string, changed_signed_test_string)
        
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()    

