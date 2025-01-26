from eCommerceApp.helper_funcs import (
    validate_email,
    check_password_strength,
    check_email_pattern,
)


def test_email_pattern_validation():
    """
    Tests that the email regex pattern is matching valid e-mail patterns.
    """
    assert check_email_pattern("testemail1@gmail.com", True) is True
    assert check_email_pattern("testemail1@gmail", True) is False
    assert check_email_pattern("testemail1", True) is False
    assert check_email_pattern("test@email1", True) is False


def test_account_validation():
    """
    Tests that account exists in account repository based on e-mail value.
    """
    assert validate_email("testemail1@gmail.com", True) is True
    assert validate_email("testemail10@gmail.com", True) is False


def test_password_strength():
    """
    Tests if inputted passwords pass the necessary strength checks.
    """
    assert check_password_strength("SsDMoDuLe123!.", True) is True
    assert check_password_strength("SsDMoDuLe123#", True) is False
    assert check_password_strength("SsDMoDuLe", True) is False
    assert check_password_strength("Az.!12", True) is False
    assert check_password_strength("jfjhsjkhfjhgkdskfl", True) is False
    assert check_password_strength("Az.!12", False) is True
