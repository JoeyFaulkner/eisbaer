# eisbaer ❄️🐻
data modelling for nhl.com ice hockey data for visualization + data science

## Motivation
NHL.com provides a generous amount of data via API endpoints regarding games, plays in those games, players making those plays, amongst other things.
Eisbaer exists to make it easier to scrape this data from the site, and represent it locally in a postgres db, to make more complex queries available,
with the endgoal being visualization and data science on top of it.

## Current status
The first stage of modelling the data we get from the game feed endpoint works correctly, but currently only models shot and faceoff plays.
PostGIS support is implemented which means it is possible to query for plays by their position on the court. The coordinates of the court are 
from (-100, -42) to (100, 42), which corresponds roughly to the official NHL hockey rink size of 85ft by 200ft, with the centre ice faceoff spot at (0,0). 

## See also
https://gitlab.com/dword4/nhlapi - project to document the nhl.com api which was used in the development of this library.
