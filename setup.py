from distutils.core import setup

VERSION = '0.1'
setup_kwargs = {
    "version": VERSION,
    "description": 'Cyclus input generation from PRIS database',
    "author": 'Jin Whan Bae',
}

if __name__ == '__main__':
    setup(
        name='write_input',
        packages=["write_input"],
        **setup_kwargs
    )
