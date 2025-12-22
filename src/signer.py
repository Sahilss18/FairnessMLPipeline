# src/signer.py
"""
Signer utility for RSA-based digital signatures.
Used by audit_logger.py to sign each audit entry.
"""

import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class Signer:
    KEY_PATH = "models/private_key.pem"
    PUB_PATH = "models/public_key.pem"

    def __init__(self, private_key=None, public_key=None):
        self.private_key = private_key
        self.public_key = public_key

    @classmethod
    def load_or_create(cls):
        os.makedirs("models", exist_ok=True)

        # Generate new RSA key pair if not found
        if not os.path.exists(cls.KEY_PATH):
            print("🔐 Generating new RSA key pair for audit signing...")
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            public_key = private_key.public_key()

            # Save keys
            with open(cls.KEY_PATH, "wb") as f:
                f.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )
            with open(cls.PUB_PATH, "wb") as f:
                f.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                )
        else:
            # Load existing keys
            with open(cls.KEY_PATH, "rb") as f:
                private_key = serialization.load_pem_private_key(f.read(), password=None)
            with open(cls.PUB_PATH, "rb") as f:
                public_key = serialization.load_pem_public_key(f.read())

        return cls(private_key, public_key)

    def sign(self, message: str) -> str:
        """Return base64 signature of message."""
        signature = self.private_key.sign(
            message.encode("utf-8"),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return base64.b64encode(signature).decode("utf-8")

    def verify(self, message: str, signature_b64: str) -> bool:
        """Verify message with public key."""
        try:
            sig = base64.b64decode(signature_b64)
            self.public_key.verify(
                sig,
                message.encode("utf-8"),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False
