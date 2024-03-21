## Wait Socket

### 1. [Front] Back에게 게임 신청

- `ws/general_game/wait` 웹소켓 연결 요청

### 2. [Back] 대기 명단에 넣음

### 3. [Back] 게임 인원 충족 시, game_id 전송

```json
{
    "game_id": {game_id}
}
```

### 4. [Front] wait 소켓 종료

## Game Socket

### 1. [Front] 게임 페이지로 이동 및 소켓 연결 요청

- `ws/general_game/{game_id}` 웹소켓 연결 요청

### 2. [Back] 클라이언트에게 ready 전송

```json
{
  "message_type": "ready",
  "intra_id": {intra_id},
  "number": "player1" or "player2"
}
```

### 3. [Front] ready 수신하고 Back에게 ready 전송

```json
{
  "message_type": "ready",
  "intra_id": {intra_id},
  "number": "player1" or "player2"
}
```

### 4. [Back] 클라이언트에게 start 전송

- 양쪽에게 ready 메시지를 수신하면 start 메시지를 전송

```json
{
  "message_type": "start",
  "1p": {intra_id},
  "2p": {intra_id}
}
```

### 5. 