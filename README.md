# SensUs

## TODO
- correct layers
- rewrite `application/image_analysis` module
- write `class Video(Element)`
- write dot selection layer
- write acquisition module 
- (optionnal) generalize positionning system (not resolution dependent)

## Logging system
Log are both written in stdout (terminal) and in the local file `./Log`. The local file has a higher verbosity and can be read live using `./read_log.sh` which simply use the command `tail -f log`.

## Dependencies
- python3
- pygame

