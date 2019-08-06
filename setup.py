from setuptools import setup

setup(
    name='pyevmasm',
    version='0.2.1',
    description='Ethereum Virtual Machine (EVM) assembler and disassembler',
    author='Trail of Bits',
    author_email='evmasm@trailofbits.com',
    url='https://github.com/trailofbits/pyevmasm',
    license='Apache License 2.0',
    packages=['pyevmasm'],
    python_requires='>2.7',
    install_requires=[
        'future'
    ],
    extras_require={
        'dev': [
            'nose',
            'coverage',
            'flake8'
        ]
    },
    entry_points={
        'console_scripts': [
            'evmasm = pyevmasm.__main__:main'
        ]
    }
)
