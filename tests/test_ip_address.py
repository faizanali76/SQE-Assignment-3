import pytest
from validators import ipv4, ipv6


@pytest.mark.ip
class TestIPAddress:
    @pytest.mark.order(3)
    def test_ipv4(self, case, check_validation):
        check_validation(ipv4, case)

    @pytest.mark.order(4)
    def test_ipv6(self, case, check_validation):
        check_validation(ipv6, case)
