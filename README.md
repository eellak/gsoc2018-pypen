# Python PenTest Library - PyPen

Penetration Testing library written in Python  
A [GFOSS](https://summerofcode.withgoogle.com/organizations/4954936912117760/) project for the Google Summer of Code 2018 programme
* [GSoC project link](https://summerofcode.withgoogle.com/projects/#5583642407993344) 

## Description

Development of a Python library for penetration testers. The library will include a set of tools for performing the basic tasks for attacking a remote host. It will include reconnaissance tools such as modules that will be able to collect data for a specific target either through the web or through user input. Moreover, other tools will be developed to create custom dictionaries for username and password attacks. Other attack techniques that will be supported include DoS attack, and BruteForce attack. The library will also include various statistical functions for extracting additional information from a captured host.

## Documentation

There's a detailed documentation section for each module of this project. It contains information regarding:  
* requirements
* installation
* usage
* examples  

See [Wiki](https://github.com/eellak/gsoc2018-pypen/wiki) tab

## Project plan

See [Projects](https://github.com/eellak/gsoc2018-pypen/projects/1) tab

### Work Done

This project consists of three main modules:  
* [User Reconnaissance & Information Gathering](https://github.com/eellak/gsoc2018-pypen/tree/master/user_reconnaissance). This module's purpose is to gather information about Facebook users with public information on their profiles, and to create a collection of that information, which will be used in a dictionary attack.
* [Target System Reconnaissance & Information Gathering](https://github.com/eellak/gsoc2018-pypen/tree/master/target_system_reconnaissance). A set of functions have been developed in order to get useful information for a target system such as open ports, OS info etc.
* [Attack PenTest Tools](https://github.com/eellak/gsoc2018-pypen/tree/master/pentest_tools). A set of simple tools that try to take advantage of any information gathered with the use of our User Reconnaissance module and Target System Reconnaissance module, in order to succeed in some basic attack techniques.

## Future Work

Possible additions or improvements to this project could be the following:  
* An SSH bruteforce module (brutSSH.py), similar to bruftp.py
* The improvement of pydos_scapy.py, as it is not very effective at the moment, plus the improvement of the simple socket implementation, in order for the script to be cross platfrom and not depend on hping3
* An extension of the User Reconnaissance module so that it covers a wider variety of social networks, such as Instagram, Twitter, LinkedIn etc.
* A distributed, online password cracking module, based on our User Reconnaissance data, that will possibly use spoofed IPs to ensure a large number of attempts.

## Contributors

### Developer

* Konstantinos Christos Liosis

### Mentors

* [Antonios Andreatos](https://www.researchgate.net/profile/Antonios_Andreatos)
* [Panagiotis Karampelas](https://www.linkedin.com/in/panagiotis-karampelas-5868002/)
* [Christos Pavlatos](http://www.cslab.ece.ntua.gr/~pavlatos/)

### Organization

[Open Technologies Alliance - GFOSS](https://gfoss.eu/)

## Final Report (Gist)

[gsoc18_pypen_report.md](https://gist.github.com/stikos/5228db0426a902e8833e7d73d67ec102)

### Disclaimer

*The purpose of this library is educational, for Penetration Testing and Ethical Hacking and under no circumstances for malicious actions. It's use will comply to all current data protection legislation.*
