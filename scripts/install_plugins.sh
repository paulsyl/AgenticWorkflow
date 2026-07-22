#!/bin/bash
# install_plugins.sh
# This script symlinks all plugins from this repository into your local AgenticWorkflow / Gemini config directory.

PLUGIN_DIR="$HOME/.gemini/config/plugins"
REPO_PLUGINS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../plugins" && pwd)"

# Ensure the local plugin directory exists
mkdir -p "$PLUGIN_DIR"

echo "Installing plugins to $PLUGIN_DIR..."

for plugin in "$REPO_PLUGINS_DIR"/*; do
  if [ -d "$plugin" ]; then
    plugin_name=$(basename "$plugin")
    target_link="$PLUGIN_DIR/$plugin_name"
    
    if [ -L "$target_link" ] || [ -e "$target_link" ]; then
      echo "Plugin '$plugin_name' already exists at $target_link. Skipping..."
    else
      ln -s "$plugin" "$target_link"
      echo "Successfully linked '$plugin_name'."
    fi
  fi
done

echo "Done!"
