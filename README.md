# AllOfTheLights

AllOfTheLights is a quick-and-dirty OS X menubar tool that allows you to simulate scene control with a [RaZberry](http://razberry.z-wave.me/) z-wave daughtercard for the RaspberryPi.

![Screenshot](https://raw.github.com/kenkeiter/allofthelights/master/screenshot.png)

## Getting Started

Make sure you've got the following libraries installed:

+ `requests`
+ `PyObjC`
+ `py2app`

If you've got Python 2.7 installed (most Macs do), you should already have Python, `PyObjC`, and `py2app`. You can install `requests` by running

		$ pip install requests

From there, getting started with AllOfTheLights is simple. First, clone the directory

		$ git clone https://github.com/kenkeiter/allofthelights.git
		$ cd allofthelights/
		
Then, build the application bundle using py2app

		$ python setup.py py2app

Copy the resulting application bundle to your _Applications_ directory

		$ cp dist/allofthelights.app /Applications

The application is now installed! When launched, it will look for `.allofthelights.json` in your home directory. Edit `example.json` to point to your RaspberryPi, and copy it there, like so:

		$ cp example.json ~/.allofthelights.json

All set! Launch the application (which should be at `/Applications/allofthelights.app`). You'll get an error if any JSON errors are encountered.

## License

This code is licensed under the [_MIT Public License_](http://opensource.org/licenses/MIT). Share and enjoy.