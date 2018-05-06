# EHR Predictor
## simran5 CS410
For CS410 Text Information Systems, I have created a basic text-classification scheme for the following diseases:
Parkinson's
Diabetes
Breast Cancer
ALS
Heart Disease
Multiple Sclerosis
Hemophilia
Acid Reflux

Under the diseases folder in the root directory, you can find all of the original texts that were used to create the classifications for each topic (aka disease). They are configured using a file.toml file, such that each file underneath a given disease is an individual classification document.

To use:
`git clone` 
`pip install requirements`
from root directory:
`python classify.py config.toml`

This will output some of the accuracy statistics to the terminal, then launch a GUI that can be used to enter in some text about your condition. 
For example, I might type in :
> I have been bleeding very easily from different parts of my body. It's hard to control the blood. Once it starts, it continues for a while.

Then there will be some diagnosis text in the bottom right corner of the screen.
---

In the future, I would like to add more diseases to this tool and get a more robust classification scheme of 98% accuracy or more. Ideally, the interface should also be more comprehensive, possibly taking into account additional paramters like height and weight.

Hope you enjoy!
