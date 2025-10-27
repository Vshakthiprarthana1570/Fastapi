import pytest
from app import models

@pytest.fixture
def test_vote(session, test_user, test_posts):
    new_vote = models.Vote(post_id = test_posts[0].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()    
    return new_vote
    
def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_on_post(authorized_client, test_vote, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409

def test_remove_vote(authorized_client, test_vote, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201

def test_remove_nonexistent_vote(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[1].id, "dir": 0})
    assert res.status_code == 404

def test_vote_on_nonexistent_post(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 9999, "dir": 1})
    assert res.status_code == 404

def test_unauthorized_vote(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401   

