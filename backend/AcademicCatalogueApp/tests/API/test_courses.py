from rest_framework.test import APITestCase


class APIGetTests(APITestCase):
    fixtures = ["fixtures"]
    url = "http://localhost:8000/api/courses"

    def test_get_basic(self):
        """
        Ensure plain GET works
        """
        url = "http://localhost:8000/api/courses"
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_get_page_size_12(self):
        """
        The first page returns the number of items that we want per page
        """
        response = self.client.get(self.url + "?page_size=12")
        self.assertEqual(len(response.data["results"]), 12)

    def test_get_page_size_12_page17(self):
        """
        The last page returns 3 items
        """
        response = self.client.get(self.url + "?page_size=12&page=6")
        self.assertEqual(len(response.data["results"]), 3)

    def test_get_page_filter(self):
        """
        There are four courses that contain Man in the name
        """
        response = self.client.get(self.url + "?name=Man")
        self.assertEqual(len(response.data["results"]), 4)
