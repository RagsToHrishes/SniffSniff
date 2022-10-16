# getClasses

Script to get classes for current semester.

## Connect to CockroachDB
```
# Only need to run once.
curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/c3a09338-fdb8-4ade-9b65-a8f817b01404/cert

# add DATABASE_URL to .env file
# install SQLAlchemy and sqlalchemy-cockroachdb and psycopg2-binary
pip3 install SQLAlchemy
pip3 install sqlalchemy-cockroachdb
pip3 install psycopg2-binary
```