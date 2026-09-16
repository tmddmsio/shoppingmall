from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    conninfo="postgresql://neondb_owner:npg_CcUAdQE3lWV8@ep-solitary-mud-aydlwbwy-pooler.c-5.us-east-2.aws.neon.tech/neondb?channel_binding=require&sslmode=require",
    min_size=1,
    max_size=10,
)


def get_db():
    return pool.connection()