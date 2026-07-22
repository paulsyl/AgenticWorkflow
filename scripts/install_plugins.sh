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
      read -p "Plugin '$plugin_name' already exists. Do you want to update/overwrite it? (y/N) " -n 1 -r
      echo
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$target_link"
        ln -s "$plugin" "$target_link"
        echo "Successfully updated '$plugin_name'."
      else
        echo "Skipping '$plugin_name'..."
      fi
    else
      ln -s "$plugin" "$target_link"
      echo "Successfully linked '$plugin_name'."
    fi
  fi
done

echo "Done!"
