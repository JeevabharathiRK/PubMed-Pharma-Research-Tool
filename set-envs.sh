# set-envs.sh
# This script sets environment variables for the PubMed Pharma Research Tool.

#!/bin/bash

# Set the Poetry cache directory to a local .poetry-cache folder
# This helps in managing dependencies without polluting the global cache
# and allows for easier cleanup.
export POETRY_CACHE_DIR="$PWD/.poetry-cache"

#Paste your GroqCloud API key below
# Go to https://console.groq.com/keys to get your API key
# You can also set this in your environment variables as GROQ_API_KEY
export GROQ_API_KEY="YOUR_GROQ_API_KEY_HERE"
