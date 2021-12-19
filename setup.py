from setuptools import setup

setup(
    name='beets-extended-metadata',
    version='0.2.4',
    description='beets plugin to use custom, extended metadata',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Joscha Düringer',
    author_email='joscha.dueringer@beardbot.net',
    url='https://github.com/calne-ca/beets-plugin-extended-metadata',
    license='MIT',
    platforms='ALL',

    test_suite='test',

    packages=['beetsplug'],

    install_requires=[
        'beets>=1.4.9',
        'mediafile>=0.9.0'
    ],

    tests_require=[
        'pytest==6.2.5',
        'mockito==1.3.0',
        'testcontainers==3.4.2'
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
