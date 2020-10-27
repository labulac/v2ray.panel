#!/usr/local/bin/bash

brew install wget curl python3
brew tap v2ray/v2ray
brew install v2ray-core
brew services start v2ray-core
pip3 install -r requirements.txt
mkdir -p ~/Library/Logs/v2ray-core/