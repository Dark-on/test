create table if not exists goals(
    id integer primary key unique,
    name varchar(255) unique,
    type varchar(255),
    options varchar(255)
);

create table if not exists progress(
    id integer primary key unique,
    date datetime,
    choice varchar(255),
    notes varchar(255),
    goal_id integer,
    FOREIGN KEY(goal_id) REFERENCES goal(id)
);