# PiSpec20_stellarnet
A Python interface for StellarNet spectrometers designed to provide the functions of a Spectronic 20 spectrophotometer  
**The StellarNet drivers need to be requested from the company.  To get the drivers you will need to complete a Software License Agreement with them (https://www.stellarnet.us/wp-content/uploads/StellarNet-SLA.pdf).  This project offers a working frontend without violating the license agreement.**  
## Project Goals and Motivations  
The goal of this project was to replace the old Spec 20s in our teaching laboratories with equivalent functionality in 
modern equipment.  Choices of hardware and software were driven largely by familiarity.  The choice of the Raspberry Pi was 
to make an effectively disposable computer.  I picked Python 3.x (the older branch works on Python 2.7) for simplicity in migrating to different hardware.  What I created here is a simple frontend for the spectrometer suitable for use by relatively untrained undergraduate students.
## Project Audience  
The project was written to support undergraduate laboratories, so really this repository is for people looking for a frontend 
to run their spectrometer.  However, the functionality of the project can readily be expanded to take advantage of the 
spectrometer features.  This code takes care of collecting the spectra, everything else is just manipulations in code.  Simple changes in the code shift the interface from having lots of things chosen for you to needing to make lots of choices.
## PiSpec20 Requirements  
The *master branch* works on newer (as of May 2024) Python 3.x versions.  Separate branches for Python 2.7 and older 3.x versions are available.  I wrote this on a Raspberry Pi 3b+.  The *master branch* was tested on Python 3.9 and 3.11 with Raspbian OS *Bullseye* and *Bookworm*.  The *Bookworm* distribution is slow on a 3b+, and not entirely recommended.  
For Windows or Mac you will need to make small changes to the code to deal with OS peculiarities.  You will need to possess a Stellarnet spectrometer.
### Libraries 
For Raspbian OS, the `apt-get` package manager was used for sytem packages.  For other Linux types, the appropriate package manager (*e.g.*, yum for CentOS) will depend on your Linux distribution.   The `pip` or `pip3` (depending on your Python set-up) get the Python packages.  Note that on Raspbian starting with the 'Bookwork' distribution, `pip` installs must be to a virtual environment to obey the stricter versioning rules.  
For Windows and MacOS, one would typically use `pip` to install Python libraries.  Help with pip is available at https://packaging.python.org/tutorials/installing-packages/  
- pyusb 1.2.1  (Linux python 3 example:  `sudo pip3 install pyusb==1.2.1`)  this is version specific, so `pip` is appropriate especially for *venv*
- libusb-1.0-0-dev
- numpy 1.24.2 
- matplotlib
- screen (if you want to hide the background processes)  
- libraries usually automatically included in Python
  - python-virtualenv  (if you want to run this in a virtual environment)
  - Tkinter  
### Files to install
- Stellarnet has dramatically simplified the installation process since 2019, so there is a lot less for the user to manage.  
- the rest of the files in PiSpec20_stellarnet should go into the same directory
- on a Windows system you will need the free 'SWDrivers.zip' or 'SWDriver64.exe' from https://www.stellarnet.us/stellarnet-downloads  instead of the driver included in this package  
- use the 'run_hidden' bash script to start the project without showing the command line.  From the command line issue `sudo chmod +x run_hidden` to make the bash script executable.  On Windows a batch file would substitute the bash script.
### Other Hardware  
- a USB connected StellarNet spectrometer  
- a light source if you are going to do absorbance experiments
## Typical Install  
The following steps were followed to install this project on a Raspberry PI model 3B+ with a fresh Raspbian (full version) installation:  
- `sudo apt-get install screen`  
- `sudo apt-get install pyusb==1.2.1`
- `sudo pip install numpy==1.24.1`
- `sudo pip matplotlib`
- downloaded this repository  
- `python3 stellarnet_spec.py` runs the interface  
## Supported Devices  
### Directly tested 
| Manufacturer  | Spectrometer  | Works ?       |  
| ------------- | ------------- | ------------- |  
| StellarNet    | Black Comet   |     yes       |

### Should work with StellarNet driver  
| Spectrometer | Linux driver | Windows driver |
| ------------ | :----------: | :------------: |
| Blue Wave | x | x |
| Black Comet | x | x |
| Silver Nova | x | x |
| High Resolution | x | x |
| Green Wave | x | x |

## How to Help  
I don't write in Python for a living, nor particularly do a lot of programming.  And it shows in the code.  
If you wish to contribute please contact me.
## License  
MIT license
