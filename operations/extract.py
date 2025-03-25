'''import kaggle
def extract():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('olistbr/brazilian-ecommerce',path='./data', unzip=True)'''
import kaggle
import os

def extract():
    try:
        # Step 1: Authenticate
        print("Authenticating with Kaggle API...")
        kaggle.api.authenticate()
        print("Authentication successful.")
        
        # Step 2: Define the dataset path and check if the folder exists
        dataset_path = './data'
        dataset_name = 'olistbr/brazilian-ecommerce'
        
        # If the dataset folder doesn't exist, create it
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
        
        # Check if the folder is already populated with files
        if len(os.listdir(dataset_path)) > 0:
            print(f"⚠️ Dataset already exists in {dataset_path}. Skipping download.")
        else:
            print("Starting to download the dataset...")
            
            # Download and unzip the dataset, force overwrite if needed
            kaggle.api.dataset_download_files(dataset_name, path=dataset_path, unzip=True, force=True)
            
            # Verify files were downloaded
            if len(os.listdir(dataset_path)) > 0:
                print(f"✅ Dataset downloaded and unzipped successfully to {dataset_path}")
            else:
                print("❌ Dataset download failed or no files found.")
    
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Call the function
extract()
