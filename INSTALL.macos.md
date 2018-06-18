Prerequisite: homebrew (https://brew.sh)

# Basic System Dependencies

## Install Python3

`brew install python`

# Python Modules

`pip3 install requests`

# Open Assistant Modules

## Speech Recognition

### gstreamer

note the options: python3 support, no python2

`brew install gst-python --with-python --without-python@2`

support for autoaudiosrc

`brew install gst-plugins-good`

### sphinx

Build tools

`brew install autoconf libtool automake swig`

sphinxbase

`git clone https://github.com/cmusphinx/sphinxbase.git`
`./autogen.sh && make install`

pocketsphinx

`git clone https://github.com/cmusphinx/pocketsphinx.git`
`./autogen.sh && make install`
