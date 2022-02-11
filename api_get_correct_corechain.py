""" Author: Ahmad Alzeitoun, The University of Bonn
    Date created: 03/2021
    Status: Production
"""

from sentence_transformers import SentenceTransformer, util
from sentence_transformers.cross_encoder import CrossEncoder
import numpy as np
from datetime import datetime
import time
from sparqlQueries import write_to_file, mu_prop_lcquad


def sbert_answers(question_val, corechains, specialUse=None): #correctAns removed as para
    model_save_path = 'models/lcquad_e5_b64_distilbert-base-uncased-2021-03-24_22-14-29'
    id_CC = [item[0] for item in corechains]
    # print (id_CC)
    lbl_CC = [item[1] for item in corechains]
    # print (lbl_CC)


    question = []
    top_5 = []
    corpus = lbl_CC

    scores = []



    #--------------------------------------------------------------------------
    #------------------------------- Cross Encoder ----------------------------
    #--------------------------------------------------------------------------
    top_5_cross = []
    if specialUse:
        #------------------------------ Cross-Encoder model
        modelType = 'crossencoder_e4_b16'
        model_save_path2 = 'models/lcquad_crossencoder_e4_b16_2021-07-26_02-32-37'
        model = CrossEncoder(model_save_path2)
        # So we create the respective sentence combinations
        sentence_combinations = [[question_val, corpus_sentence] for corpus_sentence in corpus]

        # Compute the similarity scores for these combinations
        similarity_scores = model.predict(sentence_combinations)

        # Sort the scores in decreasing order
        sim_scores_argsort = reversed(np.argsort(similarity_scores))

        # Print the scores
        #print("question:", question_val)
        for idx in sim_scores_argsort:
            #print("{:.2f}\t{}".format(similarity_scores[idx], corpus[idx]))
            top_5_cross.append(corpus[idx])

        #--------------------------------------------------------------------------
        # top1 id and label
        index_ans = lbl_CC.index(top_5_cross[0])
        top1_cross_ccId = corechains[index_ans][0]
        top1_cross_cclbl = top_5_cross[0]

        top1_cross_cc = [top1_cross_ccId,top1_cross_cclbl]
        print('-Cross Encoder: ', top_5_cross[0])
        if specialUse == 'crossencoder':
            return top1_cross_cc
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------



    #--------------------------------------------------------------------------
    #-------------------------------- Bi Encoder ------------------------------
    #--------------------------------------------------------------------------
    model = SentenceTransformer(model_save_path)

    #Encode all sentences
    corpus_embeddings = model.encode(corpus)

    question.append(question_val)
    # Encode sentences:
    query_embeddings = model.encode(question)
    #Compute cosine similarity between all pairs
    cos_sim = util.pytorch_cos_sim(corpus_embeddings, query_embeddings)

    #Add all pairs to a list with their cosine similarity score
    all_sentence_combinations = []
    for i in range(len(cos_sim)):
        all_sentence_combinations.append([cos_sim[i], i])

    #Sort list by the highest cosine similarity score
    all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)
    for score, i in all_sentence_combinations[0:15]:  # len(corpus)
        top_5.append(corpus[i])
        # scores.append(score)


    print('Bi Encoder: ', top_5[0])
    #--------------------------------------------------------------------------
    # top1 id and label
    index_ans = lbl_CC.index(top_5[0])
    top1_ccId = corechains[index_ans][0]
    top1_cclbl = top_5[0]

    top1_cc = [top1_ccId,top1_cclbl]
    return top1_cc


#============================================================================
#========  put lbl, ids of corechains for specific TE in one list
#============================================================================
def lcquad_corechain(question_val, candidate_corechains, specialUse=None):
    corechains_labels = []
    corechains_ids = []
    isFound = False
    if not specialUse:
        i = 0
        for ccLine in candidate_corechains:
            i += 1
            arguments = ccLine.split("\t")
            cc_entIds = arguments[0]
            cc_sign = arguments[1]
            cc_lbl = arguments[2]
            cc_id = arguments[3].replace("\n","")
            corechains_labels.append(cc_lbl)
            corechains_ids.append(cc_id)

        corechains = list(zip(corechains_ids,corechains_labels))
    else:
        corechains = candidate_corechains


    final_testResult = []
    gAnswer_topAnswer = []

    top1_cc = []
    # return final_testResult, gAnswer_topAnswer
    if specialUse == 'crossencoder':
        top1_cc = sbert_answers(question_val, corechains, specialUse)
    else:
        top1_cc = sbert_answers(question_val, corechains)

    return top1_cc

#============================================================================
#========  read question (Quest, answer, TE) and extract corechains
#============================================================================
#* dataSource : wikidata or cache
def lcquad_single_q(topicEntity, nlQuestion, candidate_corechains=None): ###### dataSource : wikidata or cache
    #F_test_corechains = open("data/lcquad_test/lcquad_test_corechain.txt", "r")
    F_test_corechains = open("data/lcquad_cache/lcquad_cache_corechain.txt", "r")

    all_test_corechains = F_test_corechains.readlines()

    start_time_loop = time.time()

    top1_cc = []
    # candidate_corechains = []

    print("")
    print("==============================")
    print("Question: ", nlQuestion)
    print("Topic Entity: ", topicEntity)


    #### retrieve core chains from Cashe
    if len(candidate_corechains) == 0:
        tabbed_entIDs = topicEntity + '\t'
        # collect all corechains for the relevant TE from cache
        candidate_corechains = [x for x in all_test_corechains if tabbed_entIDs in x]

        if candidate_corechains:
            top1_cc = lcquad_corechain(nlQuestion, candidate_corechains)
            #print('top corechain:', top1_cc)

        else:
            top1_cc = ['no corechain']
            print('This Topic entity has no corechain')
    #### retrieve core chains from wikidata
    else:
        # candidate_corechains = all_ccc_generation(nlQuestion, topicEntity)
        top1_cc = lcquad_corechain(nlQuestion, candidate_corechains, 'specialUse')

    return top1_cc
