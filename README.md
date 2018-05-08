# EHR Predictor
## simran5 CS410

### Overview

For CS410 Text Information Systems, I have created a basic text-classification scheme for the following diseases:
Parkinson's
Diabetes
Breast Cancer
ALS
Heart Disease
Multiple Sclerosis
Hemophilia
Acid Reflux

The application allows a user to input some text about their condition, and in turn receive a diagnostic result about which of these diseases they might possibly have. The motivation for this project was to envision a more intelligent electronic health records platform that can give patients multi-dimensional diagnostic information. There is currently a large problem in usability and information access related to the use of health records, so a tool like this could ease some of the overhead of patient care.

### Implementation

The first phase of this project was focused around data collection. I navigated to reputable sites that provide symptomatic and disease recommendation tools for the ones I was interested in. These include NCBI, Mayo Clinic, and the different non-profit websites. From here, I made a collection of texts, one for each disease that included several key passages. I focused on expected patient symptoms, since this is the intended input data for the project. 

Under the diseases folder in the root directory, you can find all of the original texts that were used to create the classifications for each topic (aka disease). They are configured using a file.toml file, such that each file underneath a given disease is an individual classification document. You will also find two key files `gencorpus.py` and `splitup.py` that were used in conjunction to do some of the organizational lifting to set up the directory for use with metapy.

This project was developed using `metapy`. I used a unigram language model with an ICU-tokenizer and a length filter to interpret the documents. I implemented a OneVAll classifier in order to model the documents as disease topics. I found that the OneVAll classifier using stochastic gradient descent and hinge loss provided good results (93% accuracy via cross validation). 

The UI was made using Tkinter, which I expect should come pre-installed with python distributions, so there should be no need to install additional software for the GUI. 

### Usage

To use:

`git clone https://github.com/simran5/ehrpredictor.git` 

`pip install requirements`

from root directory:

`python classify.py config.toml`

This will output some of the accuracy statistics to the terminal, then launch a GUI that can be used to enter in some text about your condition. 
For example, I might type in :
> I have been bleeding very easily from different parts of my body. It's hard to control the blood. Once it starts, it continues for a while.

Once the text has been entered, click *Diagnose*. Then there will be some diagnosis text in the bottom right corner of the screen.

### Contributions

This was a solo project.

### Future work

In the future, I would like to add more diseases to this tool and get a more robust classification scheme of 98% accuracy or more. Ideally, the interface should also be more comprehensive, possibly taking into account additional parameters like height and weight.

Hope you enjoy!
