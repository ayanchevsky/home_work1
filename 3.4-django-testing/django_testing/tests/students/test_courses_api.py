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


# создаем курс через фабрику
@pytest.mark.django_db
def test_cours(client, course_factory):
    cours = course_factory()
    responce = client.get(f'/api/v1/courses/{cours.id}/')
    data = responce.json()
    assert responce.status_code == 200
    assert cours.name == data['name']


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    responce = client.get('/api/v1/courses/')
    assert responce.status_code == 200
    data = responce.json()
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_id(client, course_factory):
    courses = course_factory(_quantity=10)
    # rnd = random.randint(1, 10)
    # cours_id = courses[rnd].id
    cours_id = courses[5].id
    responce = client.get(f'/api/v1/courses/?id={cours_id}')
    assert responce.status_code == 200
    data = responce.json()
    assert data[0]['id'] == cours_id


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_name(client, course_factory):
    courses = course_factory(_quantity=10)
    # rnd = random.randint(1, 10)
    # cours_id = courses[rnd].name
    cours_name = courses[5].name
    responce = client.get(f'/api/v1/courses/?name={cours_name}')
    assert responce.status_code == 200
    data = responce.json()
    assert data[0]['name'] == cours_name


# тест успешного создания курса
@pytest.mark.django_db
def test_create(client, course_factory, count):
    # student = Student.objects.create(name='admin')
    # responce = client.post('/api/v1/courses/', data={'name': 'Test', 'students': [student.id]}, format='json')
    cours = course_factory()
    responce = client.get(f'/api/v1/courses/?name={cours.name}')
    assert responce.status_code == 200
    assert Course.objects.count() == count + 1


# тест успешного обновления курса
@pytest.mark.django_db
def test_update(client, course_factory):
    # student = Student.objects.create(name='admin')
    # responce = client.post('/api/v1/courses/', data={'name': 'Test', 'students': [student.id]}, format='json')
    courses = course_factory()
    responce = client.patch(f'/api/v1/courses/{courses.id}/', data={'name': 'Test2'}, format='json')
    data_new = responce.json()
    assert responce.status_code == 200
    assert courses.name != data_new["name"]


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete(client, course_factory, count):
    # student = Student.objects.create(name='admin')
    # responce = client.post('/api/v1/courses/', data={'name': 'Test', 'students': [student.id]}, format='json')
    courses = course_factory()
    assert Course.objects.count() == count + 1
    responce = client.delete(f'/api/v1/courses/{courses.id}/')
    assert responce.status_code == 204
    assert Course.objects.count() == count
