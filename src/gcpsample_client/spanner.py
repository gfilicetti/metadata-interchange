from google.cloud import spanner

# Your Cloud Spanner instance ID.
instance_id = "oaio-test-1"

# Your Cloud Spanner database ID.
database_id = "oaio-db-1"

spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

# Execute a simple SQL statement.
with database.snapshot() as snapshot:
    results = snapshot.execute_sql("SELECT 1")

    for row in results:
        print(row)