import json
import pathlib
import traceback
import typing

import pyjsonviewer
import ujson as ujson
import urlpath as urlpath
from joblib import Memory

from .request_utils import send_request

location = "./cachedir"
memory = Memory(location, verbose=0)

PathLike = typing.Union[str, pathlib.Path, urlpath.URL]
IOPathLike = typing.Union[PathLike, typing.IO]


class ResultSet:
    def __init__(self, primary_key="doc_id", response_key: list = None, results=[]):
        self.primary_key = primary_key
        self.response_key = response_key
        self.results = results

    def _fetch_results_from_response(self, json_response):
        try:
            if self.response_key:
                assert isinstance(self.response_key, list)
                for key in self.response_key:
                    json_response = json_response[key]
                return json_response
            else:
                return json_response
        except KeyError as err:
            raise Exception(f"invalid response key:{self.response_key}")
        except Exception as err:
            print(traceback.format_exc())

    def transform(self):
        """
        transform items before final usage
        :return:
        """
        return [x for x in self.results]

    def load_json(self, path):
        """
        load json data from a file
        :param path:
        :return:
        """
        json_str = pathlib.Path(path).read_text()
        try:
            json_output = ujson.loads(json_str)
        except Exception as err:
            print(traceback.format_exc())

        try:
            self.results = self._fetch_results_from_response(json_output)
            self.results = self.transform()
        except Exception as err:
            print(traceback.format_exc())
            self.results = []

    def load_url(self, url, method="GET", params=None):
        """
        load json data from an http url
        :param url:
        :param method:
        :param params:
        :return:
        """
        # cache url requests on disk
        costly_send_request = memory.cache(send_request)
        json_output = costly_send_request(url=url, method=method, params=params)
        if not json_output:
            raise Exception(f"Invalid response from url:{url}")

        try:
            self.results = self._fetch_results_from_response(json_output)
        except Exception as err:
            print(traceback.format_exc())
            self.results = []

    def __sub__(self, other):
        """
        returns result items not present in other result set.
        :param other:
        :return:
        """
        other_keys = set([res[other.primary_key] for res in other.results])
        diff_results = [res for res in self.results if res[self.primary_key] not in other_keys]
        return ResultSet(primary_key=self.primary_key, results=diff_results)

    def __len__(self):
        """
        return size of result set
        :return:
        """
        return len(self.results)

    def __str__(self):
        """
        str representation
        :return:
        """
        return json.dumps(self.results)

    def __repr__(self):
        """
        repr string
        :return:
        """
        return f"ResultSet(primary_key={self.primary_key}, results={self.results})"

    def intersection(self, other, topn=None):
        """
        get common results between two result sets
        :param other:
        :param topn:
        :return:
        """
        if topn is None or not isinstance(topn, int):
            topn = min(len(self), len(other))

        other_keys = set([res[other.primary_key] for res in other.results[:topn]])
        common_results = [res for res in self.results[:topn] if res[self.primary_key] in other_keys]
        return ResultSet(primary_key=self.primary_key, results=common_results)

    def view_data(self):
        """
        views json data in a native window
        :return:
        """
        pyjsonviewer.view_data(json_data=self.results)
