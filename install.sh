python3 -m venv .venv
current_dir=$(pwd)
echo $current_dir

cd "$current_dir/.venv/bin"
source activate
cd .. && cd ..

if command -v pip3 > /dev/null 2>&1; then
    echo "Using pip3 to install requirements..."
    pip3 install -r requirements.txt
elif command -v pip > /dev/null 2>&1; then
    echo "Using pip to install requirements..."
    pip install -r requirements.txt
else
    echo "Error: Neither pip nor pip3 found. Please install Python and pip."
    exit 1
fi
