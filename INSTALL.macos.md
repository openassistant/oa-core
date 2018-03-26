Prerequisite: homebrew (https://brew.sh)

# Basic System Dependencies

## Install Python3

`brew install python`

## Install Gstreamer

`brew install gst-python --with-python --without-python@2`
`brew install gst-plugins-good gst-plugins-bad gst-plugins-ugly`

# Python Modules

`pip3 install requests`

# Sphinx (Speech Recognition)

Build tools

`brew install autoconf libtool automake swig`

sphinxbase

`git clone https://github.com/cmusphinx/sphinxbase.git`
`./autogen.sh && make install`

pocketsphinx

`git clone https://github.com/cmusphinx/pocketsphinx.git`
`./autogen.sh && make install`
