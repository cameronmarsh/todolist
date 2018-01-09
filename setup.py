from setuptools import setup

setup(
    name="todolist",
    version='1.0',
    py_modules=['todo'],
    install_requires=['Click'],
    entry_points='''
        [console_scripts]
        todo=todo:cli
    ''',

)
