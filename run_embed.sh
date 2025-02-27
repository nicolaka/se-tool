
#!/bin/bash


ulimit -n 10240
if [ -d "env" ]; then
    echo "Directory 'env' already exists."
else 
    python3 -m venv env
fi
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.streamlit.txt
playwright install
python embed_hashicorp.py