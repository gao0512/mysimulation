#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/gao/mysimulation/src/arbotix_ros/arbotix_python"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/gao/mysimulation/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/gao/mysimulation/install/lib/python3/dist-packages:/home/gao/mysimulation/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/gao/mysimulation/build" \
    "/usr/bin/python3" \
    "/home/gao/mysimulation/src/arbotix_ros/arbotix_python/setup.py" \
    egg_info --egg-base /home/gao/mysimulation/build/arbotix_ros/arbotix_python \
    build --build-base "/home/gao/mysimulation/build/arbotix_ros/arbotix_python" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/gao/mysimulation/install" --install-scripts="/home/gao/mysimulation/install/bin"
