import unittest
from alvarium.sign.factories import SignProviderFactory
from alvarium.sign.contracts import SignType
from alvarium.sign.interfaces import SignProvider
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


class TestSignProvider(unittest.TestCase):

    def test_none_sign_provider_should_return_data_signed(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider = factory.get_provider(SignType.NONE)

        test_string = "Signing test string"
        result = sign_provider.sign(content=bytes(test_string, "utf-8"))

        self.assertEqual(result, test_string)

    def test_none_sign_provider_should_verify_true_signed_content(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider = factory.get_provider(SignType.NONE)

        test_string = bytes("Signed Test String", "utf-8")
        signed_test_string = bytes("Signed Test String", "utf-8")

        result = sign_provider.verify(content=test_string, signed=signed_test_string)

        self.assertTrue(result)

    def test_none_sign_provider_should_verify_false_signed_content(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider = factory.get_provider(SignType.NONE)

        test_string = bytes("Signed Test String", "utf-8")
        changed_signed_test_string = bytes(
            "Changed Signed Test String", "utf-8")

        result = sign_provider.verify(content=test_string, signed=changed_signed_test_string)

        self.assertFalse(result)

    def test_ed25519_sign_provider_should_return_true(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider = factory.get_provider(SignType.ED25519)

        private_key = Ed25519PrivateKey.generate()
        private_key_bytes = private_key.private_bytes(encoding=serialization.Encoding.Raw,
                                                      format=serialization.PrivateFormat.Raw,
                                                      encryption_algorithm=serialization.NoEncryption()
                                                      )
        public_key_bytes = private_key.public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                                 format=serialization.PublicFormat.Raw
                                                                 )

        test_string = "Signing test string"
        signed_test_string = sign_provider.sign(key=private_key_bytes, content=bytes(test_string, "utf-8"))
        verification_status = sign_provider.verify(key=public_key_bytes, content=bytes(test_string, "utf-8"), 
                                                   signed=bytes.fromhex(signed_test_string))

        self.assertEqual(verification_status, True)

    def test_ed25519_sign_provider_should_return_false(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider = factory.get_provider(SignType.ED25519)

        private_key = Ed25519PrivateKey.generate()

        private_key_bytes = private_key.private_bytes(encoding=serialization.Encoding.Raw,
                                                      format=serialization.PrivateFormat.Raw,
                                                      encryption_algorithm=serialization.NoEncryption()
                                                      )

        wrong_public_key_bytes = Ed25519PrivateKey.generate().public_key().public_bytes(encoding=serialization.Encoding.Raw,
                                                                                        format=serialization.PublicFormat.Raw
                                                                                        )
        test_string = "Signing test string"
        signed_test_string = sign_provider.sign(key=private_key_bytes, content=bytes(test_string, "utf-8"))
        verification_status = sign_provider.verify(key=wrong_public_key_bytes, content=bytes(test_string, "utf-8"), 
                                                   signed=bytes.fromhex(signed_test_string))

        self.assertEqual(verification_status, False)

    def test_ed25519_sign_provider_with_loaded_key_should_return_true(self):
        factory = SignProviderFactory()
        sign_provider: SignProvider = factory.get_provider(SignType.ED25519)

        with open(f"./tests/sign/keys/public.key", "r") as key_file:
            public_key_hex = key_file.read()
            public_key_bytes = bytes.fromhex( public_key_hex )

        with open(f"./tests/sign/keys/private.key", "r") as key_file:
            private_key_hex = key_file.read()
            private_key_bytes = bytes.fromhex( private_key_hex )

        test_string = "Signing test string"
        signed_test_string = sign_provider.sign(key=private_key_bytes, content=bytes(test_string, "utf-8"))
        verification_status = sign_provider.verify(key=public_key_bytes, content=bytes(test_string, "utf-8"), 
                                                   signed=bytes.fromhex(signed_test_string))

        self.assertEqual(verification_status, True)


if __name__ == "__main__":
    unittest.main()
