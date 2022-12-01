import pytest as pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def count():
    return Course.objects.count()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_cours(client, course_factory):
    cours = course_factory(_quantity=1)
    responce = client.get('/api/v1/courses/1/')
    data = responce.json()
    assert responce.status_code == 200
    assert cours[0].name == data['name']


@pytest.mark.django_db
def test_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    responce = client.get('/api/v1/courses/')
    assert responce.status_code == 200
    data = responce.json()
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_id(client, course_factory):
    courses = course_factory(_quantity=10)
    cours_id = courses[5].id
    responce = client.get(f'/api/v1/courses/?id={cours_id}')
    assert responce.status_code == 200
    data = responce.json()
    assert data[0]['id'] == cours_id


@pytest.mark.django_db
def test_name(client, course_factory):
    courses = course_factory(_quantity=10)
    cours_name = courses[5].name
    responce = client.get(f'/api/v1/courses/?name={cours_name}')
    assert responce.status_code == 200
    data = responce.json()
    assert data[0]['name'] == cours_name


@pytest.mark.django_db
def test_create(client, count):
    student = Student.objects.create(name='admin')
    responce = client.post('/api/v1/courses/', data={'name': 'Test', 'students': [student.id]}, format='json')
    assert responce.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update(client):
    student = Student.objects.create(name='admin')
    responce = client.post('/api/v1/courses/', data={'name': 'Test', 'students': [student.id]}, format='json')
    assert responce.status_code == 201
    data_original = responce.json()
    responce = client.patch(f'/api/v1/courses/{data_original["id"]}/', data={'name': 'Test2', 'students': [student.id]}, format='json')
    data_new = responce.json()
    assert responce.status_code == 200
    assert data_original["name"] != data_new["name"]


@pytest.mark.django_db
def test_delete(client, count):
    student = Student.objects.create(name='admin')
    responce = client.post('/api/v1/courses/', data={'name': 'Test', 'students': [student.id]}, format='json')
    assert responce.status_code == 201
    assert Course.objects.count() == count + 1
    data = responce.json()
    client.delete(f'/api/v1/courses/{data["id"]}/')
    assert responce.status_code == 201
    assert Course.objects.count() == count
