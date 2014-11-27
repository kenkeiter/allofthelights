from setuptools import setup

APP = ['allofthelights.py']
DATA_FILES = ['icon.png']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'requests'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)