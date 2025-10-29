#!/bin/bash

DOWNLOADS_DIR="downloads"

DOWNLOADS=$(ls -td -- $DOWNLOADS_DIR/*/ | head -n 1) 
cd /Users/westondcrewe/Desktop
cp youtube_audio_scraper/downloads/$DOWNLOADS* songs\ for\ sets/