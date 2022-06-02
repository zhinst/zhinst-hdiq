#!/bin/bash
wheelPath=$(find dist -type f -name \*.whl)
pip install --upgrade --force-reinstall $wheelPath
python3 -c "
import zhinst.hdiq;
"
