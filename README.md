# SensUs

## TODO
- avoid crash during import PySpin -> Emile
- correct layers -> Katia
- rewrite `application/image_analysis` module -> Clara
- try high pass filter -> Clara
- write spots selection layer -> Vianney
- send capture in a subprocess -> Emile
- Test acquisition, livestream, video element, memory -> Raluca
- Application dual mode oscillation "capture" / "livestream" -> Emile
- Implement 12bits (10bits?) acquisition -> Emile
- (Optionnal) multiprocess capture
- (Optionnal) being able to set spots positions during acquisitionduring acquisitions

## Logging system
Log are both written in stdout (terminal) and in the local file `./log`. The local file has a higher verbosity and can be read live using `./read_log.sh` which simply use the command `tail -f log`.

## Dependencies
- python3
- pygame

