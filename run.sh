#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 7 ]; then
    echo "Usage: $0 app_idea app_name app_config dev_type dev_backlog clean_cache chat"
    exit 1
fi

# Assign arguments to variables
IDEA=$1
NAME=$2
CONFIG=$3
DEV_TYPE=$4
BACKLOG=$5
REQUIREMENTS=$6
DESIGN=$7


# Directory to be cleaned
CACHE_DIR=".cache"
WORKSPACE_DIR="workspace"

# Clean up cache and workspace directories if required
if [ "$CLEANUP" = "yes" ]; then
    # Check if the CACHE_DIR exists
    if [ -d "$CACHE_DIR" ]; then
        # Remove all files in the CACHE_DIR
        rm -f "$CACHE_DIR"/*
        echo "All files in $CACHE_DIR have been removed."
    else
        echo "Directory $CACHE_DIR does not exist."
    fi

    # Check if the WORKSPACE_DIR exists
    if [ -d "$WORKSPACE_DIR" ]; then
        # Remove all files in the WORKSPACE_DIR
        rm -f "$WORKSPACE_DIR"/*
        echo "All files in $WORKSPACE_DIR have been removed."
    else
        echo "Directory $WORKSPACE_DIR does not exist."
    fi
fi

if [ "$CHAT" = "yes" ]; then
    chainlit run appgenpro_chat.py 
else
    # Execute different commands based on the value of DEV_TYPE
    if [ "$DEV_TYPE" = "full" ]; then
        python appgenpro_cli.py --idea "$IDEA" --name "$NAME" --config "$CONFIG"
    elif [ "$DEV_TYPE" = "design" ]; then
        python appgenpro_cli.py --idea "$IDEA" --name "$NAME" --config "$CONFIG"
    # DEV_TYPE = 2 for implementation only
    elif [ "$DEV_TYPE" = "implement" ]; then
        python appgenpro_cli.py --idea "$IDEA" --name "$NAME" --config "$CONFIG" --backlog "$BACKLOG" --requirements "$REQUIREMENTS" --design "$DESIGN"
    else
        echo "Invalid development type specified."
        exit 1
    fi
fi