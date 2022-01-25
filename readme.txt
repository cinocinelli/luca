mypreprocesingpktlens.py requires:

pcap file that don't contain dns queries appropriately labeled with the format "websitelabelwebpagelabel.pcap"
for example for traffic meant to be identified as the amazon home page the name of the file should be amazonhome.pcap.
If any new website is added to the pool, the website name should be added to the site_list list.

Train.py requires:
For all classifiers except Panchenho 16 and Herrmann, use the regular training data and testing data output by the function gen_label_to_pktsizes
in the mypreprocesingpktlens.py file.
In the panchenko 16 use training data and testing data extracted with the function gen_label_to_pktsizes_inverted,
for Herrmann gen_label_to_pktsizes_forherrmann

E.g
Liberatore runs on training data compressed_pickle_train.pzb2,compressed_pickle_test_waggr2_RANDflows.pzb2
Panchenko 16 runs on training data compressed_pickle_train_inverted.pzb2,compressed_pickle_test_waggr2_RANDflows_inv.pzb2
Herrmann runs on training data compressed_pickle_train_herman.pzb2,compressed_pickle_test_waggr2_RANDflows_her.pzb2

This because these classifiers take data that is processed slightly differently.


