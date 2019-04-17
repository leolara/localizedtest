from AcademicCatalogueApp.viewsets.courseViewSet import CourseViewSet
from django.urls import path

app_name = "AcademicCatalogueApp"

urlpatterns = [path("courses", CourseViewSet.as_view())]
