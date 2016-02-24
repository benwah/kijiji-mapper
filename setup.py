from setuptools import setup, find_packages

setup(
    name='kijiji-mapper',
    version='0.1',
    description=(
        'Just a thing to map appartments on Kijiji because somehow they'
        'don\'t have that feature.'),
    author='Ben',
    install_requires=[
        'beautifulsoup4==4.4.1',
        'Jinja2==2.8',
        'PyYAML==3.11',
        'requests==2.9.1',
    ],
    author_email='benoitcsirois at the gmails',
    license='MIT',
    packages=find_packages(),
    zip_safe=False)
