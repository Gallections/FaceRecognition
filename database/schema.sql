CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE name (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(100),
    date_created TIMESTAMP default current_timestamp
);

CREATE TABLE encoding (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID DEFAULT uuid_generate_v4(),
    FOREIGN KEY (person_id) REFERENCES name(id) ON DELETE CASCADE,
    face_encoding JSONB,
    date_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID DEFAULT uuid_generate_v4(),
    FOREIGN KEY (person_id) REFERENCES name(id) ON DELETE CASCADE,
    image BYTEA,
    data_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)