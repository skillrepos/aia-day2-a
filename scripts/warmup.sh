#!/bin/bash

# Model warmup script wrapper
# This script ensures the Python environment is activated and runs the warmup

echo "Starting AI Agent Model Warmup..."

# Get the project root directory
PROJECT_ROOT="$(dirname "$(dirname "$0")")"

# Check if virtual environment exists, if not create it
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Creating virtual environment..."
    cd "$PROJECT_ROOT"
    python3 -m venv venv
    source venv/bin/activate
    pip install ollama langchain-ollama openai requests litellm smolagents
    cd - > /dev/null
else
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Run the warmup script
python3 "$(dirname "$0")"/warmup_model.py --max-per-model 3

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "Model warmup completed successfully!"
else
    echo "Model warmup completed with some issues. Agents should still work."
fi

exit $exit_code

