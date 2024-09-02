from setuptools import setup, find_packages

setup(
    name='cmponentsDjangoType',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django app for ...',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jose-CR/componentsDjangotype',
    author='Alejandro',
    author_email='',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django :: 3.2',
    ],
    install_requires=[
        'Django>=3.2',
    ],
)