import pathlib
import traceback
import typing

import ujson as ujson
import urlpath as urlpath

from .request_utils import send_request

PathLike = typing.Union[str, pathlib.Path, urlpath.URL]
IOPathLike = typing.Union[PathLike, typing.IO]


class ResultSet:
    def __init__(self, primary_key="doc_id", response_key=None):
        self.primary_key = primary_key
        self.response_key = response_key
        self.results = []

    def _fetch_results_from_response(self, json_response):
        try:
            if self.response_key:
                return json_response[self.response_key]
            else:
                return json_response
        except KeyError as err:
            raise Exception(f"invalid response key:{self.response_key}")
        except Exception as err:
            print(traceback.format_exc())

    def load_json(self, path):
        json_str = pathlib.Path(path).read_text()
        try:
            json_output = ujson.loads(json_str)
        except Exception as err:
            print(traceback.format_exc())

        try:
            self.results = self._fetch_results_from_response(json_output)
        except Exception as err:
            print(traceback.format_exc())
            self.results = []

    def load_url(self, url, method="GET", params=None):
        json_output = send_request(url=url, method=method, params=params)
        if not json_output:
            raise Exception(f"Invalid response from url:{url}")

        try:
            self.results = self._fetch_results_from_response(json_output)
        except Exception as err:
            print(traceback.format_exc())
            self.results = []

    def __sub__(self, other):
        other_keys = set([res[other.primary_key] for res in other.results])
        diff_results = [res for res in self.results if res[self.primary_key] not in other_keys]
        return diff_results

    def __len__(self):
        return len(self.results)

    def intersection(self, other, topn=None):
        if topn is None or not isinstance(topn, int):
            topn = min(len(self), len(other))

        other_keys = set([res[other.primary_key] for res in other.results[:topn]])
        common_results = [res for res in self.results[:topn] if res[self.primary_key] in other_keys]
        return common_results
