create table goals(
    id integer primary key,
    name varchar(255),
    options varchar(255)
);

create table progress(
    id integer primary key,
    date datetime,
    selected varchar(255),
    note varchar(255),
    goal_id integer,
    FOREIGN KEY(goal_id) REFERENCES goal(id)
);