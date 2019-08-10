import setuptools
import importlib

# Avoid native import statements as we don't want to depend on the package being created yet.
def load_module(module_name, full_path):
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
version = load_module("rlbottraining.version", "rlbottraining/version.py")
paths = load_module("rlbottraining.paths", "rlbottraining/paths.py")

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name='rlbottraining',
    packages=setuptools.find_packages(),
    install_requires=[
        'rlbot>=1.25.0',
        'docopt',
        'watchdog',
        'numpy',
    ],
    python_requires='>=3.7.0',
    version=version.__version__,
    description='A framework for writing training for Rocket League bots.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='RLBot Community',
    author_email='rlbotofficial@gmail.com',
    url='https://github.com/RLBot/RLBotTraining',
    keywords=['rocket-league', 'training', 'train'],
    license='MIT License',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        # Allow people to run `rlbottraining` instead of `python -m rlbottraining`
        'console_scripts': ['rlbottraining = rlbottraining.__main__:main']
    },
    package_data={
        'rlbottraining': [
            f'{paths._match_config_dir}/*.cfg',
            f'{paths._example_bot_dir}/*/*.cfg',
            str(paths._website_static_source),
            str(paths._example_rl_custom_training_json),
        ]
    },
)


