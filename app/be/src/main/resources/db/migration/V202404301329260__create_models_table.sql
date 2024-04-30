create table if not exists models (
    id uuid primary key default uuid_generate_v4(),
    model_info jsonb not null,
    model_as_ddl varchar default '',
    task_id uuid not null unique references tasks(id)
);