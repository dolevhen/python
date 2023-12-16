user_profile = {
    "age": 24,
    "username": "dodo",
    "weapons": ["m16"],
    "is_active": True,
    "clan": "human"
}

# 1
print(user_profile.keys())
print(user_profile)
# 2
user_profile["weapons"].extend(['m4'])
print(user_profile)
# 3
user_profile.update({"is_banned": False})
# 4
user_profile["is_banned"] = True
print(user_profile)
# 5
user_profile2 = user_profile.copy()
user_profile2["username"] = "bobo"
user_profile2["age"] = 29
print(user_profile2)
