#!/bin/bash
wget -O go.sh https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh
version=$1
file_name="v2ray-${version}.zip"

wget -O ${file_name} "https://github.com/v2fly/v2ray-core/releases/download/${version}/v2ray-linux-arm32-v7a.zip"
chmod +x go.sh
printf 'y' | ./go.sh --local ${file_name}

rm go.sh
rm ${file_name}