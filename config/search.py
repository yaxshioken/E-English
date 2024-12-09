from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        search_fields = []
        if request.query_params.get("name_only"):
            search_fields.append("name")
        if request.query_params.get("level_only"):
            search_fields.append("level")
        if request.query_params.get("unit_num_only"):
            search_fields.append("unit_num")
        if request.query_params.get("book_only"):
            search_fields.append("book")
        if request.query_params.get("en_only"):
            search_fields.append("en")
        if request.query_params.get("uzonly"):
            search_fields.append("uz")
        if request.query_params.get("unit_only"):
            search_fields.append("unit")
        if search_fields:
            return search_fields

        return super().get_search_fields(view, request)