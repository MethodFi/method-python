from setuptools import setup, find_packages

setup(
    name='method-python',
    version='1.2.4',
    description='Python library for the Method API',
    long_description='Python library for the Method API',
    long_description_content_type='text/x-rst',
    author='Marco del Carmen',
    author_email='marco@mdelcarmen.me',
    url='https://github.com/MethodFi/method-python',
    license='MIT',
    packages=find_packages(exclude='test'),
    package_data={'README': ['README.md']},
    python_requires=">=3.6",
    install_requires=[
        'hammock==0.2.4'
    ],
)
