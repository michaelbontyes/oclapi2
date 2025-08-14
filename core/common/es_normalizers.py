from elasticsearch_dsl import normalizer
from pydash import get

normalizer("lowercase", type='lowercase')


class ScoreNormalizer:
    MIN_MAX_NORMALIZER = 'min_max_normalizer'

    def __init__(self, search_results, normalizer=MIN_MAX_NORMALIZER):
        self.search_results = search_results
        self.normalizer = normalizer

    def normalize(self):
        if self.normalizer == self.MIN_MAX_NORMALIZER:
            return self.__min_max_normalize()
        return self.search_results

    def __min_max_normalize(self):
        max_score = get(self.search_results, 'hits.max_score')
        if not max_score:
            return self.search_results
        for result in self.search_results['hits']['hits']:
            result['_score'] = result['_score'] / max_score
        self.search_results['hits']['max_score'] = 1
        return self.search_results
