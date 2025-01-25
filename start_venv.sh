# Create virtual invieronment 
python3 -m venv .venv

# Activate virtual invieronment 
source ./.venv/bin/activate

# Pull all need libraries
pip freeze > requirements.txt

# If requirements.txt is empty use command "deactivate" to deactivate virtual invienronment
deactivate

# Copу all need libraries from global_requirements
pip freeze > global_requirements.txt  

# Activate virtual invieronment 
source ./.venv/bin/activate

# Install libraries from global_requirements.txt  
pip install -r global_requirements.txt