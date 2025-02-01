def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "is_online": user.is_online,
    }


def serializer_friends(user):
    return {
        "id": user.id,
        "user_id": user.user_id,
        "friend_id": user.friend_id,
        "created_at": user.created_at,
        "status": user.status,
    }
