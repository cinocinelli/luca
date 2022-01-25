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
import shutil

path_train = "./datasets/flows-perwebpage-train/"
path_test = "./datasets/flows-perwebpage-test/"
#path_train = "S:/Webpage fingerprinter/datasets/old-new-fused/"

path_wrong_train = './datasets/trainwrongpcap/'
path_wrong_test = './datasets/testwrongpcap/'

path_s_train = './datasets/trainsmall/'
path_s_test = './datasets/testsmall/'
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
# path_wflows = "S:/Webpage fingerprinter/datasets/split-aggr5flowswrand_3sec_hostpair/"


# site_list = ['amazon', 'bing','ebay','google','reddit', 'repubblica', 'stackoverflow','wikipedia', 'yahoo', 'youtube']
site_list = ['dianxiaomi.com', '25pp.com', 'vvvdj.com', 'panduoduo.net', 'winit.com.cn', 'jizhangla.com', 'tongtool.com', 'xianshiw.com', 'ih5.cn', 'w7000.com', 'jia400.com', 'i4.cn', 'aipai.com', 'pcauto.com.cn', '61learn.com', 'china360.cn', 'hea.cn', 'cnfla.com', 'yiihuu.com', 'tapd.cn', 'ijianji.com', 'sz.gov.cn', 'oschina.net', 'kugou.com', 'maigoo.com', 'sznews.com', 'rcfans.com', 'vip.com', '4px.com', '11467.com', 'genban.org', 'findlaw.cn', 'icourse163.org', 'meizu.com', 'ofweek.com', 'juooo.com', 'topfo.com', '120ask.com', '163.com', 'cnad.com', 'lamabang.com', '5118.com', '126.com', 'pcbaby.com.cn', 'myqcloud.com', 'juzimi.com', 'rabbitpre.com', 'flyme.cn', 'kuaidi100.com', 'mfisp.com', 'uc.cn', 'coding.net', 'fzg360.com', 'yunzhijia.com', 'hrloo.com', 'chuansong.me', '3gmfw.cn', 'feng.com', 'mob.com', 'myzaker.com', 'yunexpress.com', 'wpjam.com', 'kingtrans.cn', 'vivo.com.cn', 'cmbchina.com', 'ca168.com', 'bochk.com', 'chuandong.com', 'netease.com', 'qeqeqe.com', 'seowhy.com', 'home77.com', 'eccn.com', 'sztb.gov.cn', 'tradezz.com', 'pconline.com.cn', 'zhujiceping.com', 'seedit.com', 'taojindi.com', 'caichongwang.com', 'sm.cn', 'cps.com.cn', 'iciba.com', 'tencent.com', 'cheshen.cn', 'kankanwu.com', '500.com', 'xiaodaoxing.com', '51.la', 'jobui.com', 'ca800.com', 'sf-express.com', 'elecfans.com', 'leiphone.com', '8684.cn', 'ylsw.com', 'szu.edu.cn', '51dzw.com', 'geihui.com', 'webkaka.com']
def gen_label_to_flow(namefilepcap):
    index_end_website_name = namefilepcap.index('.pcap')
    label = namefilepcap[:index_end_website_name]
    return label

def gen_label_to_pktsizes(path_,w_path):
    label_to_vectors = []
    array_of_pkt_lens = []
    exset = set()
    exdic = dict()
    for file in os.listdir(path_):        
        print(file)
        
        try:
            label = gen_label_to_flow(file)
            for l in site_list:
                if l in label:
                    label = l

            # just use tcp
            
            # Skip if it is not an IP packet
            
            for ts, pkt in dpkt.pcap.Reader(open(path_ + file,'rb')):
                eth_hdr = dpkt.ethernet.Ethernet(pkt) #ethernet header
                ip_hdr = 0
                ip_src_str = ''
                
                if eth_hdr.type!=dpkt.ethernet.ETH_TYPE_IP:
                    print('skip - not ETH_TYPE_IP ')
                    continue
                
                if eth_hdr.type != dpkt.ethernet.ETH_TYPE_ARP:
                    ip_hdr = eth_hdr.data
                    
                    if ip_hdr.p!=dpkt.ip.IP_PROTO_TCP:
                        print('skip - not IP_PROTO_TCP ')
                        continue
                    
                    
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
        except Exception as e :
            # shutil.move(path_ + file,w_path + file)
            if str(e) in exdic.keys():
                exdic[str(e)].append(file)
            else:
                exdic[str(e)] = [file]
            exset.add(str(e))
            print(str(e))
    print(exset)
    for k in exdic.keys():
        print(k)
        print(exdic[k])
    
    if "train" or "fused" in path_:
        # compressed_pickle = bz2.BZ2File('compressed_pickle_train.pbz2', 'w')
        compressed_pickle = bz2.BZ2File('wangs_compressed_pickle_train.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "wflows" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_wflows.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "test" in path_:
        compressed_pickle = bz2.BZ2File('wangs_compressed_pickle_test.pbz2', 'w')
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
        compressed_pickle = bz2.BZ2File('wang_compressed_pickle_train_inverted.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "wflows" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_wflows_inverted.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "test" in path_:
        compressed_pickle = bz2.BZ2File('wang_compressed_pickle_test_inverted.pbz2', 'w')
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
        compressed_pickle = bz2.BZ2File('wang_compressed_pickle_test_herman.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    #elif path_.__contains__("train"):
    if "train" or "fused" in path_:
        compressed_pickle = bz2.BZ2File('wang_compressed_pickle_train_herman.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    if "wflows" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_wflows_herman.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    
    if "aggr" in path_:
        compressed_pickle = bz2.BZ2File('compressed_pickle_test_waggr5_RANDflows_her.pbz2', 'w')
        pickle.dump(label_to_vectors, compressed_pickle)
    return label_to_vectors


# path_test = "S:/Webpage fingerprinter/datasets/split-test-3sec-hostpair/"
# path_train = "S:/Webpage fingerprinter/datasets/split-train-3sec-hostpair/"
# path_test_flows = "S:/Webpage fingerprinter/datasets/split-wflows-aggrs/"

# gen_label_to_pktsizes(path_test,path_wrong_test)
# gen_label_to_pktsizes(path_train,path_wrong_train)

gen_label_to_pktsizes(path_s_test,path_wrong_test)
gen_label_to_pktsizes(path_s_train,path_wrong_train)



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

# gen_label_to_pktsizes(path_wflows)
# gen_label_to_pktsizes_inverted(path_wflows)
# gen_label_to_pktsizes_forhermann(path_wflows)

