# Helmet Impact Force Monitor adapted on Raspberry 2

The objective of this project is to measure the impact handled by a body during a fall and notice the user if medical attention is needed.

In fact, by impact we mean the force of the impact. And for that end, we will use an accelerometer to measure the G-force that is exerted on the body.
Studies have shown that G-force above 9G can be fatal and G-force between 4G and 6G can also be dangerous if sustained for a few seconds.

Our inpiration of this project comes from [this link](https://learn.sparkfun.com/tutorials/raspberry-pi-zero-helmet-impact-force-monitor?_ga=2.98552733.34402635.1521538802-1075053833.1521538802)

## Materials needed

* Raspberry Pi 2
	* with its power cable
	* a microSD card with NOOBS OS installed on it
* An accelerometer
	* We used a LISD2H accelerometer but we will explain how to adapt the code to yours
* An LED and its appropriate resistor
	* We used a red LED and a 1kohms resistor
* Some jumper wires
* A USB camera

![alt text](https://github.com/VcVh/Helmet-Impact-Force-Monitor/blob/master/img/materiel.jpg "test")

## Configuration of your Raspberry

The easiest way to enable SSH and I2C on your device is by plugging a monitor, a keyboard and a mouse to it. Then power-up your card and open a terminal and type:
	* sudo apt-get update
	* sudo apt-get upgrade
	* sudo shutdown -r now

Then search for the configuration panel where you can enable both I2C and SSH.

Now you won't need the peripherals anymore but you will need to know the IP address of your card. You can find it using a software such as IP Tracker.
Once known, you are now able to control your Rapsberry Pi using Putty.



Once you're connected on your card, we will need to install some libraries. One for the camera and one in order to use Excel files.

Type the following commands :
* To install Open CV2 (Camera)
	* sudo apt-get install python-opencv
	* sudo apt-get install python-scipy
	* sudo apt-get install ipython
* To install Xlsx Writer
	* git clone https://github.com/jmcnamara/xlswriter.git


## Build the circuit

On the following picture, in green you can see the connections to do for the LED and in blue the connections related to the accelerometer.
![alt text](https://github.com/VcVh/Helmet-Impact-Force-Monitor/blob/master/img/pinout.jpg "test")


Don't forget to plug-in your USB camera in one of the slots of the Raspberry and the Ethernet cable.
Here is a picture of the complete circuit :
![alt text](https://github.com/VcVh/Helmet-Impact-Force-Monitor/blob/master/img/montage.jpg "test")

## Program it

The python code is available on this repository (casque.py).
You should check that some lines of the code are in accordance to your circuit.

Line 37: Check the address used by your accelerometer using the command :

i2cdetect -y 1

In our case here is the result:
![alt text](https://github.com/VcVh/Helmet-Impact-Force-Monitor/blob/master/img/i2cdetect.JPG "test")

Line 40; 70 to 83;100;102;104 : Refer to the datasheet of your accelerometer to complete accordingly.

Line 43: Check on the Pinout figure that you connected the positive side of your LED on the corresponding GPIO (in our case it is GPIO 26).

The Python code works as demonstrated by the following block diagram.


In order to upload the code on the Raspberry Pi, you can use a software such as FileZilla.
Here is how to configure it:

![alt text](https://github.com/VcVh/Helmet-Impact-Force-Monitor/blob/master/img/Filezilla.JPG "test")

Then you can just drag and drop your code on a folder in your Pi.

To run it, go on Putty and search for the directory you put your code in using the line of command: cd "Insert_name_of_your_directory"

Then type : sudo python casque.py

A demonstration of the project working is available on [this Youtube video](https://www.youtube.com/watch?v=R443RuSPm10&feature=youtu.be)












