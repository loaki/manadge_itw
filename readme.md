
#### Installation

create virtualenv
install required python packages
start docker-compose
mongodb on port 27017
mongo-express on port 8081

`source start.sh`

#### Run Schedule

run schedule every day at 10am
get 100 first societies with NAF code 62.01Z using Sirene API
insert into mongodb

`python sirene.py`

#### Mongo-express

visualise data in datatable `database` 

`http://localhost:8081/`