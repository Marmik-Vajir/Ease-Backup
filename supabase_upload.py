from supabase_config import supabase
import os

def upload_file_to_supabase(file_path):
    try:
        file_name = os.path.basename(file_path)

        with open(file_path, "rb") as f:
            supabase.storage.from_("files").upload(file_name,f)

        print(f"Uploaded: {file_name}")
        return True

    except Exception as e:
        print("Upload Error:", e)
        return False