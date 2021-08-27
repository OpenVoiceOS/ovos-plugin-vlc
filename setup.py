#!/usr/bin/env python3
from setuptools import setup


PLUGIN_ENTRY_POINT = 'ovos_vlc=ovos_plugin_vlc'

setup(
    name='ovos_plugin_vlc',
    version='0.0.1a3',
    description='vlc plugin for ovos',
    url='https://github.com/OpenVoiceOS/ovos-vlc-plugin',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['ovos_plugin_vlc'],
    install_requires=["python-vlc>=1.1.2",
                      "ovos-plugin-manager>=0.0.1a3"],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='ovos audio plugin',
    entry_points={'mycroft.plugin.audioservice': PLUGIN_ENTRY_POINT}
)
