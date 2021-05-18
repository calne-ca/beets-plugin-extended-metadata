from setuptools import setup

setup(
    name='beets-extended-metadata',
    version='0.1.9',
    description='beets plugin to use custom, extended metadata in your queries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Joscha Düringer',
    author_email='joscha.dueringer@beardbot.net',
    url='https://github.com/calne-ca/beets-extended-metadata',
    license='MIT',
    platforms='ALL',

    test_suite='test',

    packages=['beetsplug'],

    install_requires=[
        'beets>=1.4.9',
        'mediafile==0.6.0',
        'futures; python_version<"3"',
    ],

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
