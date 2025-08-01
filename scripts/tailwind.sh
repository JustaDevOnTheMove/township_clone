#!/bin/bash

set -e

tailwind -i ./project/static/tailwind/tailwind.css -o ./project/static/tailwind/generated.css --watch

# TODO: Test minify
# ./tailwindcss -i input.css -o output.css --minify
