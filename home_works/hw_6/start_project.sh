 docker compose up -d pg
 
 source ./.venv/bin/activate

 pip install -r requirements.txt
 
 alembic init alembic 

 alembic revision --autogenerate -m "Initial migration"