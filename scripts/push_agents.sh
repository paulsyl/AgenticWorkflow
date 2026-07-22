#!/bin/bash

# push_agents.sh
# This script pushes global agents/plugins from the AgenticWorkflow repo to the .agents directory of all other projects.

SOURCE_PLUGINS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../plugins" && pwd)"
PROJECTS_DIR="$HOME/projects"
IGNORE_DIR="AgenticWorkspace"

MODE="symlink"

if [[ "$1" == "--copy" ]]; then
  MODE="copy"
fi

echo "Pushing agents ($MODE mode) from $SOURCE_PLUGINS_DIR to projects in $PROJECTS_DIR..."

for proj_path in "$PROJECTS_DIR"/*; do
  if [ -d "$proj_path" ]; then
    proj_name=$(basename "$proj_path")
    
    # Skip non-project directories
    if [[ "$proj_name" == "$IGNORE_DIR" ]] || [[ "$proj_name" == .* ]]; then
      continue
    fi

    echo "Processing project: $proj_name"
    TARGET_AGENTS_DIR="$proj_path/.agents/plugins"
    mkdir -p "$TARGET_AGENTS_DIR"

    for plugin in "$SOURCE_PLUGINS_DIR"/*; do
      if [ -d "$plugin" ]; then
        plugin_name=$(basename "$plugin")
        target_dest="$TARGET_AGENTS_DIR/$plugin_name"

        # Remove existing if it exists
        if [ -L "$target_dest" ] || [ -e "$target_dest" ]; then
          rm -rf "$target_dest"
        fi
        
        if [[ "$MODE" == "copy" ]]; then
          cp -r "$plugin" "$target_dest"
          echo "  -> Copied '$plugin_name' to $proj_name"
        else
          ln -s "$plugin" "$target_dest"
          echo "  -> Symlinked '$plugin_name' to $proj_name"
        fi
      fi
    done
  fi
done

echo "Done!"
