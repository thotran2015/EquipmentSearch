#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 08:29:16 2018

@author: thotran
"""
from scraping import used_line, sci_bay
from scraping import dotmed, ebay, biosurplus, daigger, labcommerce, labx, google, equipnet, eurekaspot, \
    marshallscientific, medwow, newlifescientific, sibgene
import numpy as np
import multiprocessing as multi


def chunks(n, links):
    return np.array_split(links, n)


# use this number of CPUs for number of processes in the pool
cpus = multi.cpu_count()
workers = []
NEW_FUNCS = [daigger.extract_results,
             dotmed.extract_results,
             ebay.extract_results,
             google.extract_results,
             labx.extract_results,
             medwow.extract_results,
             sibgene.extract_results
             ]

WEBSITE_NAMES = {ebay.extract_results: "ebay", equipnet.extract_results: "equipnet", google.extract_results: "google",
                 used_line.extract_results: "used line",
                 eurekaspot.extract_results: "eurekaspot", labcommerce.extract_results: "labcommerce",
                 newlifescientific.extract_results: "newlifescientific", biosurplus.extract_results: "biosurplus",
                 sci_bay.extract_results: "sci_bay",
                 dotmed.extract_results: "dotmed", sibgene.extract_results: "sibgene", labx.extract_results: "labx",
                 medwow.extract_results: "medwow", marshallscientific.extract_results:
                     "marshallscientific", daigger.extract_results: "daigger"}

page_bins = chunks(cpus, NEW_FUNCS)
print(cpus)
# for cpu in range(cpus):
#    sys.stdout.write("CPU"+str(cpu) + "\n")
#    #Process that sends a list of pages to the extract func
#    worker = multi.Process(name =str(cpu), target = )
