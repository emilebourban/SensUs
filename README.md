# SensUs

## TODO
- script pour tourner interface sans bureau
- release folder of measures
- rewrite `application/image_analysis` module -> Raluca
- try high pass filter -> Clara
- (Optionnal) Create disable mode for buttons (becoming grayish)
- (Optionnal) multiprocess capture
- (Optionnal) being able to set spots positions during acquisitionduring acquisitions

## Logging system
Log are both written in stdout (terminal) and in the local file `./log`. The local file has a higher verbosity and can be read live using `./read_log.sh` which simply use the command `tail -f log`.

## Dependencies
- python3
- pygame

