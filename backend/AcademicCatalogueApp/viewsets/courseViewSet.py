from rest_framework.generics import ListAPIView
from AcademicCatalogueApp.models import Course
from AcademicCatalogueApp.serializers.courseSerializer import CourseSerializer
from django.db.models import Max, Min
from AcademicCatalogueApp.filters import CoursesFilter
from AcademicCatalogueApp.pagination import ResultsSetPagination


# This class is like a controller for the API endpoint of courses
class CourseViewSet(ListAPIView):
    serializer_class = CourseSerializer
    filterset_class = CoursesFilter
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        courses = Course.objects.exclude(times=None)

        # sort by time is a special case and we handle it in a different method
        if ("sortBy" in self.request.query_params and self.request.query_params["sortBy"] == "time"):
            return self.get_queryset_orderby_time(courses)

        if "sortBy" in self.request.query_params:
            order_string = self.request.query_params["sortBy"]
            if ("dir" in self.request.query_params and self.request.query_params["dir"] == "desc"):
                order_string = "-" + order_string
            courses = courses.order_by(order_string)

        return courses

    def get_queryset_orderby_time(self, course):
        # The SQL generated here might be optimised, but as number of courses is bound it does not matter
        if ("dir" in self.request.query_params and self.request.query_params["dir"] == "desc"):
            return course.annotate(Max("times__hour")).order_by("-times__hour__max")
        else:
            return course.annotate(Min("times__hour")).order_by("times__hour__min")
