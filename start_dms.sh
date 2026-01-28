#!/bin/bash
# DMS (Data Maintenance Service) Startup Script
# DMS is an independent project, no dependency on sai directory

cd "$(dirname "$0")"

# Add current directory to PYTHONPATH for relative imports
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Activate conda environment
if [ -f ~/anaconda3/etc/profile.d/conda.sh ]; then
    source ~/anaconda3/etc/profile.d/conda.sh
    conda activate trade311
elif [ -f ~/miniconda3/etc/profile.d/conda.sh ]; then
    source ~/miniconda3/etc/profile.d/conda.sh
    conda activate trade311
else
    echo "Warning: conda not found, trying to run Python directly"
fi

echo "Starting DMS (Data Maintenance Service)..."
echo "Access URL: http://localhost:11183"
echo "Web Interface: http://localhost:11183"
echo "API Docs: http://localhost:11183/docs"
echo ""

# Start DMS service
python app.py
