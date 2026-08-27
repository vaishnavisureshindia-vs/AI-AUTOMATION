"""
===============================================================================
SCRIPT NAME    : resource_lifecycle_pipeline.py
DESCRIPTION    : Composite CRUD & File Upload Automation Pipeline.
OBJECTIVE      : Execute full HTTP lifecycle operations (POST, PATCH, DELETE)
                 and multipart file uploads with structured logging.
PURPOSE        : Demonstrates how enterprise applications create, update, mutate,
                 and delete resources while transmitting binary files to remote APIs.
===============================================================================
"""

import json
import logging
import os
import requests

# 1. Initialize System Audit Logging
logging.basicConfig(
    filename="lifecycle_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Target mock endpoints for testing resource creation and mutation
api_base = "https://httpbin.org"

print("--- 🚀 Advanced Resource & File Lifecycle Pipeline ---")

# Dynamic inputs for resource creation
project_name = input("Enter new project title (e.g., Enterprise AI Core): ")
lead_owner = input("Enter project owner email: ")

# -----------------------------------------------------------------------------
# STAGE 1: CREATE RESOURCE (Day 16 - POST with JSON Payload)
# -----------------------------------------------------------------------------
print("\n[Stage 1] Creating new resource via POST...")
create_payload = {
    "title": project_name,
    "owner": lead_owner,
    "status": "draft",
    "tags": ["automation", "ai"],
}

try:
  # json= automatically converts dictionary to JSON string and sets Content-Type header
  response = requests.post(
      f"{api_base}/post", json=create_payload, timeout=5
  )
  response.raise_for_status()

  logging.info(f"POST Success: Resource created for '{project_name}'")
  print("✅ Resource Created Successfully!")
  print(f"Server Received Payload:\n{json.dumps(response.json().get('json'), indent=2)}")

except requests.exceptions.RequestException as err:
  logging.error(f"POST Failed: {err}")
  print(f"❌ Creation Error: {err}")
  exit(1)

# -----------------------------------------------------------------------------
# STAGE 2: MUTATE RESOURCE (Day 17 - PATCH for Partial Update)
# -----------------------------------------------------------------------------
print("\n[Stage 2] Updating status via PATCH...")
update_payload = {"status": "production", "version": "1.0.0"}

try:
  # PATCH modifies specific fields without touching the rest of the record
  response = requests.patch(
      f"{api_base}/patch", json=update_payload, timeout=5
  )
  response.raise_for_status()

  logging.info("PATCH Success: Resource updated to 'production'")
  print("✅ Resource Updated Successfully!")
  print(f"Updated Fields:\n{json.dumps(response.json().get('json'), indent=2)}")

except requests.exceptions.RequestException as err:
  logging.error(f"PATCH Failed: {err}")
  print(f"❌ Update Error: {err}")

# -----------------------------------------------------------------------------
# STAGE 3: MULTIPART FILE UPLOAD (Day 18 - Uploading Attachments)
# -----------------------------------------------------------------------------
print("\n[Stage 3] Executing Multipart File Upload...")

# Create a sample text report file on the fly for upload testing
dummy_filename = "project_manifest.txt"
with open(dummy_filename, "w") as f:
  f.write(f"Project Manifest: {project_name}\nOwner: {lead_owner}\nStatus: Active")

try:
  # Open file in binary read mode ('rb') and send via files parameter
  with open(dummy_filename, "rb") as file_stream:
    upload_payload = {"file": (dummy_filename, file_stream, "text/plain")}
    response = requests.post(
        f"{api_base}/post", files=upload_payload, timeout=10
    )
    response.raise_for_status()

  logging.info(f"Upload Success: Attached '{dummy_filename}' to server.")
  print(f"✅ File '{dummy_filename}' Uploaded Successfully!")

except requests.exceptions.RequestException as err:
  logging.error(f"Upload Failed: {err}")
  print(f"❌ Upload Error: {err}")

finally:
  # Clean up local temporary file
  if os.path.exists(dummy_filename):
    os.remove(dummy_filename)

# -----------------------------------------------------------------------------
# STAGE 4: DESTROY RESOURCE (Day 17 - DELETE Operation)
# -----------------------------------------------------------------------------
print("\n[Stage 4] Deleting resource via DELETE...")

try:
  response = requests.delete(f"{api_base}/delete", timeout=5)
  response.raise_for_status()

  logging.info("DELETE Success: Resource decommissioned from remote server.")
  print("✅ Resource Deleted Successfully!")

except requests.exceptions.RequestException as err:
  logging.error(f"DELETE Failed: {err}")
  print(f"❌ Deletion Error: {err}")

print("\n🎉 Pipeline Execution Finished. Check 'lifecycle_audit.log' for audit trail.")