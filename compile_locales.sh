#!/bin/bash
# shellcheck disable=SC2044
for file in $(find ./src/arpasswords/locales/ru/LC_MESSAGES -name "*.po"); do
    msgfmt -o "${file%.po}.mo" "$file"
done
for file in $(find ./src/arpasswords/locales/en/LC_MESSAGES -name "*.po"); do
    msgfmt -o "${file%.po}.mo" "$file"
done
