import pytest
from validators import length


@pytest.mark.length
@pytest.mark.order(2)
class TestLength:
    def test_length(self, case, check_validation):
        check_validation(length, case)
