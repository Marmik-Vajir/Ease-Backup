import time
import os
from datetime import datetime
import firebase_config
from supabase_upload import upload_file_to_supabase
from google_drive_upload import upload_to_drive

def check_and_backup():
    print("Checking for files...")

    files = firebase_config.db.collection("files").stream()

    high = []
    medium = []
    low = []

    # categorized
    for file in files:
        data = file.to_dict()
        doc_id = file.id

        if data.get("status") != "Waiting":
            continue

        priority = data.get("priority")

        if priority == "High":
            high.append((doc_id, data))
        elif priority == "Medium":
            medium.append((doc_id, data))
        else:
            low.append((doc_id, data))

    # order execution (outside loop)
    execution_list = high + medium + low

    # execute (outside looop)
    for doc_id, data in execution_list:
      try:
        file_path = data.get("file_path")
        file_name = data.get("file_name")

        print(f"Uploading: {file_name}")

        # set status to Uploading
        firebase_config.db.collection("files").document(doc_id).update({
            "status": "Uploading"
        })

        # upload file
        # supabase_success = upload_file_to_supabase(file_path)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

        
        if file_size_mb < 50:
            supabase_success = upload_file_to_supabase(file_path)
        else:
            print("Skipped Supabase (file too large, max size 50MB)")
            supabase_success = True  # treat as success

        # upload to google drive
        drive_success = upload_to_drive(file_path, data.get("user_email"))

        # only complete if BOTH succeed
        if supabase_success and drive_success:
            firebase_config.db.collection("files").document(doc_id).update({
                "status": "Completed",
                "completion_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            firebase_config.db.collection("files").document(doc_id).update({
                "status": "Failed"
            })

        print(f"Completed: {file_name}")

      except Exception as e:
          print("error processing file: ", e)
          
# run continuous
def run_server():
    while True:
      check_and_backup()
      time.sleep(10)

if __name__ == "__main__":
    run_server()