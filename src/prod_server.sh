#!/bin/sh

gunicorn microweb.app:app --timeout 6000 --bind 0.0.0.0:5000
