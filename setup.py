from setuptools import setup

setup(
    name='regDelta',
    version='0.1',
    py_modules=['projekt'],
    install_requires=[
        'Click',
        'setuptools',
    ],
    entry_points='''
    [console_scripts]
    regDelta=regDelta:main
     ''',
)