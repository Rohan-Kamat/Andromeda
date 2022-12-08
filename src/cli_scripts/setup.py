from setuptools import setup

setup(
    name='parser_script',
    version='0.1.0',
    py_modules=['parser_script'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'parse = parser_script:parse',
        ],
    },
)