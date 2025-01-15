import unreal
import tkinter as tk
from tkinter import filedialog


def import_fbx_with_existing_skeleton(fbx_file_path, destination_path, skeleton_asset_path):
    # this function will allow the user to select an animation to import and then it will import that animation with all these preset settings.  That way the user does not need to modify import settings every time they import animations into unreal as part of this pipeline.

    root = tk.Tk()
    root.withdraw()

    # Initialize AssetTools and Import Tasks
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    import_task = unreal.AssetImportTask()

    import_task.filename = fbx_file_path  # Path to FBX file we want to import
    import_task.destination_path = destination_path  # Unreal Engine folder we want to import the animations to
    import_task.replace_existing = True # will replace file with the same name if needed, this will allow the user to easily update changes made to the animation
    import_task.automated = True
    import_task.save = True

    # Set up FBX import options
    options = unreal.FbxImportUI()
    options.automated_import_should_detect_type = False
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION # Allows us to import the animation without the skeletal mesh, the skeletal mesh is already in engine 
    options.import_mesh = False  
    options.import_animations = True  # Enable animation import 
    options.import_materials = False
    options.import_textures = False
    options.create_physics_asset = False

    # Assigns the skeleton that animation will be imported onto
    skeleton_asset = unreal.EditorAssetLibrary.load_asset(skeleton_asset_path)
    if skeleton_asset:
        # Assign the skeleton to the options
        options.skeleton = skeleton_asset
        print(f"Using skeleton: {skeleton_asset.get_name()}")
    else:
        print(f"Error: Skeleton asset at {skeleton_asset_path} not found.")
        return  # Exit the function if skeleton is not found

    # Assign options to the import task
    import_task.options = options

    # Perform the import task
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])

    print(f"FBX Import Complete: {fbx_file_path} -> {destination_path}")

# Run the importer
if __name__ == "__main__":

   fbx_file = filedialog.askopenfile(mode='r', title="Select FBX File", filetypes=[("FBX Files", "*.fbx")]) #will open a windows dialog so that the user can choose which file to import
   
   if fbx_file:
        FBX_FILE_PATH = fbx_file.name  # Get the file path as a string
        DESTINATION_PATH = "/Game/Frankie/Animation"  # The Unreal folder where the animation will be imported
        SKELETON_ASSET_PATH = '/Game/Frankie/Mesh/FrankieBody_Export_Skeleton'  # Path to the existing skeleton asset in Unreal

        # Run the function to import the FBX with the existing skeleton
        import_fbx_with_existing_skeleton(FBX_FILE_PATH, DESTINATION_PATH, SKELETON_ASSET_PATH)
else:
        print("No file selected.")