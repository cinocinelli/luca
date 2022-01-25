import pickle
import bz2
import cPickle
import sys

sys.path.append("..")
import classifiers
import warnings
import numpy

if sys.argv[1] =='0':
    data_path_train = './compressed_pickle_train.pbz2'
    data_path_test = './compressed_pickle_test.pbz2'
elif sys.argv[1] =='1':
    data_path_train = './wang_compressed_pickle_train.pbz2'
    data_path_test = './wang_compressed_pickle_test.pbz2'
elif sys.argv[1] =='2':
    data_path_train = './wangs_compressed_pickle_train.pbz2'
    data_path_test = './wangs_compressed_pickle_test.pbz2'

result_path = './results/'

data_path_train_her = './compressed_pickle_train_herman.pbz2'
data_path_train_inv = './compressed_pickle_train_inverted.pbz2'


data_path_test_her = './compressed_pickle_test_herman.pbz2'
data_path_test_inv = './compressed_pickle_test_inverted.pbz2'

############    this data is not good   ####################################################################################
#data_path_test_waggr7flows = './compressed_pickle_test_waggr7flows.pbz2'
#data_path_test_waggr7flows_inv = './compressed_pickle_test_waggr7flows_inverted.pbz2'
#data_path_test_waggr7flows_her = './compressed_pickle_test_waggr7flows_herman.pbz2'
########################################################################################################################

# data_path_test_wsplitflows = './compressed_pickle_test_wsplitflows.pbz2'
# data_path_test_wsplitflows_inv = './compressed_pickle_test_wsplitflows_inverted.pbz2'
# data_path_test_wsplitflows_her = './compressed_pickle_test_wsplitflows_herman.pbz2'

# data_path_test_wsplit_oneinterface_flows = './compressed_pickle_test_wsplitflows_oneinterface.pbz2'
# data_path_test_wsplit_oneinterface_flows_inv = './compressed_pickle_test_wsplitflows_oneinterface_inv.pbz2'
# data_path_test_wsplit_oneinterface_flows_her = './compressed_pickle_test_wsplitflows_oneinterface_her.pbz2'


# data_path_test_waggr2flows = './compressed_pickle_test_waggr2flows.pbz2'
# data_path_test_waggr2flows_inv = './compressed_pickle_test_waggr2flows_inv.pbz2'
# data_path_test_waggr2flows_her = './compressed_pickle_test_waggr2flows_her.pbz2'

# data_path_test_waggr5flows = './compressed_pickle_test_waggr5flows.pbz2'
# data_path_test_waggr5flows_inv = './compressed_pickle_test_waggr5flows_inv.pbz2'
# data_path_test_waggr5flows_her = './compressed_pickle_test_waggr5flows_her.pbz2'


# data_path_test_waggr2_RANDflows = './compressed_pickle_test_waggr2_RANDflows.pbz2'
# data_path_test_waggr2_RANDflows_inv = './compressed_pickle_test_waggr2_RANDflows_inv.pbz2'
# data_path_test_waggr2_RANDflows_her = './compressed_pickle_test_waggr2_RANDflows_her.pbz2'

# data_path_test_waggr5_RANDflows = './compressed_pickle_test_waggr5_RANDflows.pbz2'
# data_path_test_waggr5_RANDflows_inv = './compressed_pickle_test_waggr5_RANDflows_inv.pbz2'
# data_path_test_waggr5_RANDflows_her = './compressed_pickle_test_waggr5_RANDflows_her.pbz2'




results_file = "results_all"


def read_data_from_pickles(path_):
    data_ = bz2.BZ2File(path_, 'rb')
    data_ = cPickle.load(data_)
    X_flows, labels = [], []
    for label, flow in data_:
        #print(len(flow))
        X_flows.append(flow)
        labels.append(label)

    return X_flows, labels


def train_it():

    results = {}
    results['my dataset'] = {}
    # train and test normal traffic for everything else
    x_train_flows, y_train_labels = read_data_from_pickles(data_path_train)
    # remove comments here to test normal data without flows (for all other classifiers except herrmann and Panchenko16
    x_test_flows, y_test_labels = read_data_from_pickles(data_path_test) #data_path_test

    #train and test normal traffic for herman
    xh_train_flows, yh_train_labels = read_data_from_pickles(data_path_train_her)
    # remove comments here to test normal data without flows collected for herrmann classifier(for herrmann)
    xh_test_flows, yh_test_labels = read_data_from_pickles(data_path_test_her)

    # train and test normal traffic for pachenko
    xinv_train_flows, yinv_train_labels = read_data_from_pickles(data_path_train_inv)
    xinv_train_flows, yinv_train_labels = read_data_from_pickles(data_path_train_inv)
    # remove comments here to test normal data without flows collected by inverting direction (for pachenko 16)
    xinv_test_flows, yinv_test_labels = read_data_from_pickles(data_path_test_inv)

    # remove comments here to test with aggregation-7 flows data not good
    #xaggr7flows_test_flows, yaggr7flows_test_labels = read_data_from_pickles(data_path_test_waggr7flows)
    #xaggr7flowsinv_test_flows, yaggr7flowsinv_test_labels = read_data_from_pickles(data_path_test_waggr7flows_inv)
    #xaggr7flowsh_test_flows, yaggr7flowsh_test_labels = read_data_from_pickles(data_path_test_waggr7flows_her)
    # remove comments here to test with split flows collected on all interfaces
    # xsplitflows_test_flows, ysplitflows_test_labels = read_data_from_pickles(data_path_test_wsplitflows)
    # xsplitflowsinv_test_flows, ysplitflowsinv_test_labels = read_data_from_pickles(data_path_test_wsplitflows_inv)
    # xsplitflowsh_test_flows, ysplitflowsh_test_labels = read_data_from_pickles(data_path_test_wsplitflows_her)
    # # remove comments here to test with split flows collected on one interface
    # xsplit_oneinterface_flows_test_flows, ysplit_oneinterface_flows_test_labels = read_data_from_pickles(data_path_test_wsplit_oneinterface_flows)
    # xsplit_oneinterface_flowsinv_test_flows, ysplit_oneinterface_flowsinv_test_labels = read_data_from_pickles(data_path_test_wsplit_oneinterface_flows_inv)
    # xsplit_oneinterface_flowsh_test_flows, ysplit_oneinterface_flowsh_test_labels = read_data_from_pickles(data_path_test_wsplit_oneinterface_flows_her)
    # # remove comments here to test with aggregation-2 flows
    # xaggr2flows_test_flows, yaggr2flows_test_labels = read_data_from_pickles(data_path_test_waggr2flows)
    # xaggr2flowsinv_test_flows, yaggr2flowsinv_test_labels = read_data_from_pickles(data_path_test_waggr2flows_inv)
    # xaggr2flowsh_test_flows, yaggr2flowsh_test_labels = read_data_from_pickles(data_path_test_waggr2flows_her)
    # # remove comments here to test with aggregation-5 flows
    # xaggr5flows_test_flows, yaggr5flows_test_labels = read_data_from_pickles(data_path_test_waggr5flows)
    # xaggr5flowsinv_test_flows, yaggr5flowsinv_test_labels = read_data_from_pickles(data_path_test_waggr5flows_inv)
    # xaggr5flowsh_test_flows, yaggr5flowsh_test_labels = read_data_from_pickles(data_path_test_waggr5flows_her)
    # # remove comments here to test with aggregation-2 flows with random traffic
    # xaggr2_RANDflows_test_flows, yaggr2_RANDflows_test_labels = read_data_from_pickles(data_path_test_waggr2_RANDflows)
    # xaggr2_RANDflowsinv_test_flows, yaggr2_RANDflowsinv_test_labels = read_data_from_pickles(data_path_test_waggr2_RANDflows_inv)
    # xaggr2_RANDflowsh_test_flows, yaggr2_RANDflowsh_test_labels = read_data_from_pickles(data_path_test_waggr2_RANDflows_her)
    # # remove comments here to test with aggregation-5 flows with random traffic
    # xaggr5_RANDflows_test_flows, yaggr5_RANDflows_test_labels = read_data_from_pickles(data_path_test_waggr5_RANDflows)
    # xaggr5_RANDflowsinv_test_flows, yaggr5_RANDflowsinv_test_labels = read_data_from_pickles(data_path_test_waggr5_RANDflows_inv)
    # xaggr5_RANDflowsh_test_flows, yaggr5_RANDflowsh_test_labels = read_data_from_pickles(data_path_test_waggr5_RANDflows_her)


    
    ####################################################################
    ##  THE CODE BELOW NEEDS NORMAL DATA TO FUNCTION
    ##  TRAINING AND TESTING ON NON AGGREGATED FLOWS
    #####################################################################
    

    #####################################################################
    classifier_name = "liberatoreNB2006"
    print("running", classifier_name)
    y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
                                                              y_train_labels,
                                                              x_test_flows,
                                                              y_test_labels,
                                                              )
    
    results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    result = open(result_path+classifier_name+'.txt','w')
    result.write(str(results))
    result.close()
    print(results)
    #####################################################################

    
    #####################################################################
    classifier_name = "liberatoreJaccard2006"
    print("running", classifier_name)
    y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
                                                                   y_train_labels,
                                                                   x_test_flows,
                                                                   y_test_labels,
                                                                   )
    results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    result = open(result_path+classifier_name+'.txt','w')
    result.write(str(results))
    result.close()
    print(results)
    #####################################################################


    #####################################################################
    
    # print("TRAINING COMPLETE NOW TESTING AGAINST FLOWS WITH AGGREGATION")
    # print("AGGREGATION-2 TESTING")
    # ####################################################################
    # ##  THE CODE BELOW IS TO TEST THE TRAINED MODEL AGAINST TESTING DATA WITH AGGR-2 FLOWS INSTALLED
    # ##
    # #####################################################################
    
    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                                       y_train_labels,
    #                                                                       xaggr2flows_test_flows,
    #                                                                       yaggr2flows_test_labels,
    #                                                                       )

    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr2flows_test_flows,
    #                                                                            yaggr2flows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    

    # #####################################################################
    
    # print("AGGREGATION-5 TESTING")
    
    # ####################################################################
    # ##  THE CODE BELOW IS TO TEST THE TRAINED MODEL AGAINST TESTING DATA WITH AGGR-5 FLOWS INSTALLED
    # ##
    # #####################################################################

    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                                       y_train_labels,
    #                                                                       xaggr5flows_test_flows,
    #                                                                       yaggr5flows_test_labels,
    #                                                                       )

    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr5flows_test_flows,
    #                                                                            yaggr5flows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    # #####################################################################
    
    # print("AGGREGATION-2 WITH RANDOM TRAFFIC")
    
    # ####################################################################
    # ##  THE CODE BELOW IS TO TEST THE TRAINED MODEL AGAINST TESTING DATA WITH AGGREGATION-2 FLOWS INSTALLED, CONTAINING ALSO 
    # ##    RANDOM WEBISTE TRAFFIC IN ADDITION TO THE ONE WE ARE FINGERPRINTING 
    # ##
    # #####################################################################

    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                                       y_train_labels,
    #                                                                       xaggr2_RANDflows_test_flows,
    #                                                                       yaggr2_RANDflows_test_labels,
    #                                                                       )

    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr2_RANDflows_test_flows,
    #                                                                            yaggr2_RANDflows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    # #####################################################################
    
    # print("AGGREGATION-5 WITH RANDOM TRAFFIC")
    
    # ####################################################################
    # ##  THE CODE BELOW IS TO TEST THE TRAINED MODEL AGAINST TESTING DATA WITH AGGREGATION-5 FLOWS INSTALLED, CONTAINING ALSO
    # ##    RANDOM WEBISTE TRAFFIC IN ADDITION TO THE ONE WE ARE FINGERPRINTING
    # ##
    # #####################################################################

    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                                       y_train_labels,
    #                                                                       xaggr5_RANDflows_test_flows,
    #                                                                       yaggr5_RANDflows_test_labels,
    #                                                                       )

    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr5_RANDflows_test_flows,
    #                                                                            yaggr5_RANDflows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################


    # #####################################################################
    
    # print("AGGREGATION TESTING COMPLETE NOW TESTING AGAINST FLOWS WITH SPLIT")
    
    # ####################################################################
    # ##  THE CODE BELOW IS TO TEST THE TRAINED MODEL AGAINST TESTING DATA WITH SPLITTING FLOWS INSTALLED
    # ##
    # #####################################################################

    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                                       y_train_labels,
    #                                                                       xsplitflows_test_flows,
    #                                                                       ysplitflows_test_labels,
    #                                                                       )

    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################
    # # print(results)

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xsplitflows_test_flows,
    #                                                                            ysplitflows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################


    # #####################################################################
    
    # print("SPLIT TESTING ON ALL INTERFACE COMPLETE NOW TESTING AGAINST FLOWS WITH SPLIT BUT COLLECTED ON ONE INTERFACE ONLY")
    
    # ####################################################################
    # ##  THE CODE BELOW IS TO TEST THE TRAINED MODEL AGAINST TESTING DATA WITH SPLITTING FLOWS COLLECTED ON ONE INTERFACE INSTALLED
    # ##
    # #####################################################################
    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                                       y_train_labels,
    #                                                                       xsplit_oneinterface_flows_test_flows,
    #                                                                       ysplit_oneinterface_flows_test_labels,
    #                                                                       )

    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    # #####################################################################

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xsplit_oneinterface_flows_test_flows,
    #                                                                            ysplit_oneinterface_flows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # print(results)
    #####################################################################

    # print(results)
    

train_it()
#read_data_from_pickles(data_path_train)