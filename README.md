# Question Answering over Hyper-relational Knowledge Graph API

Question Answering system API, receives pair of (Question, Topic Entity) as input and generates the answer of the given question as (SPARQL Query, Result of excuting the query) as output.

## Description

In this work, we explore the core chain approaches for the task of Knowledge Graph Question Answering (KGQA). We adopt hyper-relational KG (e.g., Wikidata) as new domain for previous work, focusing on pre-trained Language model, Sentence-BERT is state-of-the-art sentence and text embedding, we proposed method for core chain ranking on QA dataset [LC-QuAD 2.0](https://figshare.com/projects/LCQuAD_2_0/62270) over wikidata knowledge graph. Our system generates the core chains from a natural language question (NLQ) then ranks these core chains in-order to build actual Sparql query. In addition, we explore the intention of the question, we consider this task as a classification task and we used a pre-trained BERT model to accomplish it.

We converted the application to be used as an API using FastAPI.

## Getting Started

### Dependencies

We recommend **Python 3.6** or higher, **[PyTorch 1.6.0](https://pytorch.org/get-started/locally/)** or higher and **[transformers v3.1.0](https://github.com/huggingface/transformers)** or higher. The code does **not** work with Python 2.7.

If you want to use a GPU / CUDA, you must install PyTorch with the matching CUDA Version. Follow
[PyTorch - Get Started](https://pytorch.org/get-started/locally/) for further details how to install PyTorch.

The pretrained models should be existed under model folder, the folder is empty and you need to download them from this [link](https://github.com/aalzeitoun/QA-over-HKG-API).

### Installing

* Install [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
* Install [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper)
* Install [FastAPI](https://fastapi.tiangolo.com)


### Executing program

* Run the API App (as a server)
* Run the Example (as a client)
```
$ uvicorn main:app --reload
```
```
$ python3 example.py
```

## Example

example.py send a JSON body contains a ***Question*** and the ***Topic Entity*** (Wikidata identifier) of the question as a *request* to the API, then will receive a JSON file holds the *Answer*, *SPARQL Query* and the *Top Ranked Core chain*.

JSON sent to the API:
```
{
    "question_txt": "Which is the sports award that Lionel Messi was awarded?",
    "topic_entity_id": "Q615"
}
```

JSON received from API app:
```
{
    "question_txt": "Which is the sports award that Lionel Messi was awarded?",
    "topic_entity_id": "Q615",
    "top_corechain": "THE TOP RANKED CORECHAIN",
    "sparqlQuery": "SPARQL QUERY OF THE ANSWER",
    "answer": "ANSWER OF THE QUESTION"
}
```

## Authors

Contributors names and contact info:

* Ahmad Alzeitoun (Author)  
* Dr. Mohnish Dubey (Supervisor)

## Version History

* 0.1
    * Initial Release

## License

To be added

## Acknowledgments

Inspiration:
* [Learning to Rank Query Graphs for Complex Question Answering over Knowledge Graphs](https://arxiv.org/abs/1811.01118)
* [Semantic Parsing via Staged Query Graph Generation: Question Answering with Knowledge Base](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ACL15-STAGG.pdf)
