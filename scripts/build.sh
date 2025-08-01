#!/bin/bash

export BUILD_ENV="${BUILD_ENV:-production}"

set -e

rm -rf project/build
rm -rf project/.webassets-cache
rm -rf project/static/.webassets-cache

python3 app.py build
