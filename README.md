# volunteerio

## Run
To run this software run the `src/volunteerio/run.py` file

## TODOS
Delete names?
make adding names guarded by a 'rangers only' paragraph
export: sort by name and by activity
Show some basic stats on admin page. 


## DB Schema
### Volunteers
Create table volunteers (
	id serial primary key,
	name text not null,
	email text not null
)

### Park activities
create table activities (
	id serial primary key,
	activity, text, not null,
)

### Activity store
create table activity_store (
	id serial primary key,
	volunteer_id, int,
	activity_id, int,
	date, date,
	hours, double

	foreign key volunteer_id references volunteers(id)
	foreign key activity_id references activities(id) 
)
