#!/bin/sh
# Create a folder for a new animation and copy a prompt template into it.
# Usage: ./new-animation.sh "Frog Buys Groceries"           ->  animations/frog-buys-groceries/prompt.txt (from prompt.txt)
#        ./new-animation.sh --scion "Frog Buys Groceries"   ->  the same, from prompt-scion.txt

set -e
cd "$(dirname "$0")"

template=prompt.txt
if [ "$1" = "--scion" ]; then
  template=prompt-scion.txt
  shift
fi

if [ -z "$1" ]; then
  echo "Usage: ./new-animation.sh [--scion] \"name of the animation\""
  exit 1
fi

# Lowercase, spaces and underscores to hyphens, drop anything else unsafe in a URL.
slug=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr ' _' '--' | tr -cd 'a-z0-9-' | tr -s '-' | sed 's/^-//; s/-$//')

if [ -z "$slug" ]; then
  echo "That name has no usable letters or numbers."
  exit 1
fi

dir="animations/$slug"
if [ -e "$dir" ]; then
  echo "$dir already exists. Pick another name."
  exit 1
fi

mkdir -p "$dir"
cp "$template" "$dir/prompt.txt"

echo "Created $dir/prompt.txt (from $template)"
if [ "$template" = prompt-scion.txt ]; then
  echo "Next: fill in the bracketed blanks near the top of that file ([WORK], [DIRECTION AND REFERENCES],"
  echo "[FORMAT, DURATION, ASPECT RATIO], [AVAILABLE RESOURCES]),"
else
  echo "Next: fill in the blanks at the end of that file (subject, style, length, aspect ratio),"
fi
echo "then ask Claude to \"make the animation in $slug\"."
