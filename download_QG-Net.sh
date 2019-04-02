#!/bin/bash
# Configure download location
DOWNLOAD_PATH="$1/test/testinput"
mkdir -p $DOWNLOAD_PATH

# Download the test files
mkdir "$1"/data/
cd "$1"/data/
wget -v -O test.tar.gz -L https://rice.box.com/shared/static/o8hw9zyzm1391blwtm8lx6c38qu9shck.gz
tar -xvf test.tar.gz

# Download qg-net
cd $DOWNLOAD_PATH
wget -v -O QG-Net.pt -L https://rice.box.com/shared/static/izhz3hasup6ekgi8jwyokt70btdq5z3j.pt
mv $DOWNLOAD_PATH/*.pt $DOWNLOAD_PATH/QG-Net.pt

echo "download completed."
