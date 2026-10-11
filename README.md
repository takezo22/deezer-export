# DEEZER EXPORT SCRIPT

## Description
You currently can't use an API to save your loved songs because they're not registered in a playlist. So I made this script to get the list of songs/authors in all your playlists.

## Requirements
Python > 3.12, selenium

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