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
## EC2 Deployment:
### Launch Instance
- Allow SSH from specific IP addresses only, HTTP, HTTPS
- enable ipv4 autoassign (to be removed later)

### Installation of Deputy
- `sudo apt install`
- `sudo apt update`

#### Install Python version:
Depending on distro version you might need to install Python 3.11
- Add the Deadsnakes third party repo
- `sudo add-apt-repository ppa:deadsnakes/ppa`
- `sudo apt install python3.11`
- Python will now be available via python3.11. e.g. `python3.11 --version`

#### Install PDM
- `curl -sSL https://pdm-project.org/install-pdm.py | python3.11 -`
- `export PATH=/home/ubuntu/.local/bin:$PATH`

#### Clone repo
Create ssh key
- `ssh-keygen -t ed25519 -C "tomer.simhony@proton.me"`
Start ssh-agent in the background, and add the SSH private key to the ssh agent.
- `eval "$(ssh-agent -s)"`
- `ssh-add ~/.ssh/id_ed25519`
Add the SSH public key to the github account
- `cat ~/.ssh/id_ed25519.pub`
- Copy and paste that into the SSH keys settings of Github
- `mkdir ev_metrix`
- `cd ev_metrix`
- `git clone git@github.com:FluidViscosity/volunteerio.git`
- 
### Setup python environment
- `pdm install`


#### Server
**Install nginx (our reverse proxy) with:**
`sudo apt update`
`sudo apt install nginx`

**Install certbot**
`sudo snap install --classic certbot`
`sudo ln -s /snap/bin/certbot /usr/bin/certbot`