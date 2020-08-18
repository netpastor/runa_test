import json

from django.test import Client
from django.urls import reverse


def test_create_categories(db):
    client = Client()

    data = {
        "name": "Category 1",
        "children": [
            {
                "name": "Category 1.1",
                "children": [
                    {
                        "name": "Category 1.1.1",
                        "children": [
                            {"name": "Category 1.1.1.1"},
                            {"name": "Category 1.1.1.2"},
                            {"name": "Category 1.1.1.3"},
                        ],
                    },
                    {
                        "name": "Category 1.1.2",
                        "children": [
                            {"name": "Category 1.1.2.1"},
                            {"name": "Category 1.1.2.2"},
                            {"name": "Category 1.1.2.3"},
                        ],
                    },
                ],
            },
            {
                "name": "Category 1.2",
                "children": [
                    {"name": "Category 1.2.1"},
                    {
                        "name": "Category 1.2.2",
                        "children": [
                            {"name": "Category 1.2.2.1"},
                            {"name": "Category 1.2.2.2"},
                        ],
                    },
                ],
            },
        ],
    }

    response = client.post(
        path=reverse("categories-list"), data={"body": json.dumps(data)}
    )
    assert response.status_code == 201

    response = client.get(path=reverse("categories-detail", args=[1, ]))
    response_data = response.json()

    assert all(
        (
            response.status_code == 200,
            len(response_data["parents"]) == 0,
            len(response_data["children"]) == 2,
            len(response_data["siblings"]) == 0,
        )
    )

    response = client.get(path=reverse("categories-detail", args=[2, ]))
    response_data = response.json()

    assert all(
        (
            response.status_code == 200,
            len(response_data["parents"]) == 1,
            len(response_data["children"]) == 2,
            len(response_data["siblings"]) == 1,
        )
    )

    response = client.get(path=reverse("categories-detail", args=[8, ]))
    response_data = response.json()

    assert all(
        (
            response.status_code == 200,
            len(response_data["parents"]) == 3,
            len(response_data["children"]) == 0,
            len(response_data["siblings"]) == 2,
        )
    )
