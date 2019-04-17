from AcademicCatalogueApp.models import Course
import django_filters

# Enables that we can filter for each field of course
class CoursesFilter(django_filters.FilterSet):
    times_hour = django_filters.CharFilter(method="filter_hour")
    name = django_filters.CharFilter(lookup_expr="icontains")
    professor = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Course
        fields = "__all__"

    def filter_hour(self, queryset, hour, value):
        return queryset.filter(times__hour=value)
