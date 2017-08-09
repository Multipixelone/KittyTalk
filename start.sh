#!/bin/sh

# Start Flash Server (Debug for Now...)

echo "KittyTalk by Multipixelone!"
export FLASK_APP=KittyTalk.py
python -m flask run --host=0.0.0.0 --port=80
