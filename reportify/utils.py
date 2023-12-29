import os
import pickle
import random
import string
from collections import OrderedDict

import nltk
from django.conf import settings
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from transformers import DistilBertModel, DistilBertTokenizer


class CustomPageNumberPagination(PageNumberPagination):
    max_page_size = 20
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    (
                        "current_page",
                        self.get_page_number(
                            self.request,
                            self.page.paginator,
                        ),
                    ),
                    ("total_pages", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )


class ReportClassifierModelLoader:
    svm_model = None

    @classmethod
    def load_model(cls):
        """
        Load SVM model.
        """
        model_path = os.path.join(
            settings.BASE_DIR,
            "reports",
            "ml_models",
            "report_classifier.pkl",
        )
        with open(model_path, "rb") as f:
            svm_model = pickle.load(f)

        cls.svm_model = svm_model

    @classmethod
    def get_model(cls):
        """
        Get SVM model.
        """
        return cls.svm_model


def generate_random_string(string_length: int = 5) -> str:
    """
    Generate random string.
    """
    random_string = "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=string_length,
        )
    )

    return random_string


def generate_random_numbers(number_length: int = 5) -> str:
    """
    Generate random numbers.
    """
    random_numbers = "".join(
        random.choices(
            string.digits,
            k=number_length,
        )
    )

    return random_numbers


def remove_punctuation(input_string):
    """
    Remove punctuation from input string.
    """
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result


def get_bert_embeddings(sentence):
    """
    Get BERT embeddings for a sentence.
    """
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model = DistilBertModel.from_pretrained("distilbert-base-uncased")

    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()


def get_user_input_embeddings(user_input):
    """
    Get user input embeddings from BERT model.
    """
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))

    user_input_processed = remove_punctuation(user_input.lower())

    user_input_tokens = nltk.word_tokenize(user_input_processed)
    user_input_tokens = [word for word in user_input_tokens if word not in stop_words]
    user_input_tokens = [stemmer.stem(word) for word in user_input_tokens]

    user_input_string = " ".join(user_input_tokens)
    user_input_embedding = get_bert_embeddings(user_input_string)

    return user_input_embedding
