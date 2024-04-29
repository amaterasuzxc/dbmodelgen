create table if not exists tasks (
    id uuid primary key default uuid_generate_v4(),
    title varchar(100) not null,
    text varchar not null,
    status varchar(20) not null
);