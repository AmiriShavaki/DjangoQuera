from django.test import TestCase
from classes.serializers import ClassroomSerializer

class SerializerTest(TestCase):
    def test_cap_cor(self):
        data = {"capacity":5, "name":"mamad", "department":"main", "area":0}
        seri = ClassroomSerializer(data=data)
        assert seri.is_valid()

    def test_cap_wrong(self):
        data = {"capacity":4, "name":"mamad", "department":"main", "area":0}
        seri = ClassroomSerializer(data=data)
        assert not seri.is_valid()
    def test_cap_wrong2(self):
        data = {"capacity":5, "name":"mamad", "department":"main", "area":-1}
        seri = ClassroomSerializer(data=data)
        assert not seri.is_valid() 
    def test_cap_wrong3(self):
        data = {"capacity":4, "name":"mamad", "department":"main", "area":-0.1}
        seri = ClassroomSerializer(data=data)
        assert not seri.is_valid()