import math
import metapy
import sys
import time

def make_classifier(training, inv_idx, fwd_idx):
    """
    Use this function to train and return a Classifier object of your
    choice from the given training set. (You can ignore the inv_idx and
    fwd_idx parameters in almost all cases, but they are there if you need
    them.)

    **Make sure you update your config.toml to change your feature
    representation!** The data provided here will be generated according to
    your specified analyzer pipeline in your configuration file (which, by
    default, is going to be unigram words).

    Also, if you change your feature set and already have an existing
    index, **please make sure to delete it before running this script** to
    ensure your new features are properly indexed.
    """
    # Baseline
    # return metapy.classify.NaiveBayes(training)
    # Lower, even with variations of gamma and max_iter
    # return metapy.classify.LogisticRegression(training = training)
    # Lower
    # return metapy.classify.KNN(training = training, inv_idx = inv_idx, k = 4, ranker = metapy.index.OkapiBM25(), weighted = False)
    # Higher k does not improve
    # return metapy.classify.KNN(training = training, inv_idx = inv_idx, k = 8, ranker = metapy.index.OkapiBM25(), weighted = True)
    
    return metapy.classify.OneVsAll(training, metapy.classify.SGD, loss_id='hinge')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    metapy.log_to_stderr()

    cfg = sys.argv[1]
    print('Building or loading indexes...')
    inv_idx = metapy.index.make_inverted_index(cfg)
    fwd_idx = metapy.index.make_forward_index(cfg)

    dset = metapy.classify.MulticlassDataset(fwd_idx)
    view = metapy.classify.MulticlassDatasetView(dset)
    view.shuffle()
    
    training = view[0:int(0.75*len(view))]
    testing = view[int(0.75*len(view)):len(view)+1]

    print('Running cross-validation...')
    start_time = time.time()
    matrix = metapy.classify.cross_validate(lambda fold:
            make_classifier(fold, inv_idx, fwd_idx), dset, 5)
    print(matrix)

    classifier = make_classifier(training, inv_idx, fwd_idx)
    # classifier.classify(testing[0].weights))
    tmatrix = classifier.test(testing)
    tmatrix.print_stats()

    print(classifier.classify(testing[12].weights))
    print(testing[12].id)
    

    matrix.print_stats()
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
