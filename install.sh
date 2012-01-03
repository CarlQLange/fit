#!/bin/bash
#install.sh

#this will still only work on systems with python3 installed
#and listen will only work on systems with sox installed

echo ""
mkdir ~/bin
mkdir ~/bin/_fit
cp -v -R ./_fit/* ~/bin/_fit
cp -v ./fitunes.py ~/bin/fit
chmod a+x ~/bin/fit

if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
	echo "Adding ~/bin to your PATH"
	echo "export PATH=${PATH}:$HOME/bin" >> ~/.profile
	export PATH=${PATH}:$HOME/bin
fi

echo ""
echo "Done! Type \"fit 'play a song you like'\" to get started!"