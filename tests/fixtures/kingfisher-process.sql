CREATE TABLE IF NOT EXISTS compiled_release (
    id bigserial PRIMARY KEY,
    ocid text NOT NULL,
    collection_id bigint NOT NULL,
    collection_file_id bigint NOT NULL,
    data_id bigint NOT NULL,
    release_date text NOT NULL
);

INSERT INTO compiled_release VALUES (1, 'ocds-213czf-1', 123, 1, 1, '2000-01-01T00:00:00Z');
