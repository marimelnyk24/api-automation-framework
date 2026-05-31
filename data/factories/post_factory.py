import random

from faker import Faker

from data.models.post import Post

fake = Faker()


class PostFactory:

    @staticmethod
    def create(**kwargs) -> Post:
        defaults = {
            "userId": random.randint(1, 10),
            "id": None,
            "title": fake.sentence(),
            "body": fake.text()
        }

        defaults.update(kwargs)

        return Post(**defaults)