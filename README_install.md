# ecmc PYQT GUI installation

## Centos
Need a mix of conda and pip since cannot find all needed packages in conda:

```
sudo yum install conda
# Choose python 3.5 or 3.6 (for 3.6 the below line needs editing)
conda create --name ecmccomgui_py35 python=3.5
conda activate ecmccomgui_py35
pip install pyqt5
pip install matplotlib
pip install numpy
pip install pyepics

sudo yum install qt5-qtbase-devel
```
probbaly pyepics is also needed (but could not find in my notes, maybe alreday installed on the ess centos machines..)..

## Raspian (Raspi 4b)
Setup partly virtuel environment using berryconda (https://github.com/jjhelmus/berryconda).

1. Download "Berryconda3-2.0.0-Linux-armv7l.sh" from https://github.com/jjhelmus/berryconda
2. Run "Berryconda3-2.0.0-Linux-armv7l.sh" script:

```
bash Berryconda3-2.0.0-Linux-armv7l.sh
```

3. Create conda environment and install packages:
```
conda create --name ecmccomgui_py35 python=3.5
source activate ecmccomgui_py35
conda install -c tballance pyqt5
conda install -c "rpi"  numpy
pip install pyepics
pip install pyqtgraph  # Not needed
conda install -c rpi scipy
pip install matplotlib
```
