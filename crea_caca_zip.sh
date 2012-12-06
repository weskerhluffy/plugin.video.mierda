#!/bin/sh

echo "caca"
#pyobfuscate crap.py 
#python3.3 -m mnfy  crap1.py > crap2.py
#python3.3 -m mnfy --function-to-lambda crap.py > crap1.py
cd ..
rm -rfv /tmp/plugin.video.crapvideo* 
cp -rfv plugin.video.crapvideo /tmp/
cd /tmp/plugin.video.crapvideo/
echo "ofuscando CACA"
pyobfuscate crap.py 2>&1 > crap1.py
mv crap1.py crap.py
rm -rfv .[A-Za-z0-9]*
rm -fv *.sh
rm -fv *.pyc
cd ..
zip -r plugin.video.crapvideo.zip plugin.video.crapvideo
rm -rfv  $HOME/Downloads/plugin.video.crapvideo*
mv -fv plugin.video.crapvideo.zip $HOME/Downloads/
rm -rfv plugin.video.crapvideo*
echo "#### el resultado"
zipinfo $HOME/Downloads/plugin.video.crapvideo.zip
