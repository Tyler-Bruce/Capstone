# Capstone
Hello, my name is Tyler Bruce and this is my Capstone for CS 4233. Here you will find all of the source code, drafts, and pictures used within my project.
My capstone is a manual for Parallel Computing within Python. I use Python 3.9.0 for all of the coding. Please click the links below to navigate to various sections of this project.
 - [Manual PDFs](Manual/)
 - [Manual Docs](Manual/Microsoft%20Word%20Docs)
 - [Source Code](Source%20Code/)
 - [Proposal Docs](Proposal/)
 - [Latest Version of Manual](Manual/Final.pdf)
# Table of Contents
1. [Installation Instructions](Installation-Instructions)
2. [Requirements Analysis](Requirements=Analysis)
3. [Usage Instructions](Usage-Instructions)
4. [License](License)

# Requirements Analysis
Once I had my project set in stone, I had a clear idea of what I needed to do for my project to be considered complete. I needed to develop a procedural manual for parallelizing CPU bound and I/O bound code with Python. I needed to utilize threads, processes, thread and process pools using Async IO and I needed do so with a clear set of easily repeatable instructions that were supplemented with examples of code that I wrote. Provided with the manual are serial programs that are to be attempted by the end user of the manual. For reference, I also include parallel programs using the same serial programs so that they can help guide the end user with parallelizing their own code. All of this material is to be uploaded to Github so that it may be downloaded and attempted by the user.

# Installation Instructions
[Python 3.9.0+](https://www.python.org/downloads/) was used in this project. [Visual Studio Code](https://code.visualstudio.com/Download) was the IDE that worked well for me, but any Python friendly IDE will work. The modules used in this project that are not within the Python standard library are:
 - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 - [requests](https://docs.python-requests.org/en/master/)

To install a Python module in Visual Studio Code, first find your terminal and type in this piece of code.
```
python -m pip install SomePackage
```
This should activate the pip installer which will download and install your module of choice. After this process is complete, you can import your module like so.
```Python
import SomePackage
```

# Usage Instructions
Take the serial program files found within the [Source Code folder](Source%20Code/) and parallelize them using the [manual](Manual/v2.5(revised)Manual%20for%20Parallel%20Computing%20in%20Python.pdf) as a primary resource. Feel free to reference the code I wrote as a complementary piece to the manual.

# License
[MIT License](License/LICENSE)
