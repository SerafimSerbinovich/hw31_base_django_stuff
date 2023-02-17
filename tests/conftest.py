from pytest_factoryboy import register
from tests.factories import AdFactory, CategoryFactory, UserFactory

pytest_plugins = "tests.fixtures"

register(CategoryFactory)
register(UserFactory)
register(AdFactory)
