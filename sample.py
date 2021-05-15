from icecream import ic

from irlab import ResultSet

if __name__ == '__main__':
    # compare results from json file
    old_rs = ResultSet(primary_key="doc_id", response_key=None)

    old_rs.load_json("dat/old_results.json")

    new_rs = ResultSet(primary_key="doc_id", response_key=None)

    new_rs.load_json("dat/new_results.json")
    ic(len(old_rs - new_rs) / len(new_rs.results))
    (old_rs-new_rs - new_rs).view_data()

    # compare results from url file
    # old_rs = ResultSet(primary_key="doc_id", response_key=None)
    # old_rs.load_url(url="http://localhost:20002/url/staging", method="GET")
    #
    # new_rs = ResultSet(primary_key="doc_id", response_key=None)
    # new_rs.load_url(url="http://localhost:20003/similar/url/production", method="GET")
    #
    # ic(len(new_rs.intersection(old_rs, topn=10)))
    # ic(len(new_rs.intersection(old_rs, topn=20)))
    # ic(len(new_rs.intersection(old_rs, topn=30)))
    # ic(len(new_rs.intersection(old_rs, topn=40)))
