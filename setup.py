from setuptools import setup

setup(
    name='pyevmasm',
    version='0.1.0',
    description='Ethereum Virtual Machine (EVM) assembler and disassembler',
    scripts=['evmasm'],
    author='Trail of Bits',
    author_email='evmasm@trailofbits.com',
    url='https://github.com/trailofbits/pyevmasm',
    license='Apache License 2.0',
    packages=['pyevmasm'],
    python_requires='>2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    install_requires=[
        'future'
        ],
    extras_require={
        'dev': [
            'nose'
            ]
        }
)
