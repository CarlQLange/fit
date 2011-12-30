#!/bin/bash
#install.sh

echo ""
cp -v ./fitunes.py ./fit
echo "chmod a+x ./fit"
chmod a+x ./fit
cp -v ./fit ~/bin
echo "rm ./fit"
rm ./fit
echo ""
echo "You might have to add ~/bin to your \$PATH. Yep. Unless it's already there which it's not by default."
echo "Done! Type \"fit play 'a song you like'\" to get started!"