import json
import os

def load_users(file_path='data.json'):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "..", "data.json")
        data_path = os.path.normpath(data_path)
        
        # Đọc file JSON
        with open(data_path, 'r', encoding='utf-8') as file:
            users = json.load(file)
            
        # Kiểm tra dữ liệu
        if isinstance(users, list):
            return users
        else:
            print(f"Warning: Expected list but got {type(users)}")
            return []
            
    except FileNotFoundError:
        print(f"Error: File {data_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return []
    except Exception as e:
        print(f"Error loading users: {e}")
        return []
