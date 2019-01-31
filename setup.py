import setuptools

__version__ = None  # This will get replaced when reading version.py

exec(open('rlbottraining/version.py').read())

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='rlbottraining',
    packages=setuptools.find_packages(),
    install_requires=['rlbot', 'docopt'],
    python_requires='>=3.7.0',
    version=__version__,
    description='A framework for writing custom Rocket League bots that run offline.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='RLBot Community',
    author_email='rlbotofficial@gmail.com',
    url='https://github.com/RLBot/RLBotTraining',
    keywords=['rocket-league', 'training', 'train'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        # Allow people to run `rlbottraining` instead of `python -m rlbottraining`
        'console_scripts': ['rlbottraining = rlbottraining.__main__:main']
    },
)
