# DEEZER EXPORT SCRIPT

## Description
There is currently no API to export your loved songs because they're not registered in a proper playlist. So I made this script to get the list of songs/authors in your loved songs.\
You can also export the content of a playlist, get stats on them and compare playlists together to see if there are matching songs.

## Requirements
Python, selenium

## Installation and usage
Clone this repository, then install the dependencies :

```
pip install -e .
```
### How to use :
Get help :
```
deezer --help
```
Export loved songs :
```
deezer --loved
```
Export playlist (via Deezer API) :
```
deezer --playlist {playlist ID}
```
all exports are in separate folders, in data/ at the root of the project.