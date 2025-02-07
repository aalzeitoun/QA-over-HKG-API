""" Author: Ahmad Alzeitoun, The University of Bonn
    Date created: 02/2022
    Status: Production
"""

from api_build_query import question_answering
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
# import torch

class Question_para(BaseModel):
    question_txt: str
    topic_entity_id: str

app = FastAPI()

@app.post("/answer/")
async def create_item(question: Question_para):
    question_dict = question.dict()
    if question.topic_entity_id:
        top_corechain, sparqlQuery = question_answering(question.question_txt, question.topic_entity_id)
        question_dict.update({"top_corechain": top_corechain, "sparqlQuery": sparqlQuery})
    return question_dict
