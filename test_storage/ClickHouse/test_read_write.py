import time
import datetime
import random
from clickhouse_driver import Client
from tqdm import tqdm

# Connect to ClickHouse server
client = Client('localhost')

# Create the test table if it doesn't exist
# create_table_query = '''
    # CREATE TABLE IF NOT EXISTS user_progress (
        # user_id Int32,
        # movie_id Int32,
        # progress Float64,
        # timestamp DateTime
    # ) ENGINE = MergeTree()
    # PARTITION BY toYYYYMMDD(timestamp)
    # ORDER BY (user_id, movie_id, timestamp)
# '''
# client.execute(create_table_query)

# Function to insert random data into the table
def insert_data(total_rows):
    insert_query = 'INSERT INTO user_progress (user_id, movie_id, progress, timestamp) VALUES'
    data = [(random.randint(1, 100), random.randint(1, 100), random.random(), datetime.datetime.now()) for _ in tqdm(range(total_rows), desc='Inserting', unit='row')]
    client.execute(insert_query, data)

# Function to read all data from the table
def read_data():
    select_query = 'SELECT user_id, movie_id, progress FROM user_progress WHERE user_id = 1'
    result = client.execute(select_query)
    return result

# Measure the write velocity
# start_time = time.time()
# insert_data(100000)
# end_time = time.time()
# write_velocity = 100000 / (end_time - start_time)
# print(f'Write Velocity: {write_velocity:.2f} rows/s')

# Measure the read velocity
start_time = time.time()
result = read_data()
end_time = time.time()
read_velocity = len(result) / (end_time - start_time)
print(f'Read Velocity: {read_velocity:.2f} rows/s')
print(f'Total time: {(end_time - start_time):.2f} s')

# Close the connection
client.disconnect()

