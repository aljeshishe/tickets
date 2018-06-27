conda env create -f requirements.yaml
call activate db_template

python db.py create
python db.py alembic revision --autogenerate -m "comment"
python db.py alembic upgrade head
python db.py test
python db.py drop

call deactivate db_template
conda remove -n db_template --all -y