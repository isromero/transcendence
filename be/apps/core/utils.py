def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "status": user.status,
    }

def serializer_friend(user):
    return {
        "id": user.id,
        "user_id": user.user_id,
        "friend_id": user.friend_id,
        "created_at": user.created_at,
        "status": user.status,
    }