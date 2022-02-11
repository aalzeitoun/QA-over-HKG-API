# Question Answering over Hyper-relational Knowledge Graph API

Question Answering system API that receive pair of (question, Topic Entity) as input and generate the output as the answer of the given question as (SPARQL Query, Result of excuting the query).

## Description

In this work, we explore the core chain approaches for the task of Knowledge Graph Question Answering (KGQA). We adopt hyper-relational KG (e.g., Wiki- data) as new domain for previous work, focusing on pre-trained Language model, Sentence-BERT is state-of-the-art sentence and text embedding, we proposed method for core chain ranking on two QA data-set LC-QuAD 2.0 over wikidata knowledge graph. Our system generates the core chains from a natural language question (NLQ) then ranks these core chains in-order to build actual Sparql query. In addition, we explore the intention of the question, we consider this task as a predicting task and we pre-trained BERT model to accomplish it.

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```
