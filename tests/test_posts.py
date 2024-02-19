import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    def validate(post):
        print(post)
        return schemas.PostResponse(**(post["Post"]))

    post_map = map(validate, res.json())
    posts = list(post_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts")
    assert res.status_code == 401


def test_get_unexistent_post(authorized_client):
    res = authorized_client.get("/posts/0")
    assert res.status_code == 404


def test_get_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponse(**res.json()["Post"])
    assert res.status_code == 200
    assert post.id == test_posts[0].id


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("awesome new title", "awesome new content", True),
        ("favourite pizza", "i love queso katupyry", False),
        ("clickiest click sound", "click", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user.id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts", json={"title": "should be true", "content": "idk if published"}
    )
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "should be true"
    assert created_post.content == "idk if published"
    assert created_post.published == True
    assert created_post.user.id == test_user["id"]


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/posts", json={"title": "should be true", "content": "idk if published"}
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_unexistent_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/0")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_user_2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_unauthorized_user_udpate_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_unexistent_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put("/posts/800000", json=data)
    assert res.status_code == 404
