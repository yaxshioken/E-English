import django_filters

from essential.models import Vocab


class VocabFilter(django_filters.FilterSet):
    en = django_filters.CharFilter(lookup_expr='icontains')
    uz = django_filters.CharFilter(lookup_expr='icontains')
    unit = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Vocab
        fields = ['en', 'uz', 'unit']