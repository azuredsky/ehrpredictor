import math
import metapy
import sys
import time
from tkinter import Tk, Label, Text, Button, LEFT, RIGHT, END

class SimpleGUI:
    def __init__(self, master, classifier, fwd_idx):
        self.master = master
        master.title("EHR Diagnosis Tool")

        self.label = Label(master, text="Use this tool to help predict your medical conditions.")

        self.label.pack()

        self.entry = Text(master)
        self.entry.pack()

        self.submit_button = Button(master, text="Diagnose!", command=self.parseInput)
        self.submit_button.pack(side=LEFT)

        self.response = Label(master, text="")
        self.response.pack(side=RIGHT)

    def parseInput(self):
        user_input = self.entry.get("1.0", END)
        # Ensure the user has entered something.
        if len(user_input) >= 1:
            pred = diagnose(classifier, fwd_idx, user_input)
            response = get_response(pred)
            self.response["text"] = response

def make_classifier(training, inv_idx, fwd_idx):
    """
    This function wil define our classifier. I am using a OneVsAll as it 
    had the highest accuracy on my training set.
    """
    
    return metapy.classify.OneVsAll(training, metapy.classify.SGD, loss_id='hinge')

def make_indxs(cfg):
    """
    Inverted idx and forward idx are returned in that order.
    """
    return metapy.index.make_inverted_index(cfg), metapy.index.make_forward_index(cfg)

def make_datasetview(fwd_idx):
    """
    Insert the fwd_idx into a format that can be used by the classifier.
    """
    dset = metapy.classify.MulticlassDataset(fwd_idx)
    view = metapy.classify.MulticlassDatasetView(dset)
    return dset, view

def test_classifier(dset, view, fwd_idx, inv_idx):
    """
    This method was used to ensure a certain level of accuracy from the classifier.
    """
    training = view[0:int(0.75*len(view))]
    testing = view[int(0.75*len(view)):len(view)+1]

    print('Running cross-validation...')
    matrix = metapy.classify.cross_validate(lambda fold:
            make_classifier(fold, inv_idx, fwd_idx), dset, 5)
    matrix.print_stats()

def diagnose(classifier, fwd_idx, user_input):
    doc = metapy.index.Document()
    doc.content(user_input)
    return classifier.classify(fwd_idx.tokenize(doc))

def get_response(prediction):
    if prediction == "acidreflux":
        return "You may have acid reflux."
    elif prediction == "als":
        return "You may have ALS."
    elif prediction == "alzheimer":
        return "You may have Alzheimer's."
    elif prediction == "breastcancer":
        return "You may have breast cancer."
    elif prediction == "diabetes":
        return "You may have diabetes."
    elif prediction == "hemophilia":
        return "You may have hemophilia."
    elif prediction == "multiplesclerosis":
        return "You may have multiple sclerosis."
    elif prediction == "parkinsons":
        return "You may have Parkinson's."
    else:
        return "I'm sorry, something went wrong."

"""
I am using 9 diseases for diagnosis here:
Heart disease
Alzheimer's
Diabetes
Hemophilia
Breast cancer
Acid reflux
Parkinson's
Multiple Sclerosis
ALS

In order to construct the data, I pulled symptomatic profiles from a variety of online resources. 
From there, I used some separate python scripts (found in ./diseases under splitup.py and gencorpus.py) to 
arrange the data in a desired file format to be read by the file.toml. The original text samples can be 
found under the name of their disease in ./diseases.
"""
if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: {} config.toml input.toml".format(sys.argv[0]))
        sys.exit(1)

    metapy.log_to_stderr()

    cfg = sys.argv[1]
    print('Building or loading indexes...')

    # Build the data indices using the config.toml.
    inv_idx, fwd_idx = make_indxs(cfg)

    # Set up the MultiClassDatatsetView to be used for the classifier.
    dset, view = make_datasetview(fwd_idx)
    view.shuffle()
    
    # Test the proposed classifier model to see if it upholds a standard of accuracy.
    test_classifier(dset, view, fwd_idx, inv_idx)

    # Construct the classifier.
    classifier = make_classifier(view, inv_idx, fwd_idx)

    # Now we construct the GUI in order to take user input and run it through the classifier.
    print("Initialize the GUI")

    root = Tk()
    GUI = SimpleGUI(root, classifier, fwd_idx)
    root.mainloop()
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
