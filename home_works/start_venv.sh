# Create virtual invieronment 
python3 -m venv .venv

# Activate virtual invieronment 
source ./.venv/bin/activate

# Pull all need libraries in requirements.txt file
pip freeze > requirements.txt

# If requirements.txt is empty use command "deactivate" to deactivate virtual invienronment
deactivate

# Install libraries from global_requirements.txt  
pip install -r requirements.txt