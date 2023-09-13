F# Instalación

Esta carpeta contiene la descripción para la instalación manual, la descripción de las dependencias de python y el script de instalación automática.

Suponemos que la instalación se realiza en un Ubuntu 20.04.6 LTS limpio, si no es el caso, siga la guía de instalación paso a paso y modifique los comandos de acuerdo a su situación.  

Considere asignar alrededor de 30 GB o más para este software.  
También es necesario notificar que la instalación podría tardar varias horas debido a la instalación de origen de Gazebo.

## Qué se instalará y qué se hará:  
1. ROS Noetic con ros-control, ros-controllers, controller-manager, geometry2, hector_models, gazebo_ros_pkgs;
2. Gazebo 11 desde la fuente con plugins para el modelo de movimiento de la superficie de contacto;
3. Go más reciente;
4. Bibliotecas Conda y Python (ver `environment.yml`);
5. MongoDB;
6. Se modificará `~/.bashrc`.

## Virtual machine:  
Si desea evitar la instalación, puede utilizar la máquina virtual suministrada. 
Para ello
* Instale la última versión de [Oracle VM VirtualBox](https://www.virtualbox.org/)
* Descargue partes del archivo de infraestructura de escritorio virtual (VDI) dividido mediante `chmod +x download.sh && ./download.sh`.
* Asegúrese de que ha descargado 16 partes de tipo `part...`.
* Reúna esas partes en un archivo .vdi mediante `cat part. > pruebas.vdi
* Pon `tests.vdi` y `tests.vbox` en tu carpeta `VirtualBox VMs` donde "Oracle VM VirtualBox" busca imágenes
* Puedes arrancar esta VM

## Automatic installation (Not Supported):   
Puedes intentar instalar todo automáticamente usando `installation.sh`,
aún así pueden surgir problemas eventuales y le proponemos una guía de instalación manual presentada a continuación.

Para instalar automáticamente:
    `chmod +x installation.sh && ./installation.sh`  

## Manual step-by-step installation:
Tenga paciencia, la instalación de Gazebo a partir del código fuente puede llevar algún tiempo (aproximadamente 1 hora). 

## 1.    Actualizar el sistema, instalar Git y Wget.
```
sudo apt -y update && sudo apt -y upgrade 
```

``` 
sudo apt -y install git wget
```

```
sudo apt install git
```

## 2.    Instalar ROS Noetic.
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
  sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 && \
  sudo apt update && \
  sudo apt install -y ros-noetic-desktop-full && \
  source /opt/ros/noetic/setup.bash && \
  echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc && \
  source ~/.bashrc
```
## 3.    Preparar el sistema para la instalación del Gazebo.
```
sudo apt-get -y remove '.*gazebo.*' '.*sdformat.*' '.*ignition-math.*' '.*ignition-msgs.*' '.*ignition-transport.*'
```

## 4.    Instalar bibliotecas Gazebo.
Ignition CMake  
```
sudo apt-get -y install build-essential cmake pkg-config && \
	git clone https://github.com/ignitionrobotics/ign-cmake /tmp/ign-cmake && \
	cd /tmp/ign-cmake && \
	git checkout ign-cmake2 && \
	mkdir build && \
	cd build && \
	cmake ../ && \
	make -j4 && \
	sudo make install
```
Ignition Math  
```
sudo apt-get -y install build-essential cmake git python && \
	git clone https://github.com/ignitionrobotics/ign-math /tmp/ign-math && \
	cd /tmp/ign-math && \
	git checkout ign-math6 && \
	mkdir build && \
	cd build && \
	cmake ../ && \
	make -j4 && \
	sudo make install
```
Ignition Common  
```
sudo apt-get -y install build-essential \
         cmake \
         libfreeimage-dev \
         libtinyxml2-dev \
         uuid-dev \
         libgts-dev \
         libavdevice-dev \
         libavformat-dev \
         libavcodec-dev \
         libswscale-dev \
         libavutil-dev \
         libprotoc-dev \
         libprotobuf-dev && \
	git clone https://github.com/ignitionrobotics/ign-common /tmp/ign-common && \
	cd /tmp/ign-common && \
	git checkout ign-common3 && \
	mkdir build && \
	cd build && \
	cmake ../ && \
	make -j4 && \
	sudo make install
```
SDFormat  
```
sudo apt-get -y install build-essential \
                     cmake \
                     git \
                     python \
                     libboost-system-dev \
                     libtinyxml-dev \
                     libxml2-utils \
                     ruby-dev \
                     ruby && \
	git clone https://github.com/osrf/sdformat /tmp/sdformat && \
	cd /tmp/sdformat && \
	git checkout sdf9 && \
	mkdir build && \
	cd build && \
	cmake ../ && \
	make -j4 && \
	sudo make install
```
Ignition Messages  
```
sudo apt-get -y install build-essential \
                     cmake \
                     git \
                     libprotoc-dev \
                     libprotobuf-dev \
                     protobuf-compiler && \
	git clone https://github.com/ignitionrobotics/ign-msgs /tmp/ign-msgs && \
	cd /tmp/ign-msgs && \
	git checkout ign-msgs5 && \
	mkdir build && \
	cd build && \
	cmake ../ && \
	make -j4 && \
	sudo make install
```
Ignition Fuel Tools  
``` 
sudo apt-get -y install build-essential \
                     cmake \
         libzip-dev \
         libjsoncpp-dev \
         libcurl4-openssl-dev \
         libyaml-dev && \
	git clone https://github.com/ignitionrobotics/ign-fuel-tools /tmp/ign-fuel-tools && \
	cd /tmp/ign-fuel-tools && \
	git checkout ign-fuel-tools4 && \
	mkdir build && \
	cd build && \
	cmake ../ && \
	make -j4 && \
	sudo make install
```
Ignition Transport  
```
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
    wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
    sudo apt-get -y update && \
    sudo apt-get -y install libignition-transport8-dev
```
## 5.    Inicializar el espacio de trabajo.
```
mkdir ~/catkin_ws
mkdir ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
## 6. Copy the project
```
cd ~/catkin_ws/src
git clone https://github.com/Hiram8A/robot_ws.git
```
## 7.    Instalación Gazebo.
```
git clone https://github.com/osrf/gazebo /tmp/gazebo && \
cp -r ~/catkin_ws/src/robot_ws/plugins/gazebo_plugins/* /tmp/gazebo/plugins && \
cd /tmp/gazebo && \
source /opt/ros/noetic/setup.bash && \
mkdir build && \
cd build && \
cmake ../ && \
make -j4 && \
sudo make install   
```
## 8.   Copiar plugins del control de los Fipplers.
```
cd  ~/catkin_ws/src/robot_ws/plugins/flipper_control
mkdir build
cd build && \
cmake .. && \
make -j4 && \
sudo cp libjaguar_plugin.so /usr/lib/
```
## 9.   Modificación de las variables del entorno , la ruta por defecto es /usr/local
```
echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> ~/.bashrc 
```

```
echo "export PATH=/usr/local/bin:$PATH" >> ~/.bashrc
```

```
echo "export PKG_CONFIG_PATH=/usr/local/lib/
```

```
pkgconfig:$PKG_CONFIG_PATH" >> ~/.bashrc
```

```
source ~/.bashrc
```
## 10.   Instalación de paquetes ROS.
```
sudo apt-get install -y ros-noetic-gazebo-ros-control 
```

```
ros-noetic-ros-controllers ros-noetic-ros-control 
```

```
ros-noetic-controller-manager ros-noetic-joint-state-controller 
```

```
cd ~/catkin_ws/src && \
    git clone https://github.com/ros-simulation/gazebo_ros_pkgs.git -b noetic-devel && \
    git clone https://github.com/ros/geometry2.git -b 0.7.5 && \
    git clone https://github.com/tu-darmstadt-ros-pkg/hector_models.git && \
    source /opt/ros/noetic/setup.bash && \
    cd ~/catkin_ws && \
    /bin/bash -c "catkin_make"
```

## 11.    Intalacion de paqueterias previas python
```
sudo apt install curl
```

## 11.   Instalación de Python
Verificar instalacion de python
```
python3 --version
```

Instalar Python en caso de no tenerlo
```
sudp apt-get update
sudo apt-get install python3.7
```

```
cd ~/ && curl https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh --output conda.sh &&\
    chmod +x ~/conda.sh &&\
    ~/conda.sh -b
```

```
echo "export PATH=~/anaconda3/bin:$PATH" >> ~/.bashrc
```

```
source ~/.bashrc
```

```
conda init bash
```

```
source ~/.bashrc
```

```
conda env create -f ~/catkin_ws/src/robot_ws/installation/
environment.yml
```

```
echo "conda activate sb_learning" >> ~/.bashrc && source ~/.bashrc
```

```
cd ~/catkin_ws/src/robot_ws/gym-training && pip install -e .
```
## 12.   Instalación Go. 
```
cd ~/Downloads
```

```
wget https://golang.org/dl/go1.16.6.linux-amd64.tar.gz
```

```
rm -rf /usr/local/go 
```

```
sudo tar -C /usr/local -xzf go1.16.6.linux-amd64.tar.gz
```

```
echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
```

```
source ~/.bashrc
```
## 13.   Instalación de MongoDB.
```
sudo apt-get install -y gnupg
```

```
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
```

```
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
```

```
sudo apt-get update
```

```
sudo apt-get install -y mongodb-org
```

```
echo "running=\`pgrep mongod\`
if  [[ !  -z  \$running  ]]
then
  echo \"Mongo is already running\" \$running
else
  sudo systemctl start mongod
  echo \"Mongo is started\"
fi
">> ~/.bashrc
```

## 14.   Instalacion de paquetes de las cámaras.
```
sudo apt update
```

```
sudo apt install ros-noetic-gazebo-ros-pkgs
```

## 15.   Instalacion de los paquetes del Joystick
```
sudo apt-get install ros-noetic-joy
```

### 15.1   Configuración del Joystick

Conecte su joystick a su ordenador. Ahora veamos si Linux reconoce tu joystick.
```
ls /dev/input/
```
Verá una lista de todos sus dispositivos de entrada similar a la siguiente:
```
by-id    event0  event2  event4  event6  event8  mouse0  mouse2  uinput
by-path  event1  event3  event5  event7  js0     mice    mouse1
```

Como puedes ver arriba, los dispositivos joystick son referidos por jsX ; en este caso, nuestro joystick es js0. Asegurémonos de que el joystick funciona.
```
sudo jstest /dev/input/jsX
```
Verás la salida del joystick en la pantalla. Mueve el joystick para ver cómo cambian los datos.
```
Driver version is 2.1.0.
Joystick (Logitech Logitech Cordless RumblePad 2) has 6 axes (X, Y, Z, Rz, Hat0X, Hat0Y)
and 12 buttons (BtnX, BtnY, BtnZ, BtnTL, BtnTR, BtnTL2, BtnTR2, BtnSelect, BtnStart, BtnMode, BtnThumbL, BtnThumbR).
Testing ... (interrupt to exit)
Axes:  0:     0  1:     0  2:     0  3:     0  4:     0  5:     0 Buttons:  0:off  1:off  2:off  3:off  4:off  5:off  6:off  7:off  8:off  9:off 10:off 11:off
```

Ahora vamos a hacer el joystick accesible para el nodo ROS joy. Empieza por listar los permisos del joystick:
```
ls -l /dev/input/jsX
```

Verás algo parecido a:
```
crw-rw-XX- 1 root dialout 188, 0 2023-07-25 10:04 /dev/input/jsX
```
Si XX es rw: el dispositivo js está configurado correctamente.

Si XX es --: el dispositivo js no está configurado correctamente y necesitas:

```
sudo chmod a+rw /dev/input/jsX
```

## 16.   Inicio del nodo Joy
Para obtener los datos del joystick publicados sobre ROS necesitamos iniciar el nodo joy. En primer lugar vamos a decirle al nodo joy qué dispositivo de joystick utilizar- el valor predeterminado es js0.

```
roscore
rosparam set joy_node/dev "/dev/input/jsX"
```

Ahora podemos iniciar el joy Node.
```
rosrun joy joy_node
```

Verás algo parecido a:
```
[ INFO] 1253226189.805503000: Started node [/joy], pid [4672], bound on [aqy], xmlrpc port [33367], tcpros port [58776], logging to [/u/mwise/ros/ros/log/joy_4672.log], using [real] time

[ INFO] 1253226189.812270000: Joystick device: /dev/input/js0

[ INFO] 1253226189.812370000: Joystick deadzone: 2000
```

Ahora en un nuevo terminal puedes hacer rostopic echo del  joy topic para ver los datos del joystick:
```
rostopic echo joy
```

Al mover el joystick, verás algo parecido a :
```
---
axes: (0.0, 0.0, 0.0, 0.0)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, 0.0, 0.12372203916311264)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, -0.18555253744125366, 0.12372203916311264)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, -0.18555253744125366, 0.34022033214569092)
buttons: (0, 0, 0, 0, 0)
---
axes: (0.0, 0.0, -0.36082032322883606, 0.34022033214569092)
buttons: (0, 0, 0, 0, 0)
```

En `electric` y superior al nuevo `sensor_msgs/Joy`  se emite un mensaje que incluye un encabezado como el siguiente:

```
---
header: 
  seq: 9414
  stamp: 
    secs: 1325530130
    nsecs: 146351623
  frame_id: ''
axes: [-0.0038758506998419762, -0.0038453321903944016, -0.0, -0.999969482421875, 0.0, 0.0]
buttons: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
---
header: 
  seq: 9415
  stamp: 
    secs: 1325530130
    nsecs: 146351623
  frame_id: ''
axes: [-0.0038758506998419762, -0.0038453321903944016, -0.0, -0.999969482421875, 0.0, 0.0]
buttons: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
---
header: 
  seq: 9416
  stamp: 
    secs: 1325530130
    nsecs: 146351623
  frame_id: ''
axes: [-0.0038758506998419762, -0.0038453321903944016, -0.0, -0.999969482421875, 0.0, 0.0]
buttons: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
---
```

## 17.   Inicialización del proyecto.
```
roscd control/..
```

```
python build.py
```



## Recusos

http://docs.ros.org/en/noetic/api/geometry_msgs/html/msg/Pose.html

https://answers.ros.org/question/54895/how-to-rostopic-echo-only-the-pose-in-the-odom-topic/

http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick
