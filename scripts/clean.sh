#!/bin/bash

set -e

rm -rf project/__pycache__
rm -rf project/pages/__pycache__
rm -rf project/build
rm -rf project/.webassets-cache
rm -rf project/static/.webassets-cache
rm -rf project/static/css/styles.css

echo "Project Cleanup Complete"
