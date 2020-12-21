import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
]

REQUIREMENTS = ['requests', 'beautifulsoup4', 'lxml', 'tqdm', 'halo']

setuptools.setup(
    name='erome',
    version='0.0.1',
    author='Amenly',
    author_email='uamenly@protonmail.com',
    description='A program for downloading photos and videos from EroMe',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Amenly/EroMe',
    packages=setuptools.find_packages(),
    classifiers=CLASSIFIERS,
    keywords=['erome', 'scraper', 'download', 'photos', 'videos'],
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': ['erome=erome.erome:main']
    }
)
