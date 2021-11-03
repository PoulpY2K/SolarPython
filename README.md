# SolarPython

## Start the project

### 1. With [Make](https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=freefr&download= "Make installer for Windows")

To start the project, you just have to use ``make run`` in your terminal.
This command will setup the project environment by installing the required dependencies, and then it will start the SolarPython simulator.


### 2. Manual setup and run

If Make is not installed on your computer (which is totally fine), you need to manually setup the environment by install the dependencies. But no worries, one file in the **libs** folder will do it for you.

All you have to do is run ``pip install -r libs\dependencies.txt``
(or ``pip install -r dependencies.txt`` if you already are in the **libs** folder)

Then, to start the project, simply run ``python solar_system.py`` in a terminal.

## I get an error from astropy on setup

Adding `astropy` requires having the Visual C++ Build Tools, which is kind of unconvenient because you have to go through a long installation process.

But there's a ay to do it without all this process, which is using one of the wheel files available in the **libs** folder, or at this [link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#astropy) if you python version is not present.

Then, once you have the wheel file, just do ``pip install astropy-4.3.1-cpxx-cpxx-win_amd64.whl`` and then launch the start process again.

For Linux users, you probably won't face this problem at all, so you're also probably not reading this 🤡