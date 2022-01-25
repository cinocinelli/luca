from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime
import dpkt
import os
import pickle
import bz2
import socket
from scipy import stats
import numpy
import pandas
from collections import OrderedDict


#path_train = "S:/Webpage fingerprinter/datasets/flows-perwebpage-train/"
#path_train = "S:/Webpage fingerprinter/datasets/old-new-fused/"
#path_test = "S:/Webpage fingerprinter/datasets/flows-perwebpage-test/"
#path_train = "S:/Webpage fingerprinter/datasets/split-train-hostpair/"
#path_test = "S:/Webpage fingerprinter/datasets/split-test-hostpair/"
#path_train = "S:/Webpage fingerprinter/datasets/split-train-hostpair/"
#path_test = "S:/Webpage fingerprinter/datasets/split-test-hostpair/"
#path_test = "S:/Webpage fingerprinter/datasets/split-test-1sec/"
#path_train = "S:/Webpage fingerprinter/datasets/split-train-1sec/"
#path_test = "S:/Webpage fingerprinter/datasets/split-test-hostpair-samepktcount/"
#path_train = "S:/Webpage fingerprinter/datasets/split-train-hostpair-samepktcount/"
#path_test = "S:/Webpage fingerprinter/datasets/split-test-1sec-hostpair/"
#path_train = "S:/Webpage fingerprinter/datasets/split-train-1sec-hostpair/"
#path_test = "S:/Webpage fingerprinter/datasets/split-test-2sec-hostpair/"
#path_train = "S:/Webpage fingerprinter/datasets/split-train-2sec-hostpair/"
#path_test = "S:/Webpage fingerprinter/datasets/split-test-3sec-hostpair/"
#path_train = "S:/Webpage fingerprinter/datasets/split-train-3sec-hostpair/"
#path_wflows = "S:/Webpage fingerprinter/datasets/split-wflows-aggrs/"
#path_wflows = "S:/Webpage fingerprinter/datasets/split-wsplitflows-3sec-hostpair/"
#path_wflows = "S:/Webpage fingerprinter/datasets/split-testwsplitflows_one_interface_3sec_hostpair/"
#path_wflows = "S:/Webpage fingerprinter/datasets/split-aggr2flows_3sec_hostpair/"
path_wflows = "S:/Webpage fingerprinter/datasets/split-aggr5flowswrand_3sec_hostpair/"


site_list = ['amazon', 'bing','ebay','google','reddit', 'repubblica', 'stackoverflow','wikipedia', 'yahoo', 'youtube']
def gen_label_to_flow(namefilepcap):
    index_end_website_name = namefilepcap.index('.')
    label = namefilepcap[:index_end_website_name]
    return label

def gen_label_to_pktsizes(path_):
    label_to_vectors = []
    array_of_pkt_lens = []

    for file in os.listdir(path_):
        label = gen_label_to_flow(file)
        for l in site_list:
            if l in label:
                label = l

        for ts, pkt in dpkt.pcap.Reader(open(path_ + file,'rb')):
            eth_hdr = dpkt.ethernet.Ethernet(pkt) #ethernet header
            ip_hdr = 0
            ip_src_str = ''

            if eth_hdr.type != dpkt.ethernet.ETH_TYPE_ARP:
                ip_hdr = eth_hdr.data
                ip_src_str = socket.inet_ntoa(ip_hdr.src)
                tcp = ip_hdr.data


            if tcp.flags & dpkt.tcp.TH_RST or len(pkt) == 54 or eth_hdr.type == dpkt.ethernet.ETH_TYPE_ARP: #or len(pkt) >1515:
                continue
            if ip_src_str[0:7] == '10.0.0.':
                array_of_pkt_lens.append(len(pkt))
            if ip_src_str[0:7] != '10.0.0.':
                array_of_pkt_lens.append(-len(pkt))

        if len(array_of_pkt_lens) <=6: #if there are less then 6 packets in a tuple, ignore
            continue
        label_to_vectors.append((label, array_of_pkt_lens)) #[label] = [len_incoming_packets, len_outgoing_packets, len_both_packets]
        array_of_pkt_lens = []

    
    if "train" or "fused" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_train.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "wflows" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_wflows.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "test" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    
    if "aggr" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_waggr5_RANDflows.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)

    return label_to_vectors

def gen_label_to_pktsizes_inverted(path_):
    label_to_vectors = []
    array_of_pkt_lens = []

    for file in os.listdir(path_):

        label = gen_label_to_flow(file)
        for l in site_list:
            if l in label:
                label = l
        #print(label)
        for ts, pkt in dpkt.pcap.Reader(open(path_ + file,'rb')):

            eth_hdr = dpkt.ethernet.Ethernet(pkt) #ethernet header
            #arp_hdr = dpkt.arp.ARP(pkt)
            ip_hdr = 0
            ip_src_str = ''

            if eth_hdr.type != dpkt.ethernet.ETH_TYPE_ARP:
                ip_hdr = eth_hdr.data
                ip_src_str = socket.inet_ntoa(ip_hdr.src)
                tcp = ip_hdr.data
            #if eth.type==dpkt.ethernet.ETH_TYPE_ARP
            if tcp.flags & dpkt.tcp.TH_RST or len(pkt) == 54 or eth_hdr.type == dpkt.ethernet.ETH_TYPE_ARP : #or len(pkt) >1515:
                continue
            if ip_src_str[0:7] == '10.0.0.':
                array_of_pkt_lens.append(-len(pkt))
            if ip_src_str[0:7] != '10.0.0.':
                array_of_pkt_lens.append(len(pkt))

        if len(array_of_pkt_lens) <=6: #se ci sono meno di 20 pacchetti come feature del label non lo mettiamo
            continue
        label_to_vectors.append((label, array_of_pkt_lens)) #[label] = [len_incoming_packets, len_outgoing_packets, len_both_packets]
        array_of_pkt_lens = []

    #print(len(label_to_vectors[0][1]))
    #if "test" in path_:
        #compressed_pickle = bz2.BZ2File('compressed_pickle_test.pbz2', 'w')
        #pickle.dump(label_to_vectors, compressed_pickle)
    #elif path_.__contains__("train"):
    
    if "train" or "fused" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_train_inverted.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "wflows" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_wflows_inverted.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "test" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_inverted.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    
    if "aggr" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_waggr5_RANDflows_inv.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)


    return label_to_vectors
def gen_label_to_pktsizes_forhermann(path_):
    label_to_vectors = []
    array_of_pkt_lens = []

    for file in os.listdir(path_):

        label = gen_label_to_flow(file)
        for l in site_list:
            if l in label:
                label = l
        #print(label)
        for ts, pkt in dpkt.pcap.Reader(open(path_ + file,'rb')):

            eth_hdr = dpkt.ethernet.Ethernet(pkt) #ethernet header
            ip_hdr = 0
            ip_src_str = ''

            if eth_hdr.type != dpkt.ethernet.ETH_TYPE_ARP:
                ip_hdr = eth_hdr.data
                ip_src_str = socket.inet_ntoa(ip_hdr.src)
                tcp = ip_hdr.data
            if tcp.flags & dpkt.tcp.TH_RST or len(pkt) >1515 or eth_hdr.type == dpkt.ethernet.ETH_TYPE_ARP: #or len(pkt) == 54 or len(pkt) >1515:
                continue
            if (ip_src_str[0:7] == '10.0.0.'):
                array_of_pkt_lens.append(len(pkt))
            if (ip_src_str[0:7] != '10.0.0.'):
                array_of_pkt_lens.append(-len(pkt))

        if len(array_of_pkt_lens) <=20: #se ci sono meno di 20 pacchetti come feature del label non lo mettiamo
            continue
        label_to_vectors.append((label, array_of_pkt_lens)) #[label] = [len_incoming_packets, len_outgoing_packets, len_both_packets]
        array_of_pkt_lens = []

    #print(len(label_to_vectors[0][1]))
    
    if "test" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_herman.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    #elif path_.__contains__("train"):
    if "train" or "fused" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_train_herman.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "wflows" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_wflows_herman.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    
    if "aggr" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_waggr5_RANDflows_her.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    return label_to_vectors


path_test = "S:/Webpage fingerprinter/datasets/split-test-3sec-hostpair/"
path_train = "S:/Webpage fingerprinter/datasets/split-train-3sec-hostpair/"
path_test_flows = "S:/Webpage fingerprinter/datasets/split-wflows-aggrs/"

#gen_label_to_pktsizes(path_test)
#gen_label_to_pktsizes(path_train)
#gen_label_to_pktsizes_forhermann(path_train)
#gen_label_to_pktsizes_forhermann(path_test)
#gen_label_to_pktsizes_inverted(path_test)
#gen_label_to_pktsizes_inverted(path_train)
#gen_label_to_pktsizes(path_flows)
#gen_label_to_pktsizes_inverted(path_wflows)
#gen_label_to_pktsizes_forhermann(path_wflows)


#gen_label_to_pktsizes(path_test_flows)
#gen_label_to_pktsizes_inverted(path_test)
#gen_label_to_pktsizes_inverted(path_train)
#gen_label_to_pktsizes_inverted(path_test_flows)
#gen_label_to_pktsizes_forhermann(path_train)
#gen_label_to_pktsizes_forhermann(path_test)
#gen_label_to_pktsizes_forhermann(path_test_flows)

gen_label_to_pktsizes(path_wflows)
gen_label_to_pktsizes_inverted(path_wflows)
gen_label_to_pktsizes_forhermann(path_wflows)

