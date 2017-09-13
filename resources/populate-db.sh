#!/usr/bin/env bash
set -euo pipefail

while getopts ":e:" opt; do
  case $opt in
    e) ENDPOINT="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

echo $ENDPOINT


