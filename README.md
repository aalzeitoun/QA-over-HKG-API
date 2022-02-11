# Question Answering over Hyper-relational Knowledge Graph API

Question Answering system API that receive pair of (question, Topic Entity) as input and generate the output as the answer of the given question as (SPARQL Query, Result of excuting the query).

## Description

In this work, we explore the core chain approaches for the task of Knowledge Graph Question Answering (KGQA). We adopt hyper-relational KG (e.g., Wikidata) as new domain for previous work, focusing on pre-trained Language model, Sentence-BERT is state-of-the-art sentence and text embedding, we proposed method for core chain ranking on two QA dataset [LC-QuAD 2.0](https://figshare.com/projects/LCQuAD_2_0/62270) over wikidata knowledge graph. Our system generates the core chains from a natural language question (NLQ) then ranks these core chains in-order to build actual Sparql query. In addition, we explore the intention of the question, we consider this task as a predicting task and we pre-trained BERT model to accomplish it.

## Getting Started

### Dependencies

We recommend **Python 3.6** or higher, **[PyTorch 1.6.0](https://pytorch.org/get-started/locally/)** or higher and **[transformers v3.1.0](https://github.com/huggingface/transformers)** or higher. The code does **not** work with Python 2.7.

If you want to use a GPU / CUDA, you must install PyTorch with the matching CUDA Version. Follow
[PyTorch - Get Started](https://pytorch.org/get-started/locally/) for further details how to install PyTorch.

### Installing

* Install [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
* Install [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper)
* Install [FastAPI](https://fastapi.tiangolo.com)


### Executing program

* Run the API App (as a server)
* Run the Example (as a client)
```
uvicorn main:app --reload
```
```
python3 example.py
```

## Example

example.py send a JSON body contains a ***Question*** and the ***Topic Entity*** (Wikidata identifier) of the question as a *request* to the API, then will receive a JSON file holds the *Answer*, *SPARQL Query* and the *Top Ranked Core chain*.

JSON sent to the API:
```
{
    "question_txt": "What is your name?",
    "topic_entity_id": "Q3035"
}
```

JSON received from API app:
```
{
    "question_txt": "What is your name?",
    "topic_entity_id": "Q3035",
    "top_corechain": "THE TOP RANKED CORECHAIN",
    "sparqlQuery": "SPARQL QUERY OF THE ANSWER",
    "answer": "ANSWER OF THE QUESTION"
}
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.1
    * Initial Release

## License

To be added

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
