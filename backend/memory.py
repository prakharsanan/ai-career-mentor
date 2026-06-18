from collections import defaultdict

chat_memory = defaultdict(list)

def add_message(session_id, role, content):
    chat_memory[session_id].append(
        {
            "role": role,
            "content": content
        }
    )

def get_history(session_id):
    return chat_memory[session_id]