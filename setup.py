from setuptools import setup, find_packages


def readme():
    return open('README.md', 'r').read()


setup(
    name='discord-obs',
    author='micoli',
    author_email='',
    version='0.1.0',
    description='obs webcam discord menu',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/micoli/discord-obs',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('share/applications', ['discord_obs.desktop']),
        ('share/icons/hicolor/256x256/apps', ['antenna-off.png', 'antenna-off.png', 'antenna-off.png']),
        ('share/icons/hicolor/scalable/apps', ['antenna-off.svg', 'antenna-off.svg', 'antenna-off.svg'])
    ],
    install_requires=[
        'PyGObject>=3.22',
        'pyxdg',
        'gbulb',
        'python-libxdo',
        'asyncio',
        'simpleobsws',
    ],
    extras_require={
        "testing": [
            "pylint"
        ]
    },
    entry_points={
        'console_scripts': [
            'discord-obs = discord_obs.__main__:entrypoint',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing',
    ],
    keywords='discord obs menu gtk',
    license='GPLv3+',
)
