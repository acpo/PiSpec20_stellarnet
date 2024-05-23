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
spectrometer features.  This code takes care of collecting the spectra, everything else is just manipulations in code.  Simple changes in the code shift the interface from having lots of things chosen for you to needing to make lots of choices.  For example, there is a 'Save Button' commented out in the code.  If you uncomment the 3 lines of the GUI for the button, the Save function is fully implemented.  
## PiSpec20 Requirements  
The *master branch* works on newer (as of May 2024) Python 3.x versions.  Separate branches for Python 2.7 and older 3.x versions are available.  I wrote this on a Raspberry Pi 3b+.  The *master branch* was tested on Python 3.9 and 3.11 with Raspbian OS *Bullseye* and *Bookworm*.  The *Bookworm* distribution is slow on a 3b+, and not entirely recommended.  
For Windows or Mac you will need to make small changes to the code to deal with OS peculiarities.  You will need to possess a Stellarnet spectrometer.
### Libraries 
For Raspbian OS, the `apt-get` package manager was used for sytem packages.  For other Linux types, the appropriate package manager (*e.g.*, yum for CentOS) will depend on your Linux distribution.   The `pip` or `pip3` (depending on your Python set-up) get the Python packages.  Note that on Raspbian starting with the 'Bookwork' distribution, `pip` installs must be to a virtual environment to obey the stricter versioning rules.  
For Windows and MacOS, one would typically use `pip` to install Python libraries.  Help with pip is available at https://packaging.python.org/tutorials/installing-packages/  
- libusb-1.0-0-dev  (with apt-get)
- pyusb 1.2.1  (Linux example:  pip3 install pyusb==1.2.1)  this is version specific, so consider using *venv*
- numpy 1.24.2  
- matplotlib  
- (*May 2024*) may need to also get `sudo apt-get install python3-pil.imagetk` to address an import error from matplotlib  
- screen (if you want to hide the background processes)
- libraries usually automatically included in Python
  - python-virtualenv  (if you want to run this in a virtual environment)
  - Tkinter  
### Files to install  
- `99-local.rules` needs to be copied to '/etc/udev/rules.d/' or update the existing .rules file to include rules for StellarNet devices. Otherwise you would need to run as root to get USB access.  
- Stellarnet has dramatically simplified the installation process since 2019, so there is a lot less for the user to manage.
- the rest of the files in PiSpec20_stellarnet should go into the same directory.  The drivers from StellarNet should be placed in a folder within this directory.
- on a Windows system, there is an extra step in the driver installation.  See the documentation from StellarNet.

### Example install process on a Raspberry Pi 3B+    
1) fresh install of Raspbian Bullseye  
2) `sudo apt-get install libusb-1.0-0-dev`  
3) `pip3 install pyusb==1.2.1`  
4) `pip3 install numpy==1.24.2`
5) `pip3 install matplotlib`  
6) `sudo apt-get install python3-pil.imagetk`  
7) copy this repository
8) `sudo cp 99-local.rules /etc/udev/rules.d/99-local.rules`  
9) copy StellarNet drivers to the PiSpec20_LED_stellarnet folder
10) `sudo chmod +x run_hidden` to make the bash script executable.  A batch file would substitute the bash script on Windows.  
11) reboot

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
