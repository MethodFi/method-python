from setuptools import setup, find_packages

setup(
    name='method-python',
    version='0.0.14',
    description='Python library for the Method API',
    author='Marco del Carmen',
    author_email='marco@mdelcarmen.me',
    url='https://github.com/MethodFi/method-python',
    license='MIT',
    packages=find_packages(exclude='tests'),
    package_data={'README': ['README.md']},
    python_requires=">=3.6",
    install_requires=[
        'hammock==0.2.4'
    ],
)
