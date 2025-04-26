# volunteerio

## Run
To run this software run the `src/volunteerio/run.py` file

## TODOS
- DONE: create a db schema for user store, park activities, activity store
- DONE: make sure username is unique
- DONE: fetch results from db
- DONE: create a calendar view that can be moved along a calendar 
- create an export button,
- create tables if app is starting up for first time Create table if not exists (incl. constraints)
- deploy on raspberrypi
- show to rangers


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