from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    print(f"Posts are: {res}")
    #def validate(post):
        #return schemas.PostOut(**post)
    #posts_map = map(validate,res.json())
    posts_list = [schemas.PostOut(**post) for post in res.json()]
    print(posts_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_found(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/9999")
    assert res.status_code == 404   

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("My first title", "My first content", True),
    ("My second title", "My second content", False),
    ("My third title", "My third content", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content  
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={"title": "My title", "content": "My content"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "My title"     
    assert created_post.content == "My content"  
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={"title": "My title", "content": "My content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_Post(client, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_found(authorized_client):
    res = authorized_client.delete(f"/posts/9999")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")  # test_posts[3] is owned by test_user2
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "published": False
    }
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.published == data['published']

def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "published": False
    }
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}", json=data)  # test_posts[3] is owned by test_user2
    assert res.status_code == 403

def test_update_post_not_found(authorized_client):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "published": False
    }
    res = authorized_client.put(f"/posts/9999", json=data)
    assert res.status_code == 404

def test_unauthorized_user_update_post(client, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "published": False
    }
    res = client.put(
        f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401