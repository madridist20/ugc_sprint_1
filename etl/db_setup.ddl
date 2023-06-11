-- FOR node1
-- docker exec -it clickhouse-node1 bash
-- clickhouse-client

CREATE DATABASE shard;
CREATE DATABASE replica;

CREATE TABLE shard.movie_events (id UUID DEFAULT generateUUIDv4(), userId String, movieId String, event_ts Int64, inserted_at DateTime DEFAULT now()) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/movie_events', 'replica_1') PARTITION BY toYYYYMMDD(inserted_at) ORDER BY id;
CREATE TABLE replica.movie_events (id UUID DEFAULT generateUUIDv4(), userId String, movieId String, event_ts Int64, inserted_at DateTime DEFAULT now()) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movie_events', 'replica_2') PARTITION BY toYYYYMMDD(inserted_at) ORDER BY id;
CREATE TABLE default.movie_events (id UUID DEFAULT generateUUIDv4(), userId String, movieId String, event_ts Int64, inserted_at DateTime DEFAULT now()) ENGINE = Distributed('company_cluster', '', movie_events, rand());


-- FOR node3
-- docker exec -it clickhouse-node3 bash
-- clickhouse-client

CREATE DATABASE shard;
CREATE DATABASE replica;

CREATE TABLE shard.movie_events (id UUID DEFAULT generateUUIDv4(), userId String, movieId String, event_ts Int64, inserted_at DateTime DEFAULT now()) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/movie_events', 'replica_1') PARTITION BY toYYYYMMDD(inserted_at) ORDER BY id;
CREATE TABLE replica.movie_events (id UUID DEFAULT generateUUIDv4(), userId String, movieId String, event_ts Int64, inserted_at DateTime DEFAULT now()) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/movie_events', 'replica_2') PARTITION BY toYYYYMMDD(inserted_at) ORDER BY id;
CREATE TABLE default.movie_events (id UUID DEFAULT generateUUIDv4(), userId String, movieId String, event_ts Int64, inserted_at DateTime DEFAULT now()) ENGINE = Distributed('company_cluster', '', movie_events, rand());
