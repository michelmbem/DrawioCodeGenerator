#!/bin/bash
apt -y install build-essential python3-dev python3-tk libwebkitgtk-6.0-dev libtiff-dev \
    libnotify-dev freeglut3-dev libsdl2-dev libgstreamer-plugins-base1.0-dev python3-lib2to3

# Alternatively you could simply install python3-wxgtk4.0 and python3-tk
# python3-tk is only needed for auto-py-to-exe to work
