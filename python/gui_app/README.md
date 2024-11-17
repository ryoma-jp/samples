# GUI App Samples

Sample code for GUI applications using Python.

## Preparation

BUild the docker image and run the container.

```
./build-image.sh
./enter-docker.sh
```

## [Clock](./clock)

A simple clock application.

```
cd ./clock
python clock.py
```

### Trouble Shooting

1. _tkinter.TclError: couldn't connect to display

Type `xhost +`.

```
xhost +
./enter-docker.sh
```

