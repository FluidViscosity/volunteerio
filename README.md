# volunteerio

## Run
To run this software run the `src/volunteerio/run.py` file

## TODOS
- create a db schema for user store, park activities, activity store
- make sure username is unique
- fetch results from db
- create a calendar view that can be moved along a calendar 

## DB Schema
### Volunteers
id serial primary key,
Name, text not null,
email address, text??

### Park activities
id serial primary key,
activity, text, not null,

### Activity store
id serial primary key,
volunteer_id, int,
activity_id, int,
date, date,
hours, double

volunteer_id references volunteers.id foreign key
activity_id references park_activities.id foreign key