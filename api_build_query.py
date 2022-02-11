from api_get_correct_corechain import lcquad_single_q
#from api_predict_queryType import pred_questionType
from api_corechains_generation import corechains_generation

########recieve the ids of (given) correct corechain and return list[ids, lbl] of it.
### ex recieve  +P31  return: [+P31, '+instance of']
def generate_query_statements(topicEntity, correct_CC, queryHead): 
    div_parts_noSign = correct_CC.replace(',','')
    div_parts = div_parts_noSign.split(' ')
    new_correct_CC_arr = []
    queryStatements = []

    ### if not ASK query then no need to have the same predicats in the corechain
    #### ex: it will convert [+P31, +P31] --> [+P31]
    if ',' in correct_CC:
        if queryHead == "SELECT" and div_parts[0] == div_parts[1]:
            div_parts = [div_parts[0]]

    ### single predicat CC   [+P1]
    if len(div_parts) == 1:
        sign = div_parts[0][0]
        cc_without_sign = div_parts[0].replace(sign,'')
        if sign == '+':
            queryStatements = "wd:{} wdt:{} ?answer ."
            queryStatements = queryStatements.format(topicEntity, cc_without_sign)
            queryStatements = ["?answer ?answerLabel ", queryStatements]
        if sign == '-':
            queryStatements = "?answer wdt:{} wd:{} ."
            queryStatements = queryStatements.format(cc_without_sign, topicEntity)
            queryStatements = ["?answer ?answerLabel ", queryStatements]
    
    ## Two predicats CC ex: [+P1 +P2] or [+P1, +P2] or [+P1 *P2]
    if len(div_parts) == 2:
        sign1= div_parts[0][0]
        sign2= div_parts[1][0]

        cc1_without_sign = div_parts[0].replace(sign1,'')
        cc2_without_sign = div_parts[1].replace(sign2,'')
        if sign2 != '*':
            if ',' in correct_CC:
                if sign1 == '+' and sign2 == '+':
                    queryStatements = "wd:{} wdt:{} ?answer1. wd:{} wdt:{} ?answer2 ."
                    queryStatements = queryStatements.format(topicEntity, cc1_without_sign, topicEntity, cc2_without_sign)
                    queryStatements = ["?answer1 ?answer2 ?answer1Label ?answer2Label ", queryStatements]
                if sign1 == '+' and sign2 == '-':
                    queryStatements = "wd:{} wdt:{} ?answer1. ?answer2 wdt:{} wd:{} ."
                    queryStatements = queryStatements.format(topicEntity, cc1_without_sign, cc2_without_sign, topicEntity)
                    queryStatements = ["?answer1 ?answer2 ?answer1Label ?answer2Label ", queryStatements]
                if sign1 == '-' and sign2 == '+':
                    queryStatements = "?answer1 wdt:{} wd:{}. wd:{}  wdt:{} ?answer2 ."
                    queryStatements = queryStatements.format(cc1_without_sign, topicEntity, topicEntity, cc2_without_sign)
                    queryStatements = ["?answer1 ?answer2 ?answer1Label ?answer2Label ", queryStatements]
                if sign1 == '-' and sign2 == '-':
                    queryStatements = "?answer1 wdt:{} wd:{}. ?answer2 wdt:{} wd:{} ."
                    queryStatements = queryStatements.format(cc1_without_sign, topicEntity, cc2_without_sign, topicEntity)
                    queryStatements = ["?answer1 ?answer2 ?answer1Label ?answer2Label ", queryStatements]
            else:
                ####### (issue: it could be asking about answer2 instead of answer1.) ####### (SHOULD BE SOLVED!!!) ########
                if sign1 == '+' and sign2 == '+':
                    queryStatements = "wd:{} wdt:{} ?answer1. ?answer1 wdt:{} ?answer2 ."
                    queryStatements = queryStatements.format(topicEntity, cc1_without_sign, cc2_without_sign)
                    queryStatements = ["?answer1 ?answer1Label ", queryStatements]
                if sign1 == '+' and sign2 == '-':
                    queryStatements = "wd:{} wdt:{} ?answer1. ?answer2 wdt:{} ?answer1 ."
                    queryStatements = queryStatements.format(topicEntity, cc1_without_sign, cc2_without_sign)
                    queryStatements = ["?answer1 ?answer1Label ", queryStatements]
                if sign1 == '-' and sign2 == '+':
                    queryStatements = "?answer1 wdt:{} wd:{}. ?answer1  wdt:{} ?answer2 ."
                    queryStatements = queryStatements.format(cc1_without_sign, topicEntity, cc2_without_sign)
                    queryStatements = ["?answer1 ?answer1Label ", queryStatements]
                if sign1 == '-' and sign2 == '-':
                    queryStatements = "?answer1 wdt:{} wd:{}. ?answer2 wdt:{} ?answer1 ."
                    queryStatements = queryStatements.format(cc1_without_sign, topicEntity, cc2_without_sign)
                    queryStatements = ["?answer1 ?answer1Label ", queryStatements]
        else:
            ####### (issue: it could be asking about answer2 instead of answer1.) ####### (SHOULD BE SOLVED!!!) ########
            if sign1 == '+':
                #SELECT ?value WHERE { wd:Q187247 p:P27 ?s . ?s ps:P27 wd:Q159 . ?s pq:P580 ?value}
                queryStatements = "wd:{} p:{} ?s. ?s ps:{} ?answer2. ?s pq:{} ?answer1 ."
                queryStatements = queryStatements.format(topicEntity, cc1_without_sign, cc1_without_sign, cc2_without_sign)
                queryStatements = ["?answer1 ?answer1Label ", queryStatements]
            if sign1 == '-':
                queryStatements = "?answer2 p:{} ?statement . ?statement ps:{} wd:{}. ?statement pq:{} ?answer1 ."
                queryStatements = queryStatements.format(cc1_without_sign, cc1_without_sign, topicEntity, cc2_without_sign)
                queryStatements = ["?answer1 ?answer1Label ", queryStatements]
       
    
    # # ex: [+P1 +P2, +P3]    or   [+P1 *P2, *P3]
    if len(div_parts) == 3:
        sign1= div_parts[0][0]
        sign2= div_parts[1][0]
        sign3= div_parts[2][0]

        cc1_without_sign = div_parts[0].replace(sign1,'')
        cc2_without_sign = div_parts[1].replace(sign2,'')
        cc3_without_sign = div_parts[2].replace(sign3,'')
        if sign2 != '*':
            #build the last two statements:
            if sign2 == '+' and sign3 == '+':
                qStat_part2 = "?answer1 wdt:{} ?answer2. ?answer1 wdt:{} ?answer3 ."
                qStat_part2 = qStat_part2.format(cc2_without_sign, cc3_without_sign)
            if sign2 == '+' and sign3 == '-':
                qStat_part2 = "?answer1 wdt:{} ?answer2. ?answer3 wdt:{} ?answer1 ."
                qStat_part2 = qStat_part2.format(cc2_without_sign, cc3_without_sign)
            if sign2 == '-' and sign3 == '+':
                qStat_part2 = "?answer2 wdt:{} ?answer1. ?answer1  wdt:{} ?answer3 ."
                qStat_part2 = qStat_part2.format(cc2_without_sign, cc3_without_sign)
            if sign2 == '-' and sign3 == '-':
                qStat_part2 = "?answer2 wdt:{} ?answer1. ?answer3 wdt:{} ?answer1 ."
                qStat_part2 = qStat_part2.format(cc2_without_sign, cc3_without_sign)
        
            #build the first statement and combine it with the last two statemnets:
            if sign1 == '+':
                queryStatements = "wd:{} wdt:{} ?answer1. "
                queryStatements = queryStatements.format(topicEntity, cc1_without_sign)
                queryStatements = queryStatements + qStat_part2
                queryStatements = ["?answer1 ?answer1Label ", queryStatements]
            if sign1 == '-':
                queryStatements = "?answer1 wdt:{} wd:{}. "
                queryStatements = queryStatements.format(cc1_without_sign, topicEntity)
                queryStatements = queryStatements + qStat_part2
                queryStatements = ["?answer1 ?answer1Label ", queryStatements]
        else:
            if sign1 == '+':
                queryStatements = "wd:{} p:{} ?statement. ?statement ps:{} ?answer3. ?statement pq:{} ?answer1 . ?statement pq:{} ?answer2 ."
                queryStatements = queryStatements.format(topicEntity, cc1_without_sign, cc1_without_sign, cc2_without_sign, cc3_without_sign)
                queryStatements = ["?answer1 ?answer2 ?answer1Label ?answer2Label ", queryStatements]
            if sign1 == '-':
                queryStatements = "?answer3 p:{} ?statement . ?statement ps:{} wd:{}. ?statement pq:{} ?answer1 . ?statement pq:{} ?answer2 ."
                queryStatements = queryStatements.format(cc1_without_sign, cc1_without_sign, topicEntity, cc2_without_sign, cc3_without_sign)
                queryStatements = ["?answer1 ?answer2 ?answer1Label ?answer2Label ", queryStatements]

    queryStatements[1] = "WHERE { " + queryStatements[1] + " SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'.} }"
    return queryStatements





# ##############################################
def question_answering(nlQuestion, topicEntity):
    # nlQuestion = input("Enter Question: ")
    # topicEntity = input("Enter Topic Entity Identifier: ")

    candidate_corechains = corechains_generation(nlQuestion, topicEntity)
    correct_corechain = lcquad_single_q(topicEntity, nlQuestion, candidate_corechains)
    predicted_questionType = 0 #pred_questionType(nlQuestion)

    topicEntity1 = topicEntity
    if ',' in topicEntity:
        topicEntity_arr = topicEntity.split(',')
        topicEntity1 = topicEntity_arr[0]

    generatedQuery = ""

    hasCC = True
    if len(correct_corechain) == 1:
        hasCC = False

    print("Top Core chain: ", correct_corechain)

    top_corechain = ""

    if hasCC:
        queryHead = ""
        if predicted_questionType == 0:
            queryHead = "SELECT"
            query_body = generate_query_statements(topicEntity1, correct_corechain[0], queryHead)
            generatedQuery = "{} distinct {} {}"
            generatedQuery = generatedQuery.format(queryHead, query_body[0], query_body[1])

        if predicted_questionType == 1:
            queryHead = "ASK"
            query_body = generate_query_statements(topicEntity1, correct_corechain[0], queryHead)
            generatedQuery = "{} {}"
            generatedQuery = generatedQuery.format(queryHead, query_body[1])

        print(generatedQuery)
        top_corechain = correct_corechain
    else:
        print(correct_corechain[0])
        top_corechain = correct_corechain[0]

    return top_corechain, generatedQuery



# sparqlQuery = "{} ?sbj where { ?sbj wdt:P802 wd:Q44015 . ?sbj wdt:P31 wd:Q178885 } "
# print(sparqlQuery.format(queryHead, itemno, price))
# ########################################################



# Which is the sports award that Lionel Messi was awarded?  (Q615)
# question_answering("Which is the sports award that Lionel Messi was awarded?", "Q615")








# print("corrected CC: ", correct_corechain)
# print("Question Type: ", predicted_questionType)


#Q44015, Q178885	-P802 +P31	Who is the god for John the Apostle?	 
#select distinct ?sbj where { ?sbj wdt:P802 wd:Q44015 . ?sbj wdt:P31 wd:Q178885 } 



###############################################
######### Query & Core chain types:############
###############################################
# 1) +P
# select distinct ?answer where { ?answer wdt:P57 wd:Q555578}
# #Who is the director of Chespirito?

# 2) +P +P        (issue: how to know if the value is s/obj1 or s/obj2)   ->(See LCQUAD2: T10, T18)
# SELECT DISTINCT ?sbj ?sbj_label WHERE { ?sbj wdt:P31 wd:Q4830453 . ?sbj wdt:P414 wd:Q13677 . ?sbj rdfs:label ?sbj_label }
# #Tell me the business of the stock exchange of the New York Stock Exchange that contains the word wabtec in it's name?

# 3) +P *P      (issue: how to know if the value is s/obj or quilifier)  ->(See LCQUAD2: T6, T7)
# SELECT ?value WHERE { wd:Q187247 p:P27 ?s . ?s ps:P27 wd:Q159 . ?s pq:P580 ?value}
# #When was Alexander Karelin become the citizen of Russia?

# 4) +P, +P         (Always ask about two values)
# SELECT ?ans_1 ?ans_2 WHERE { wd:Q131324 wdt:P22 ?ans_1 . wd:Q131324 wdt:P25 ?ans_2 }
# # Who is the father and mother of Janet Jackson?

# 5) +P +P, +P          (always value is part of each statement)
# select ?ent where { ?ent wdt:P31 wd:Q4830453 . ?ent wdt:P2226 ?obj . ?ent wdt:P414 wd:Q151139 }
# #What business on the Frankfurt Stock Exchange has the largest market cap ?

# 6) +P *P, *P      (always value1, value2 come as quilifiers)
# SELECT ?value1 ?value2 WHERE { wd:Q184697 p:P69 ?s . ?s ps:P69 wd:Q738258 . ?s pq:P512 ?value1 . ?s pq:P812 ?value2 }
# #Which is academic degree and academic major of Gloria Estefan who educated at as University of Miami
###############################################
###############################################


# print("+*", generate_query_statements("Q187247","+P27, *P580"))
# print("-*", generate_query_statements("Q40030","-P2632, *P585"))
# print("+*", generate_query_statements("Q184697","+P69, *P512"))
# print("-*", generate_query_statements("Q738258","-P69, *P512"))
#print("-++", generate_query_statements("Q4830453","-P31 +P2226, +P512"))
# print("+**", generate_query_statements("Q184697","+P69 *P512, *P812"))
# print("-**", generate_query_statements("Q738258","-P69 *P512, *P812"))


# SELECT DISTINCT ?answer1_label ?answer2_label WHERE { wd:Q131324 wdt:P22 ?answer1. wd:Q131324 wdt:P25 ?answer2. 
#                                                     ?answer1 rdfs:label ?answer1_label. ?answer2 rdfs:label ?answer2_label.
#                                                    FILTER (lang(?answer1_label) = 'en')
#                                                    FILTER (lang(?answer2_label) = 'en')}



#! Question examples:
# what university Albert Einstein did his bachelor of science degree?  ->> Q937
# What's the original language for Titanic? ->> 
# Which is the sports award that Lionel Messi was awarded?  (Q615)