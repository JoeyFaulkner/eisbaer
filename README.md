# eisbaer ❄️🐻
data modelling for nhl.com ice hockey data for visualization + data science, using python, sqlalchemy and plotly.

## Motivation
NHL.com provides a generous amount of data via API endpoints regarding games, plays in those games, players making those plays, amongst other things.
Eisbaer exists to make it easier to scrape this data from the site, and represent it locally in a postgres db, to make more complex queries available,
with the endgoal being visualization and data science on top of it.

## Current status
The first stage of modelling the data we get from the game feed endpoint works correctly, but currently only models shot and faceoff plays.
PostGIS support is implemented which means it is possible to query for plays by their position on the court. The coordinates of the court are 
from (-100, -42) to (100, 42), which corresponds roughly to the official NHL hockey rink size of 85ft by 200ft, with the centre ice faceoff spot at (0,0). 

## Usage
To populate a postgres db, firstly set POSTGRES_URI with the desired postgres instance, for example to populate a local running postgres server:
```bash
export POSTGRES_URI='postgres://localhost:5432'
```
ideally then create a local virtualenvironment (python3.6 or higher) and install dependencies using
```bash
virtualenv venv --python=python3.6
source venv/bin/activate
pip install -r requirements.txt
```

then create tables and populate them using

```bash
python eisbaer/data_population.py
```
(warning: this currently runs a sqlalchemy drop_all command, which will only drop tables in the models/ dir, but should be approached with caution :) )

Currently this should fill the tables with one game from 2019. More CLI options to choose how many games to fill are incoming.

## See also
https://gitlab.com/dword4/nhlapi - project to document the nhl.com api which was used in the development of this library.


## Get involved
If you're interested in contributing or see anything wrong, feel free to either post an issue or get in touch with me.
