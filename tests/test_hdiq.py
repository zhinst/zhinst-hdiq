from zhinst.hdiq import utils
from zhinst.hdiq.hdiq import Hdiq

HDIQ_IP = "10.42.2.87"
HDIQ_PORT = 4242


def test__get_local_ip():
    actual_ip = utils._get_local_ip(HDIQ_IP, HDIQ_PORT)
    local_ip_list = utils._get_ip_list()
    assert actual_ip in local_ip_list
    assert actual_ip.startswith(HDIQ_IP.split(".")[0])


def test_set_lo_to_exp():
    controller = Hdiq(HDIQ_IP, HDIQ_PORT)
    sent = controller.set_lo_to_exp(1)
    assert sent


def test_set_rf_to_calib():
    controller = Hdiq(HDIQ_IP, HDIQ_PORT)
    sent = controller.set_rf_to_calib(1)
    assert sent


def test_set_rf_to_exp():
    controller = Hdiq(HDIQ_IP, HDIQ_PORT)
    sent = controller.set_rf_to_exp(1)
    assert sent


def test_get_channel_status():
    controller = Hdiq(HDIQ_IP, HDIQ_PORT)
    result = controller.get_channel_status(1)
    assert result in ("1", "2", "3")


def test_device_discovery():
    actual_devices = utils.discover_devices()
    print(actual_devices)
    assert len(actual_devices) > 0
