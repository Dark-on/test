create table goals(
    name varchar(255) primary key,
);

create table progress(
    id integer primary key,
    date datetime,
    selected varchar(255),
    raw_text text,
    goal_name integer,
    FOREIGN KEY(goal_name) REFERENCES goal(name)
);