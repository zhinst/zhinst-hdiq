[![PyPI](https://img.shields.io/pypi/v/zhinst-hdiq.svg)](https://pypi.python.org/pypi/zhinst-hdiq)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Zurich Instruments HDIQ (`zhinst-hdiq`)

`zhinst-hdiq` is a package for Python 3.7+ to control a [Zurich Instruments HDIQ IQ Modulator](https://www.zhinst.com/products/hdiq-iq-modulator) via Ethernet connection. Please note that this package is valid only for instruments with serial numbers **14100 and above**.

## Status
The `zhinst-hdiq` package is considered stable for general usage. The interface may be subject to incompatible changes between releases, which we will indicate by a change of the major version. Please check the [changelog](#changelog) if you are upgrading.

## Install
Install the package with [`pip`](https://packaging.python.org/tutorials/installing-packages/):

```sh
$ pip install zhinst-hdiq
```

## Example
The example below shows how to connect an HDIQ instrument to a host computer and control operation modes of the HDIQ channels.

```python
import zhinst.hdiq.utils
from zhinst.hdiq import Hdiq

hdiq_devices = zhinst.hdiq.utils.discover_devices()
print(f'Found devices: {hdiq_devices}')
hdiq_serial, hdiq_ip = hdiq_devices[0]
print(f'Connecting to {hdiq_serial} (IP: {hdiq_ip})')
hdiq = Hdiq(hdiq_ip)
channel = 1                               # HDIQ channel 1; HDIQ has 4 channels: 1, 2, 3, 4
hdiq.set_rf_to_calib(channel)             # calibration mode in channel 1, set RF to Calib. port
# hdiq.set_rf_to_exp(channel)             # RF mode in channel 1, set RF to Exp. port
# hdiq.set_lo_to_exp(channel)             # LO mode in channel 1, set LO to Exp. port
status = hdiq.get_channel_status(channel) # get status of channel 1
print(f'channel {channel} -> {status}')
```

## Changelog

**v1.0.0**: Initial public release
## Contributing
We welcome contributions by the community, either as bug reports, fixes and new code. Please use the GitHub issue tracker to report bugs or submit patches. Before developing something new, please get in contact with us.

## License
This software is licensed under the terms of the MIT license. See [LICENSE](./LICENSE) for more detail.
