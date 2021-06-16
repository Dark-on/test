create table if not exists goals(
    id integer primary key,
    name varchar(255),
    options varchar(255)
);

create table if not exists progress(
    id integer primary key,
    date datetime,
    selected varchar(255),
    note varchar(255),
    goal_id integer,
    FOREIGN KEY(goal_id) REFERENCES goal(id)
);