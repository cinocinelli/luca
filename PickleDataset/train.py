import pickle
import bz2
import cPickle
import sys

sys.path.append("..")
import classifiers
import warnings
import numpy

data_path_train = './compressed_pickle_train.pbz2'
data_path_train_her = './compressed_pickle_train_herman.pbz2'
data_path_train_inv = './compressed_pickle_train_inverted.pbz2'

data_path_test = './compressed_pickle_test.pbz2'
data_path_test_her = './compressed_pickle_test_herman.pbz2'
data_path_test_inv = './compressed_pickle_test_inverted.pbz2'

############    this data is not good   ####################################################################################
#data_path_test_waggr7flows = './compressed_pickle_test_waggr7flows.pbz2'
#data_path_test_waggr7flows_inv = './compressed_pickle_test_waggr7flows_inverted.pbz2'
#data_path_test_waggr7flows_her = './compressed_pickle_test_waggr7flows_herman.pbz2'
########################################################################################################################

data_path_test_wsplitflows = './compressed_pickle_test_wsplitflows.pbz2'
data_path_test_wsplitflows_inv = './compressed_pickle_test_wsplitflows_inverted.pbz2'
data_path_test_wsplitflows_her = './compressed_pickle_test_wsplitflows_herman.pbz2'

data_path_test_wsplit_oneinterface_flows = './compressed_pickle_test_wsplitflows_oneinterface.pbz2'
data_path_test_wsplit_oneinterface_flows_inv = './compressed_pickle_test_wsplitflows_oneinterface_inv.pbz2'
data_path_test_wsplit_oneinterface_flows_her = './compressed_pickle_test_wsplitflows_oneinterface_her.pbz2'


data_path_test_waggr2flows = './compressed_pickle_test_waggr2flows.pbz2'
data_path_test_waggr2flows_inv = './compressed_pickle_test_waggr2flows_inv.pbz2'
data_path_test_waggr2flows_her = './compressed_pickle_test_waggr2flows_her.pbz2'

data_path_test_waggr5flows = './compressed_pickle_test_waggr5flows.pbz2'
data_path_test_waggr5flows_inv = './compressed_pickle_test_waggr5flows_inv.pbz2'
data_path_test_waggr5flows_her = './compressed_pickle_test_waggr5flows_her.pbz2'


data_path_test_waggr2_RANDflows = './compressed_pickle_test_waggr2_RANDflows.pbz2'
data_path_test_waggr2_RANDflows_inv = './compressed_pickle_test_waggr2_RANDflows_inv.pbz2'
data_path_test_waggr2_RANDflows_her = './compressed_pickle_test_waggr2_RANDflows_her.pbz2'

data_path_test_waggr5_RANDflows = './compressed_pickle_test_waggr5_RANDflows.pbz2'
data_path_test_waggr5_RANDflows_inv = './compressed_pickle_test_waggr5_RANDflows_inv.pbz2'
data_path_test_waggr5_RANDflows_her = './compressed_pickle_test_waggr5_RANDflows_her.pbz2'




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
    print("x_train_flows, y_train_labels")
    print(len(x_train_flows), len(y_train_labels))
    # remove comments here to test normal data without flows (for all other classifiers except herrmann and Panchenko16
    x_test_flows, y_test_labels = read_data_from_pickles(data_path_test) #data_path_test
    print("x_train_flows, y_train_labels")
    print(len(x_test_flows), len(y_test_labels) )

    #train and test normal traffic for herman
    xh_train_flows, yh_train_labels = read_data_from_pickles(data_path_train_her)
    print("xh_train_flows, yh_train_labels ")
    print(len(xh_train_flows), len(yh_train_labels) )
    # remove comments here to test normal data without flows collected for herrmann classifier(for herrmann)
    xh_test_flows, yh_test_labels = read_data_from_pickles(data_path_test_her)
    print("xh_test_flows, yh_test_labels")
    print(len(xh_test_flows), len(yh_test_labels))

    # train and test normal traffic for pachenko
    xinv_train_flows, yinv_train_labels = read_data_from_pickles(data_path_train_inv)
    print("xinv_train_flows, yinv_train_labels")
    print(len(xinv_train_flows), len(yinv_train_labels))
    # remove comments here to test normal data without flows collected by inverting direction (for pachenko 16)
    xinv_test_flows, yinv_test_labels = read_data_from_pickles(data_path_test_inv)
    print("xinv_test_flows, yinv_test_labels")
    print(len(xinv_test_flows), len(yinv_test_labels))

    # remove comments here to test with aggregation-7 flows data not good
    #xaggr7flows_test_flows, yaggr7flows_test_labels = read_data_from_pickles(data_path_test_waggr7flows)
    #xaggr7flowsinv_test_flows, yaggr7flowsinv_test_labels = read_data_from_pickles(data_path_test_waggr7flows_inv)
    #xaggr7flowsh_test_flows, yaggr7flowsh_test_labels = read_data_from_pickles(data_path_test_waggr7flows_her)
    # remove comments here to test with split flows collected on all interfaces
    xsplitflows_test_flows, ysplitflows_test_labels = read_data_from_pickles(data_path_test_wsplitflows)
    print("xsplitflows_test_flows, ysplitflows_test_labels")
    print(len(xsplitflows_test_flows), len(ysplitflows_test_labels))
    xsplitflowsinv_test_flows, ysplitflowsinv_test_labels = read_data_from_pickles(data_path_test_wsplitflows_inv)
    print("xsplitflowsinv_test_flows, ysplitflowsinv_test_labels")
    print(len(xsplitflowsinv_test_flows), len(ysplitflowsinv_test_labels))
    xsplitflowsh_test_flows, ysplitflowsh_test_labels = read_data_from_pickles(data_path_test_wsplitflows_her)
    print("xsplitflowsh_test_flows, ysplitflowsh_test_labels")
    print(len(xsplitflowsh_test_flows), len(ysplitflowsh_test_labels))
    # remove comments here to test with split flows collected on one interface
    xsplit_oneinterface_flows_test_flows, ysplit_oneinterface_flows_test_labels = read_data_from_pickles(data_path_test_wsplit_oneinterface_flows)
    print("xsplit_oneinterface_flows_test_flows, ysplit_oneinterface_flows_test_labels")
    print(len(xsplit_oneinterface_flows_test_flows), len(ysplit_oneinterface_flows_test_labels))
    xsplit_oneinterface_flowsinv_test_flows, ysplit_oneinterface_flowsinv_test_labels = read_data_from_pickles(data_path_test_wsplit_oneinterface_flows_inv)
    print("xsplit_oneinterface_flowsinv_test_flows, ysplit_oneinterface_flowsinv_test_labels")
    print(len(xsplit_oneinterface_flowsinv_test_flows), len(ysplit_oneinterface_flowsinv_test_labels))
    xsplit_oneinterface_flowsh_test_flows, ysplit_oneinterface_flowsh_test_labels = read_data_from_pickles(data_path_test_wsplit_oneinterface_flows_her)
    print("xsplit_oneinterface_flowsh_test_flows, ysplit_oneinterface_flowsh_test_labels")
    print(len(xsplit_oneinterface_flowsh_test_flows), len(ysplit_oneinterface_flowsh_test_labels))
    # remove comments here to test with aggregation-2 flows
    xaggr2flows_test_flows, yaggr2flows_test_labels = read_data_from_pickles(data_path_test_waggr2flows)
    print("xaggr2flows_test_flows, yaggr2flows_test_labels")
    print(len(xaggr2flows_test_flows), len(yaggr2flows_test_labels))
    xaggr2flowsinv_test_flows, yaggr2flowsinv_test_labels = read_data_from_pickles(data_path_test_waggr2flows_inv)
    print("xaggr2flowsinv_test_flows, yaggr2flowsinv_test_labels ")
    print(len(xaggr2flowsinv_test_flows), len(yaggr2flowsinv_test_labels) )
    xaggr2flowsh_test_flows, yaggr2flowsh_test_labels = read_data_from_pickles(data_path_test_waggr2flows_her)
    print("xaggr2flowsh_test_flows, yaggr2flowsh_test_labels")
    print(len(xaggr2flowsh_test_flows), len(yaggr2flowsh_test_labels))
    # remove comments here to test with aggregation-5 flows
    xaggr5flows_test_flows, yaggr5flows_test_labels = read_data_from_pickles(data_path_test_waggr5flows)
    print("xaggr5flows_test_flows, yaggr5flows_test_labels")
    print(len(xaggr5flows_test_flows), len(yaggr5flows_test_labels))
    xaggr5flowsinv_test_flows, yaggr5flowsinv_test_labels = read_data_from_pickles(data_path_test_waggr5flows_inv)
    print("xaggr5flowsinv_test_flows, yaggr5flowsinv_test_labels")
    print(len(xaggr5flowsinv_test_flows), len(yaggr5flowsinv_test_labels))
    xaggr5flowsh_test_flows, yaggr5flowsh_test_labels = read_data_from_pickles(data_path_test_waggr5flows_her)
    print("xaggr5flowsh_test_flows, yaggr5flowsh_test_labels")
    print(len(xaggr5flowsh_test_flows), len(yaggr5flowsh_test_labels))
    # remove comments here to test with aggregation-2 flows with random traffic
    xaggr2_RANDflows_test_flows, yaggr2_RANDflows_test_labels = read_data_from_pickles(data_path_test_waggr2_RANDflows)
    print("xaggr2_RANDflows_test_flows, yaggr2_RANDflows_test_labels")
    print(len(xaggr2_RANDflows_test_flows), len(yaggr2_RANDflows_test_labels))
    xaggr2_RANDflowsinv_test_flows, yaggr2_RANDflowsinv_test_labels = read_data_from_pickles(data_path_test_waggr2_RANDflows_inv)
    print("xaggr2_RANDflowsinv_test_flows, yaggr2_RANDflowsinv_test_labels ")
    print(len(xaggr2_RANDflowsinv_test_flows), len(yaggr2_RANDflowsinv_test_labels) )
    xaggr2_RANDflowsh_test_flows, yaggr2_RANDflowsh_test_labels = read_data_from_pickles(data_path_test_waggr2_RANDflows_her)
    print("xaggr2_RANDflowsh_test_flows, yaggr2_RANDflowsh_test_labels")
    print(len(xaggr2_RANDflowsh_test_flows), len(yaggr2_RANDflowsh_test_labels))
    # remove comments here to test with aggregation-5 flows with random traffic
    xaggr5_RANDflows_test_flows, yaggr5_RANDflows_test_labels = read_data_from_pickles(data_path_test_waggr5_RANDflows)
    print("xaggr5_RANDflows_test_flows, yaggr5_RANDflows_test_labels")
    print(len(xaggr5_RANDflows_test_flows), len(yaggr5_RANDflows_test_labels))
    xaggr5_RANDflowsinv_test_flows, yaggr5_RANDflowsinv_test_labels = read_data_from_pickles(data_path_test_waggr5_RANDflows_inv)
    print("xaggr5_RANDflowsinv_test_flows, yaggr5_RANDflowsinv_test_labels ")
    print(len(xaggr5_RANDflowsinv_test_flows), len(yaggr5_RANDflowsinv_test_labels) )
    xaggr5_RANDflowsh_test_flows, yaggr5_RANDflowsh_test_labels = read_data_from_pickles(data_path_test_waggr5_RANDflows_her)
    print("xaggr5_RANDflowsh_test_flows, yaggr5_RANDflowsh_test_labels")
    print(len(xaggr5_RANDflowsh_test_flows), len(yaggr5_RANDflowsh_test_labels))

    
    ####################################################################
    ##  THE CODE BELOW NEEDS NORMAL DATA TO FUNCTION
    ##  TRAINING AND TESTING ON NON AGGREGATED FLOWS
    #####################################################################
    
# #####################################################################
    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                           y_train_labels,
    #                                                           x_test_flows,
    #                                                           y_test_labels,
    #                                                           )
    
    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    
    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                y_train_labels,
    #                                                                x_test_flows,
    #                                                                y_test_labels,
    #                                                                )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2011"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.panchenko_2011.classifier_panchenko2011(x_train_flows,
    #                                                                      y_train_labels,
    #                                                                      x_test_flows,
    #                                                                      y_test_labels,
    #                                                                      )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # can run 
    #####################################################################
    # classifier_name = "dyer_2012_notime"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.dyer_2012.classifier_dyer2012(x_train_flows,
    #                                                            y_train_labels,
    #                                                            x_test_flows,
    #                                                            y_test_labels,
    #                                                            time_train=None,
    #                                                            time_test=None
    #                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    #####################################################################
    

    # herrman_2009
    ####################################################################
    # cos_ = [True, False]
    # norm_ = [True, False]
    # TF_ = [True, False]
    # for c in cos_:
    #     for n in norm_:
    #         for tf in TF_:
    #             classifier_name = "herrman_2009_TF_%s__cos_%s__norm_%s" % (tf, c, n)  ##TESTED
    #             print("running", classifier_name)
    #             y_test, y_pred = classifiers.herrman_2009.classifier_herrman2009(xh_train_flows,
    #                                                                              yh_train_labels,
    #                                                                              xh_test_flows,
    #                                                                              yh_test_labels,
    #                                                                              cos_=c, TF_=tf, norm=n
    #                                                                              )
    #             results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2016"
    # print("running", classifier_name)

    # y_test, y_pred = classifiers.panchenko_2016.classifier_panchenko2016(xinv_train_flows,
    #                                                                      yinv_train_labels,
    #                                                                      xinv_test_flows,
    #                                                                      yinv_test_labels,
    #                                                                      )

    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################
    # 
    # print("TRAINING COMPLETE NOW TESTING AGAINST FLOWS WITH AGGREGATION")
    # print("AGGREGATION-2 TESTING")
    # ####################################################################
    # ##  THE CODE BELOW IS TO TEST THE TRAINED MODEL AGAINST TESTING DATA WITH AGGR-2 FLOWS INSTALLED
    # ##
    # #####################################################################
    # 
    # classifier_name = "liberatoreNB2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_NB(x_train_flows,
    #                                                                       y_train_labels,
    #                                                                       xaggr2flows_test_flows,
    #                                                                       yaggr2flows_test_labels,
    #                                                                       )

    # results = classifiers.common_utils.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################
    # # print(results)

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr2flows_test_flows,
    #                                                                            yaggr2flows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2011"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.panchenko_2011.classifier_panchenko2011(x_train_flows,
    #                                                                      y_train_labels,
    #                                                                      xaggr2flows_test_flows,
    #                                                                      yaggr2flows_test_labels,
    #                                                                      )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    

    # #####################################################################
    # classifier_name = "dyer_2012_notime"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.dyer_2012.classifier_dyer2012(x_train_flows,
    #                                                            y_train_labels,
    #                                                            xaggr2flows_test_flows,
    #                                                            yaggr2flows_test_labels,
    #                                                            time_train=None,
    #                                                            time_test=None
    #                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################
    
    # classifier_name = "panchenko_2016"
    # print("running", classifier_name)

    # y_test, y_pred = classifiers.panchenko_2016.classifier_panchenko2016(xinv_train_flows,
    #                                                                      yinv_train_labels,
    #                                                                      xaggr2flowsinv_test_flows,
    #                                                                      yaggr2flowsinv_test_labels,
    #                                                                      )

    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    
    # #####################################################################

    # cos_ = [True, False]
    # norm_ = [True, False]
    # TF_ = [True, False]
    # for c in cos_:
    #     for n in norm_:
    #         for tf in TF_:
    #             classifier_name = "herrman_2009_TF_%s__cos_%s__norm_%s" % (tf, c, n)  ##TESTED
    #             print("running", classifier_name)
    #             y_test, y_pred = classifiers.herrman_2009.classifier_herrman2009(xh_train_flows,
    #                                                                              yh_train_labels,
    #                                                                              xaggr2flowsh_test_flows,
    #                                                                              yaggr2flowsh_test_labels,
    #                                                                              cos_=c, TF_=tf, norm=n
    #                                                                              )
    #             results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################
    # 
    # print("AGGREGATION-5 TESTING")
    # 
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
    # #####################################################################
    # # print(results)

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr5flows_test_flows,
    #                                                                            yaggr5flows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2011"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.panchenko_2011.classifier_panchenko2011(x_train_flows,
    #                                                                      y_train_labels,
    #                                                                      xaggr5flows_test_flows,
    #                                                                      yaggr5flows_test_labels,
    #                                                                      )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################



    # #####################################################################
    # classifier_name = "dyer_2012_notime"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.dyer_2012.classifier_dyer2012(x_train_flows,
    #                                                            y_train_labels,
    #                                                            xaggr5flows_test_flows,
    #                                                            yaggr5flows_test_labels,
    #                                                            time_train=None,
    #                                                            time_test=None
    #                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # classifier_name = "panchenko_2016"
    # print("running", classifier_name)

    # y_test, y_pred = classifiers.panchenko_2016.classifier_panchenko2016(xinv_train_flows,
    #                                                                      yinv_train_labels,
    #                                                                      xaggr5flowsinv_test_flows,
    #                                                                      yaggr5flowsinv_test_labels,
    #                                                                      )

    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################

    # cos_ = [True, False]
    # norm_ = [True, False]
    # TF_ = [True, False]
    # for c in cos_:
    #     for n in norm_:
    #         for tf in TF_:
    #             classifier_name = "herrman_2009_TF_%s__cos_%s__norm_%s" % (tf, c, n)  ##TESTED
    #             print("running", classifier_name)
    #             y_test, y_pred = classifiers.herrman_2009.classifier_herrman2009(xh_train_flows,
    #                                                                              yh_train_labels,
    #                                                                              xaggr5flowsh_test_flows,
    #                                                                              yaggr5flowsh_test_labels,
    #                                                                              cos_=c, TF_=tf, norm=n
    #                                                                              )
    #             results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################
    # 
    # print("AGGREGATION-2 WITH RANDOM TRAFFIC")
    # 
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
    # #####################################################################
    # # print(results)

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr2_RANDflows_test_flows,
    #                                                                            yaggr2_RANDflows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2011"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.panchenko_2011.classifier_panchenko2011(x_train_flows,
    #                                                                      y_train_labels,
    #                                                                      xaggr2_RANDflows_test_flows,
    #                                                                      yaggr2_RANDflows_test_labels,
    #                                                                      )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "dyer_2012_notime"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.dyer_2012.classifier_dyer2012(x_train_flows,
    #                                                            y_train_labels,
    #                                                            xaggr2_RANDflows_test_flows,
    #                                                            yaggr2_RANDflows_test_labels,
    #                                                            time_train=None,
    #                                                            time_test=None
    #                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # classifier_name = "panchenko_2016"
    # print("running", classifier_name)

    # y_test, y_pred = classifiers.panchenko_2016.classifier_panchenko2016(xinv_train_flows,
    #                                                                      yinv_train_labels,
    #                                                                      xaggr2_RANDflowsinv_test_flows,
    #                                                                      yaggr2_RANDflowsinv_test_labels,
    #                                                                      )

    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################

    # cos_ = [True, False]
    # norm_ = [True, False]
    # TF_ = [True, False]
    # for c in cos_:
    #     for n in norm_:
    #         for tf in TF_:
    #             classifier_name = "herrman_2009_TF_%s__cos_%s__norm_%s" % (tf, c, n)  ##TESTED
    #             print("running", classifier_name)
    #             y_test, y_pred = classifiers.herrman_2009.classifier_herrman2009(xh_train_flows,
    #                                                                              yh_train_labels,
    #                                                                              xaggr2_RANDflowsh_test_flows,
    #                                                                              yaggr2_RANDflowsh_test_labels,
    #                                                                              cos_=c, TF_=tf, norm=n
    #                                                                              )
    #             results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################
    # 
    # print("AGGREGATION-5 WITH RANDOM TRAFFIC")
    # 
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
    # #####################################################################
    # # print(results)

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xaggr5_RANDflows_test_flows,
    #                                                                            yaggr5_RANDflows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2011"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.panchenko_2011.classifier_panchenko2011(x_train_flows,
    #                                                                      y_train_labels,
    #                                                                      xaggr5_RANDflows_test_flows,
    #                                                                      yaggr5_RANDflows_test_labels,
    #                                                                      )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "dyer_2012_notime"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.dyer_2012.classifier_dyer2012(x_train_flows,
    #                                                            y_train_labels,
    #                                                            xaggr5_RANDflows_test_flows,
    #                                                            yaggr5_RANDflows_test_labels,
    #                                                            time_train=None,
    #                                                            time_test=None
    #                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # classifier_name = "panchenko_2016"
    # print("running", classifier_name)

    # y_test, y_pred = classifiers.panchenko_2016.classifier_panchenko2016(xinv_train_flows,
    #                                                                      yinv_train_labels,
    #                                                                      xaggr5_RANDflowsinv_test_flows,
    #                                                                      yaggr5_RANDflowsinv_test_labels,
    #                                                                      )

    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################

    # cos_ = [True, False]
    # norm_ = [True, False]
    # TF_ = [True, False]
    # for c in cos_:
    #     for n in norm_:
    #         for tf in TF_:
    #             classifier_name = "herrman_2009_TF_%s__cos_%s__norm_%s" % (tf, c, n)  ##TESTED
    #             print("running", classifier_name)
    #             y_test, y_pred = classifiers.herrman_2009.classifier_herrman2009(xh_train_flows,
    #                                                                              yh_train_labels,
    #                                                                              xaggr5_RANDflowsh_test_flows,
    #                                                                              yaggr5_RANDflowsh_test_labels,
    #                                                                              cos_=c, TF_=tf, norm=n
    #                                                                              )
    #             results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################
    # 
    # print("AGGREGATION TESTING COMPLETE NOW TESTING AGAINST FLOWS WITH SPLIT")
    # 
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
    # #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2011"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.panchenko_2011.classifier_panchenko2011(x_train_flows,
    #                                                                      y_train_labels,
    #                                                                      xsplitflows_test_flows,
    #                                                                      ysplitflows_test_labels,
    #                                                                      )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################



    # #####################################################################
    # classifier_name = "dyer_2012_notime"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.dyer_2012.classifier_dyer2012(x_train_flows,
    #                                                            y_train_labels,
    #                                                            xsplitflows_test_flows,
    #                                                            ysplitflows_test_labels,
    #                                                            time_train=None,
    #                                                            time_test=None
    #                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # classifier_name = "panchenko_2016"
    # print("running", classifier_name)

    # y_test, y_pred = classifiers.panchenko_2016.classifier_panchenko2016(xinv_train_flows,
    #                                                                      yinv_train_labels,
    #                                                                      xsplitflowsinv_test_flows,
    #                                                                      ysplitflowsinv_test_labels,
    #                                                                      )

    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################

    # cos_ = [True, False]
    # norm_ = [True, False]
    # TF_ = [True, False]
    # for c in cos_:
    #     for n in norm_:
    #         for tf in TF_:
    #             classifier_name = "herrman_2009_TF_%s__cos_%s__norm_%s" % (tf, c, n)  ##TESTED
    #             print("running", classifier_name)
    #             y_test, y_pred = classifiers.herrman_2009.classifier_herrman2009(xh_train_flows,
    #                                                                              yh_train_labels,
    #                                                                              xsplitflowsh_test_flows,
    #                                                                              ysplitflowsh_test_labels,
    #                                                                              cos_=c, TF_=tf, norm=n
    #                                                                              )
    #             results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################
    # 
    # print("SPLIT TESTING ON ALL INTERFACE COMPLETE NOW TESTING AGAINST FLOWS WITH SPLIT BUT COLLECTED ON ONE INTERFACE ONLY")
    # 
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
    # #####################################################################
    # # print(results)

    # #####################################################################
    # classifier_name = "liberatoreJaccard2006"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.liberatore_2006.classifier_liberatore_jaccard(x_train_flows,
    #                                                                            y_train_labels,
    #                                                                            xsplit_oneinterface_flows_test_flows,
    #                                                                            ysplit_oneinterface_flows_test_labels,
    #                                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "panchenko_2011"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.panchenko_2011.classifier_panchenko2011(x_train_flows,
    #                                                                      y_train_labels,
    #                                                                      xsplit_oneinterface_flows_test_flows,
    #                                                                      ysplit_oneinterface_flows_test_labels,
    #                                                                      )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # #####################################################################
    # classifier_name = "dyer_2012_notime"
    # print("running", classifier_name)
    # y_test, y_pred = classifiers.dyer_2012.classifier_dyer2012(x_train_flows,
    #                                                            y_train_labels,
    #                                                            xsplit_oneinterface_flows_test_flows,
    #                                                            ysplit_oneinterface_flows_test_labels,
    #                                                            time_train=None,
    #                                                            time_test=None
    #                                                            )
    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)
    # #####################################################################

    # classifier_name = "panchenko_2016"
    # print("running", classifier_name)

    # y_test, y_pred = classifiers.panchenko_2016.classifier_panchenko2016(xinv_train_flows,
    #                                                                      yinv_train_labels,
    #                                                                      xsplit_oneinterface_flowsinv_test_flows,
    #                                                                      ysplit_oneinterface_flowsinv_test_labels,
    #                                                                      )

    # results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    # #####################################################################

    # cos_ = [True, False]
    # norm_ = [True, False]
    # TF_ = [True, False]
    # for c in cos_:
    #     for n in norm_:
    #         for tf in TF_:
    #             classifier_name = "herrman_2009_TF_%s__cos_%s__norm_%s" % (tf, c, n)  ##TESTED
    #             print("running", classifier_name)
    #             y_test, y_pred = classifiers.herrman_2009.classifier_herrman2009(xh_train_flows,
    #                                                                              yh_train_labels,
    #                                                                              xsplit_oneinterface_flowsh_test_flows,
    #                                                                              ysplit_oneinterface_flowsh_test_labels,
    #                                                                              cos_=c, TF_=tf, norm=n
    #                                                                              )
    #             results = classifiers.get_results(results, 'my dataset', classifier_name, y_test, y_pred, results_file)

    #####################################################################
    print(results)
    

train_it()
#read_data_from_pickles(data_path_train)