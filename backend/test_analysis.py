import cv2
import services.analysis_service as analysis_service

# --- IMPORTANT ---
# 1. Place an image of a single cow or buffalo in your `backend/` folder.
# 2. Change the file name below to match your test image.
TEST_IMAGE_PATH = "backend/test_cow.jpg" 

def main():
    print("--- Starting Analysis Test ---")
    
    # 1. Check if the image exists
    image = cv2.imread(TEST_IMAGE_PATH)
    if image is None:
        print(f"❌ ERROR: Cannot find the test image at '{TEST_IMAGE_PATH}'.")
        print("Please make sure the image is in the 'backend/' folder and the path is correct.")
        return

    print(f"✅ Found test image: {TEST_IMAGE_PATH}")

    # 2. Run the full analysis function
    try:
        print("\nRunning the analysis service...")
        result = analysis_service.run_full_analysis(TEST_IMAGE_PATH)

        if result is None:
            print("\n- - - - - - - - - - - - - - - - - -")
            print("✅ SUCCESS: The service correctly identified that no valid animal was found.")
            print("- - - - - - - - - - - - - - - - - -")

        else:
            print("\n- - - - - - - - - - - - - - - - - -")
            print("✅ SUCCESS: Analysis completed without errors!")
            print("\nDetected Class:", result.get("class_name"))
            print("Overall Score:", result["scores"].get("overall_score"))
            print("Trait Scores:", result["scores"].get("trait_scores"))
            print("Annotated image saved at:", result.get("annotated_image_path"))
            print("- - - - - - - - - - - - - - - - - -")

    except Exception as e:
        print("\n- - - - - - - - - - - - - - - - - -")
        print("❌ FAILED: The analysis crashed with an error.")
        print("\n--- ERROR DETAILS ---")
        import traceback
        traceback.print_exc()
        print("---------------------")

if __name__ == "__main__":
    main()



    
