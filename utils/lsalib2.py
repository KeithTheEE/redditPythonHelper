#!/usr/bin/env python

import os
import sys
import numpy
import math 
from sklearn.decomposition import NMF
import logging


'''  
Keith Murray 
email: kmurrayis@gmail.com

lsalib
'''
class termDocMatrix(object):
    def __init__(self, saveVerbose=True, wcThreshold=2, parseOn=" "):
        # Get term-document matrix
        # transormation/modified weighting of term-doc matrix 
        # dimensionality reduction
        # clustering of documents in reduced space
        self.wcThreshold = wcThreshold
        self.saveVerbose = saveVerbose
        self.parseOn = parseOn
        self.mD = {}
        self.tdm = []
        self.tdmraw = []
        self.termraw = []
        self.docs = []
        self.docsSize = []
        self.terms = []
        self.docCount = 0
        self.idfweight = False
        self.P = []
        self.Q = []
        self.er = []
        self.idfs = []
        return
    def add(self, newThing, docs=""):
        def _mergeDict(self, newD, docs=""):
            # Grab doc count so far
            docIndex = self.docCount
            # Get the correct title
            if docs == "":
                docs = docIndex
            self.docs.append(docs)
            # Add doc size (useful with tdmraw)
            tdWeight = float(sum(newD.values()))
            if tdWeight == 0:
                tdWeight = 1.
            self.docsSize.append(tdWeight)
            # Add newD to mD
            for key in newD:
                if key in self.mD:
                    if len(self.mD[key]) < self.docCount:
                        for i in range(len(self.mD[key]), self.docCount):
                            self.mD[key].append(0.)
                    self.mD[key].append(newD[key]/float(tdWeight))
                else:
                    if self.docCount > 0:
                        self.mD[key] = [0.]
                        for i in range(1, self.docCount):
                            self.mD[key].append(0.)
                        self.mD[key].append(newD[key]/float(tdWeight))
                    else:
                        self.mD[key] =  [newD[key]/float(tdWeight)]
            self.docCount += 1
            return 
            
        
        # Ok what was I just given?
        if type(newThing) == list:
            # Shit.. Ok we can handle this, a list of what?
            if len(newThing) > 0:
                if type(newThing[0]) == dict:
                    # Sweet, it's some dicts, merge them!
                    # Wait, what about the title var?
                    if (docs != "") and (type(docs) == list) and (len(docs) == len(newThing)):
                        for i in range(len(newThing)):
                            _mergeDict(self, newThing[i], docs[i])
                    else:
                        for i in range(len(newThing)):
                            _mergeDict(self, newThing[i])

                elif type(newThing[0]) in [float, int, str]:#long, unicode]:
                    # Well, I mean I don't see why numbers can't be LSA'ized
                    # Convert list to dict, then merge
                    newD = {}
                    for i in range(len(newThing)):
                        if newThing[i] in newD:
                            newD[newThing[i]] += 1
                        else:
                            newD[newThing[i]] = 1
                    _mergeDict(self, newD, docs)
                else:
                    raise TypeError ("Elements of list are not valid inputs")

                

        elif type(newThing) == dict:
            # Woo this is simple!
            _mergeDict(self, newThing, docs)

        elif type(newThing) == str:
            # I'm assuming I'm to add this string to the term doc Matrix
            strList = newThing.split(self.parseOn)
            newD = {}
            for i in range(len(strList)):
                if strList[i].strip() in newD:
                    newD[strList[i].strip()] += 1
                else:
                    newD[strList[i].strip()] = 1
            _mergeDict(self, newD, docs)
        return

    def weight_idf(self):
        # Now we're weighting it, booyea
        # The weighting applied here is idf, and assumes td weighting was applied earlier
        #   idf: inverse document frequency: log(N/ni)
        #     if every doc has word ni, the it zeros out the row
        #     Rather than math it, check for it first
        self.idfweight = True
        for key in self.mD:
            # Saving raw state allows matrix to grow w/o redoing everything
            # only done if 
            if self.saveVerbose == True:
                self.termraw.append(key)
            # This chunk is to check for the idf weight condition:
            #   if every doc has the term, then it's not worth 'mathing'
            #   and instead can be eliminated
            idf = False
            if len(self.mD[key]) < self.docCount:
                idf = True
                for i in range(len(self.mD[key]), self.docCount):
                    self.mD[key].append(0.)
            # Saving raw matrix
            if self.saveVerbose == True:
                self.tdmraw.append(self.mD[key])
            # Scan row for a zero
            if idf == False:
                for i in range(len(self.mD[key])):
                    if self.mD[key][i] == 0:
                        idf = True
                        break
            # No longer works as advertized in python3
            # CURRENTLY AN ERROR DUE TO TD WEIGHTING EARLIER: FIXED
            #if (len(filter(None, self.mD[key])) >= self.wcThreshold) and idf == True:
            # Adjustment:
            if (len(list(self.mD[key])) >= self.wcThreshold) and idf == True:
                self.terms.append(key)
                self.tdm.append(self.mD[key])
        
        # Ok now it's actually time to start weighting
        self.tdm = numpy.array(self.tdm)
        #print len(self.tdm)
        for i in range(len(self.tdm)):
            #print self.terms[i]
            ni = float(numpy.count_nonzero(self.tdm[i]))
            if ni == 0:
                raise ValueError("ARG HOW ARE THERE NO NON ZERO ELIMENTS")
            #print ni, self.docCount
            idfValue = math.log(self.docCount/ni)
            self.tdm[i] = self.tdm[i] * idfValue
            self.idfs.append(idfValue)
            
        return

    def svd(self):
        return

    def spectralEmbed(self, k, n_neighbors=10):
	    from sklearn import manifold
	    se = manifold.SpectralEmbedding(n_components=k, n_neighbors=n_neighbors)
	    Yse = se.fit_transform(self.tdm)
	    print(len(Yse))
	    return Yse

    def nmf(self, k):
        
        nmf = NMF(n_components=k, max_iter=200)
        P = nmf.fit_transform(self.tdm)
        Q = nmf.components_.T
        self.P = P
        self.Q = Q
        self.er = nmf.reconstruction_err_
        logging.debug("lsalib: Non Negative Matrix Factorization Reconstruction Error: " + str(self.er))
        #print "\tNMF Error: ", self.er
        return P, Q
 
    def saveParts(self, location=""):
        # Check Location
        if location != "":
            if location[-1] != "/":
                location = str(location) + "/"
            if not os.path.exists(location): os.makedirs(location)
        # Save Docs
        docSet = open(str(location) + "docs.lsd", 'w')
        for i in range(len(self.docs)):
            docSet.write(str(self.docs[i]) +"\n")
        docSet.close()
        # Save Weighted TD Matrix
        tdm = open(str(location) + "tdmWeighted.lsm", 'w')
        for i in range(len(self.tdm)):
            for j in range(len(self.tdm[i])):
                tdm.write(str(self.tdm[i][j]) + "\t")
            tdm.write("\n")
        tdm.close()
        # Save Raw TD Matrix
        if self.saveVerbose == True:
            tdmR = open(str(location) + "tdmRaw.lsm", 'w')
            for i in range(len(self.tdmraw)):
                for j in range(len(self.tdmraw[i])):
                    tdmR.write(str(self.tdmraw[i][j]) + "\t")
                tdmR.write("\n")
            tdmR.close()
        # Save P Matrix
        p = open(str(location) + "Pmatrix.lsp", 'w')
        for i in range(len(self.P)):
            for j in range(len(self.P[i])):
                p.write(str(self.P[i][j]) + "\t")
            p.write("\n")
        p.close()
        # Save Q Matrix
        q = open(str(location) + "Qmatrix.lsq", 'w')
        for i in range(len(self.Q)):
            for j in range(len(self.Q[i])):
                q.write(str(self.Q[i][j]) + "\t")
            q.write("\n")
        q.close()
        # Save idf Weights 
        idfs = open(str(location) + "idf.lsi", 'w')
        for i in range(len(self.idfs)):
            idfs.write(str(self.idfs[i]) + "\n")
        idfs.close()
        # Save Terms
        termSet = open(str(location) + "terms.lst", 'w')
        for i in range(len(self.terms)):
            termSet.write((self.terms[i]).encode('utf-8').strip() +"\n")
        termSet.close()

        return
            
        
            


    def __repr__(self):
        # This will be redone, 
        # __repr__ does not need to print the td matrix 
        if self.idfweight == False:
            a = "\t"
            for i in range(len(self.docs)):
                a = a +'"'+ str(self.docs[i]) +'"'+ "\t"
            a = a + "\n"
        
            for key in self.mD:
                a = a +'"'+ key +'"'+ "\t"
                for i in range(self.docCount):
                    if i < len(self.mD[key]):
                        a = a + str(self.mD[key][i]) + ",\t"
                    else:
                        a = a + "0.0,\t"
                a = a + "\n"
        else:
            a = "\t"
            for i in range(len(self.docs)):
                a = a +'"'+ str(self.docs[i]) +'"'+ "\t"
            a = a + "\n"
            for i in range(len(self.terms)):
                a = a +'"'+  self.terms[i] + '"\t'
                for j in range(self.docCount):
                    a = a + str(self.tdm[i][j]) + ",\t"
                a = a + "\n"
        #msg = str(a)
        return a


