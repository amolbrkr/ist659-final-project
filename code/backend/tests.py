from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_create_player_successful():
    # Test case for successful player creation
    response = client.post("/create-player", 
        json={
            "firstname": "Database",
            "lastname": "Dictators",
            "username": "DataD",
            "password": "password123"
            })
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,  # Replace with the actual player ID
        "firstname": "Database",
        "lastname": "Dictators",
        "username": "DataD",
        "balance": 0,  # Assuming the initial balance is 0
    }

def test_create_player_duplicate_username():
    # Test case for duplicate username (IntegrityError)
    response = client.post("/create-player", 
        json={
            "firstname": "Alice",
            "lastname": "Smith",
            "username": "DataD",  # This username already exists
            "password": "password456"
            })
    assert response.status_code == 400
    assert "Player name already exists" in response.text

def test_create_player_missing_data():
    # Test case for missing data (e.g., missing 'username')
    response = client.post("/create-player", 
        json={
            "firstname": "Database",
            "lastname": "Dictators",
            "password": "password789"
            })
    assert response.status_code == 422  # Expecting a validation error
    assert "field required" in response.text  # Check for a validation error message

def test_login_successful():
    # Test case for successful login
    response = client.post("/login", 
        json={
        "username": "DataD", 
        "password": "password123"
        })
    assert response.status_code == 200
    assert response.json() == {
        "loginSuccess": True,
        "player": 1,  # Replace with the actual player ID
        "firstname": "Database",
        "lastname": "Dictators",
        "username": "DataD",
        "balance": 0,  # Assuming the initial balance is 0
    }

def test_login_invalid_credentials():
    # Test case for invalid credentials (wrong password)
<<<<<<< Updated upstream
    response = client.post("/login", 
        json={
            "username": "DataD", 
            "password": "invalid_password"
            })
=======

    response = client.post(
        "/login", json={"username": "DataD", "password": "invalid_password"}
    )
>>>>>>> Stashed changes
    assert response.status_code == 404
    assert "Player not found, resubmit username or password." in response.text

def test_login_nonexistent_user():
    # Test case for a non-existent user
    response = client.post("/login", 
        json={
            "username": "nonexistent_user", 
            "password": "password123"
            })
    assert response.status_code == 404
    assert "Player not found, resubmit username or password." in response.text

def test_create_lobby_successful():
    # Test case for successful lobby creation
<<<<<<< Updated upstream
    response = client.post("/create-lobby", 
        json={"hostplayerID": 1})  # Replace with a valid host player ID
    assert response.status_code == 200
    assert "hostPlayerId" in response.json()  # Check if the response contains the hostPlayerId
=======
    response = client.post(
        "/create-lobby", json={"hostplayerID": 1}
    )  # Replace with a valid host player ID

    assert response.status_code == 200
    assert (
        "hostPlayerId" in response.json()
    )  # Check if the response contains the hostPlayerId

>>>>>>> Stashed changes

def test_create_lobby_nonexistent_host_player():
    # Test case for a host player that doesn't exist
    response = client.post("/create-lobby", 
        json={"hostplayerID": 999})  # Use a non-existent player ID
    assert response.status_code == 404
    assert "Player does not exist" in response.text  # Check for the error message

def test_create_lobby_when_host_player_already_in_lobby():
    # Test case for trying to create a lobby when the host player is already in one
    response = client.post("/create-lobby", 
        json={"hostplayerID": 1})  # Replace with a valid host player ID
    assert response.status_code == 404
<<<<<<< Updated upstream
    assert "Player is already in a lobby" in response.text  # Check for the error message
=======
    assert (
        "Player is already in a lobby" in response.text
    )  # Check for the error message

>>>>>>> Stashed changes

# Test case for successful player joining a lobby
def test_join_lobby_successful():
    # Assuming there's an existing player with ID 1 and an existing lobby with ID 2
    response = client.post("/join-lobby", 
        json={
            "playerId": 1, 
            "lobbyId": 2
            })
    assert response.status_code == 200
    assert "Player joined the lobby." in response.json()["message"]

# Test case for a non-existent player trying to join a lobby
def test_join_lobby_nonexistent_player():
    # Assuming there's no player with ID 999
    response = client.post("/join-lobby", 
        json={
            "playerId": 999, 
            "lobbyId": 2
            })
    assert response.status_code == 404
    assert "Player not found." in response.text

# Test case for attempting to join a full lobby
def test_join_lobby_full_lobby():
    # Assuming there's an existing lobby with ID 3 and its maximum player limit is reached
<<<<<<< Updated upstream
    response = client.post("/join-lobby", 
        json={
            "playerId": 1, 
            "lobbyId": 3
            })
    assert response.status_code == 200  # You can replace this with the expected status code for a full lobby
=======

    response = client.post("/join-lobby", json={"playerId": 1, "lobbyId": 3})

    assert (
        response.status_code == 200
    )  # You can replace this with the expected status code for a full lobby
>>>>>>> Stashed changes
    assert f"Lobby {3} is full." in response.json()["message"]

# Test case for successful card dealing
def test_deal_cards_successful():
    # Assuming there's an existing lobby with ID 1
    response = client.post("/deal-cards", 
        json={"lobby_id": 1})
    assert response.status_code == 200
    assert "lobby" in response.json()  # Check if the response contains the lobby ID

# Test case for dealing cards for a non-existent lobby
def test_deal_cards_nonexistent_lobby():
    # Assuming there's no lobby with ID 999
    response = client.post("/deal-cards", 
        json={"lobby_id": 999})
    assert response.status_code == 404
    assert f"No lobby with id: {999}" in response.text  # Check for the error message

# Test case for dealing cards when the lobby turn count is not incremented
def test_deal_cards_turn_not_incremented():
    # Assuming there's an existing lobby with ID 2 but its turn count is not incremented
<<<<<<< Updated upstream
    response = client.post("/deal-cards", 
        json={"lobby_id": 2})
    assert response.status_code == 200  # You can replace this with the expected status code for a turn not incremented
    assert "turn" in response.json()  # Check if the response contains the updated turn count
=======

    response = client.post("/deal-cards", json={"lobby_id": 2})

    assert (
        response.status_code == 200
    )  # You can replace this with the expected status code for a turn not incremented
    assert (
        "turn" in response.json()
    )  # Check if the response contains the updated turn count

>>>>>>> Stashed changes

# Test case for a player winning
def test_play_player_win():
    # Assuming there's an existing lobby with ID 1 and player with ID 1
    response = client.post("/play", 
        json={
            "lobby_id": 1, 
            "player_id": 1, 
            "action": "bet", 
            "turn": 1, 
            "ante_amount": 10
            })
    assert response.status_code == 200
    assert response.json() == {"outcome": "player_win"}

# Test case for a dealer winning
def test_play_dealer_win():
    # Assuming there's an existing lobby with ID 2 and player with ID 2
    response = client.post("/play", 
        json={
            "lobby_id": 2, 
            "player_id": 2, 
            "action": "bet", 
            "turn": 2, 
            "ante_amount": 10
            })
    assert response.status_code == 200
    assert response.json() == {"outcome": "dealer_win"}

# Test case for a draw
def test_play_draw():
    # Assuming there's an existing lobby with ID 3 and player with ID 3
    response = client.post("/play", 
        json={
            "lobby_id": 3, 
            "player_id": 3, 
            "action": "bet", 
            "turn": 3, 
            "ante_amount": 10
            })
    assert response.status_code == 200
    assert response.json() == {"outcome": None}

# Test case for a valid fold action
def test_fold_valid():
    # Assuming there's an existing player with ID 1 and ante amount of 10
    response = client.post("/fold", json={"player_id": 1, "ante_amount": 10})

    assert response.status_code == 200
    assert response.json() == {
        "balance": 0
    }  # Assuming the player's balance becomes 0 after folding


# Test case for folding with insufficient balance
def test_fold_insufficient_balance():
    # Assuming there's an existing player with ID 2 and ante amount of 100

    response = client.post("/fold", json={"player_id": 2, "ante_amount": 100})

    assert (
        response.status_code == 400
    )  # Assuming you return a 400 Bad Request when the balance is insufficient
    assert response.json() == {"error": "Insufficient balance"}

# Test case for folding by a non-existing player
def test_fold_player_not_found():
    # Assuming there's no player with ID 3
<<<<<<< Updated upstream
    response = client.post("/fold", 
        json={
            "player_id": 3, 
            "ante_amount": 10
            })
    assert response.status_code == 404  # Assuming you return a 404 Not Found when the player is not found
=======

