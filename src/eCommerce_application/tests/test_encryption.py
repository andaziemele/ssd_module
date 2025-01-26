from eCommerceApp.helper_funcs import get_secret_key
from cryptography.fernet import Fernet
import bcrypt
import pytest


# fixtures initialise necessary values where multiple tests require them
@pytest.fixture
def fernet_key():
    return get_secret_key("test_data_encryption_key", debug=True)


@pytest.fixture
def cipher_suite(fernet_key):
    return Fernet(fernet_key)


def test_encryption_decryption(cipher_suite):
    """
    Tests encryption and decryption is working as anticipated.
    :param cipher_suite: cryptography's cipher suite to implement Fernet
    """
    # Test data
    original_message = "Anda Ziemele"

    # Encrypt the message
    encrypted_message = cipher_suite.encrypt(original_message.encode())

    # Decrypt the message
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()

    # Verify the decrypted message matches the original
    assert decrypted_message == original_message


def test_encryption_produces_different_output(cipher_suite):
    """

    :param cipher_suite: cryptography's cipher suite to implement Fernet
    :return:
    """
    message = "SSD Module"

    # encrypt the same message twice
    encrypted_message1 = cipher_suite.encrypt(message.encode())
    encrypted_message2 = cipher_suite.encrypt(message.encode())

    # verify that each encryption produces different output
    assert encrypted_message1 != encrypted_message2


def test_password_hashing():
    # Convert password to bytes
    password_bytes = "StRonGPaSsWord!2@".encode("utf-8")

    # Generate hash
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Verify the hash is not the original password
    assert hashed != password_bytes

    # Verify password matches hash
    assert bcrypt.checkpw(password_bytes, hashed)


def test_wrong_password_fails():
    correct_password = "ThIsIsCorRecT123!"
    # create hash of correct password
    correct_hash = bcrypt.hashpw(correct_password.encode("utf-8"), bcrypt.gensalt())

    # Try to verify with wrong password
    input_password = "admin123"
    result = bcrypt.checkpw(input_password.encode("utf-8"), correct_hash)

    assert result is False
