# guide to setup yard with rfcat

## basic rfcat setup:
	https://blog.thehackingday.com/2019/08/yard-stick-one-primeros-pasos.html

## Notes About YARD:
	https://gist.github.com/JamesHagerman/40f414c5f0db8d476d64f78f9dd3a7b6

## using YARD with RFcat and OOKTOOLS
	https://softwaretester.info/rfcat-on-bigsur-yard-stick-one/
	https://softwaretester.info/tag/rfcat/

## RFCat

### To list usbs and see if YARD its connected and detected
```
lsusb
```

### run rfcat:
```
sudo rfcat -r
```

### test:
```
d.ping()
```

### show config:
```
print(d.reprRadioConfig())
```

### read air waves on freq:
```
d.specan(433000000)
```

### maybe rfcat for mac:
https://github.com/gqrx-sdr/gqrx/issues/714
pip install PySide2
rfcat -r
d.specan(315000000)

## OOKTools
On-Off keying:
	https://greatscottgadgets.com/sdr/



OOKTOOLS:
sudo ooktools --help
	nice project that started the invention of the tool
	https://leonjza.github.io/blog/2016/10/02/reverse-engineering-static-key-remotes-with-gnuradio-and-rfcat/

	explanation of the tool:
	https://leonjza.github.io/blog/2016/10/08/introducing-ooktools.-on-off-keying-tools-for-your-sdr/
	https://leonjza.github.io/blog/2016/10/08/ooktools-on-off-keying-tools-for-your-sdr/
i had to debug a ooktools file bc it was written in python2.7
original backup is in /tesis 



## GQRX

would be great if i could make GQRX work:
	gqrx
	cant find the yard in the devices
	here, GQRX wont work::
	https://forums.hak5.org/topic/36844-yard-stick-one-configuration-help/

