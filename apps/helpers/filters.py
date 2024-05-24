from rest_framework.filters import SearchFilter
from algoliasearch_django import raw_search


class AlgoliaSearchFilter(SearchFilter):
    def get_search_results(self, request, queryset, view):
        search_terms = self.get_search_terms(request)

        if not search_terms:
            return queryset, False

        query = search_terms[0]
        algolia_results = raw_search(queryset.model, query)

        # Extract IDs from Algolia results
        ids = [hit['objectID'] for hit in algolia_results['hits']]
        filtered_queryset = queryset.filter(id__in=ids)

        return filtered_queryset, True
