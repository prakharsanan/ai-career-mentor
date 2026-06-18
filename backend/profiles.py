profiles = {}

def get_profile(session_id):
    if session_id not in profiles:
        profiles[session_id] = {
            "name": "",
            "education": "",
            "interests": []
        }

    return profiles[session_id]