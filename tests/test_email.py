import pytest
from validators import email


@pytest.mark.email
@pytest.mark.order(1)
class TestEmail:
    def test_email(self, case, check_validation):
        check_validation(email, case)
