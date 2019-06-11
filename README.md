# README #

This repository contains scripts for streaming yi action camera and detecting faces on the host pc.

### What is this repository for? ###

* Prashant Tyagi

### How do I get set up? ###

* First Connect the camera to system via wifi, password is: 1234567890
* Run rtspclient.py for vertical token exchange for connection establishment so that camera and system communication goes up.
* Run pi_face_recognition.py to have the demo.
* Add the images (if for other persons to be detected) in the dataset folder.
* Dependencies:
  ->(for rtspclient.py) : Python 2.7
  ->(for pi_face_recognition.py): 
  		Python 3.6
		dlib 
		face_recognition 
		OpenCV-(3.1) 
		imutils 
		Ubuntu operating system(bionic beaver 18.04 LTS)
  

### Contribution guidelines ###

* Contribute as per the planning

### Who do I talk to? ###

* Prashant Tyagi(Contributor of this repo)
