# This is part of a Python framework to compliment "Robust Smartphone App Identification Via Encrypted Network Traffic Analysis".
# Copyright (C) 2017  Vincent F. Taylor and Riccardo Spolaor
# See LICENSE for more details.


import gzip, pickle , cPickle

from sklearn.metrics.classification import accuracy_score, precision_score, recall_score, f1_score


##DIRECTORY OF RESULTS
dir_results="results/"

def get_results(results, instance_of_datasets, classifier_name, y_true, y_pred, file_dump):
    tmp_ = {"y_pred": y_pred,
                                                      "y_true": y_true,
                                                      "accuracy": accuracy_score(y_true, y_pred),
                                                      "precision_micro": precision_score(y_true, y_pred,
                                                                                         average="micro"),
                                                      "precision_macro": precision_score(y_true, y_pred,
                                                                                         average="macro"),
                                                      "recall_micro": recall_score(y_true, y_pred, average="micro"),
                                                      "recall_macro": recall_score(y_true, y_pred, average="macro"),
                                                      "f1_micro": f1_score(y_true, y_pred, average="micro"),
                                                      "f1_macro": f1_score(y_true, y_pred, average="macro")
                                                      }

    cPickle.dump(tmp_, gzip.open("%s/single_%s_%s_%s.zcp"%(dir_results,file_dump,instance_of_datasets, classifier_name), "wb+"))
    results[instance_of_datasets][classifier_name]=tmp_
    print(classifier_name,
          "accuracy", results[instance_of_datasets][classifier_name]["accuracy"],
          "f1 score_micro", results[instance_of_datasets][classifier_name]["f1_micro"],
          "precision_micro", results[instance_of_datasets][classifier_name]["precision_micro"],
          "recall_micro", results[instance_of_datasets][classifier_name]["recall_micro"],
          "f1 score_macro", results[instance_of_datasets][classifier_name]["f1_macro"],
          "precision_macro", results[instance_of_datasets][classifier_name]["precision_macro"],
          "recall_macro", results[instance_of_datasets][classifier_name]["recall_macro"]
          )
    cPickle.dump(results, gzip.open(dir_results+"/"+file_dump, "wb+"))
    return results

