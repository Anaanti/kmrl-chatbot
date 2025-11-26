from .views import test_pgvector

urlpatterns = [
    path("test/", test_pgvector),
]
