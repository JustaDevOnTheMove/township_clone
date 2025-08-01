#!/bin/bash

export BUILD_ENV="development"

set -e


rm -rf project/.webassets-cache
rm -rf project/static/.webassets-cache

python3 app.py
