import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import customtkinter as ctk

# NOTE: Update 2025-01-07 by HunMin Kim - Add a Class for initial settings
class InitialSettings:
    def __init__(self):
        self.language = None
        self.participant_name = None
        self.parent_directory = None
        self.process_mode = None
        self.num_trials = 0  # Added for batch mode

    def select_language(self, root):
        # Create a frame for language selection
        lang_frame = ctk.CTkFrame(root)
        lang_frame.pack(expand=True, fill='both')

        def set_language(lang):
            if lang == 'fr':
                messagebox.showinfo("Not Implemented", "French language support is not yet implemented.")
                return
            self.language = lang
            # Prompt the user to enter the participant name
            participant_name = simpledialog.askstring(
                title="Participant Name",
                prompt="Please enter the participant name:"
            )
            if not participant_name:
                # If no name is entered, set a default name
                participant_name = 'Participant'
            self.participant_name = participant_name.strip()
            
            # Select parent directory
            self.select_parent_directory(root, lang_frame)

        # Language selection buttons
        ctk.CTkLabel(lang_frame, text="Select Language / Choisir la langue",
                     font=('Helvetica', 20, 'bold')).pack(pady=40)
        ctk.CTkButton(lang_frame, text="English", command=lambda: set_language('en'),
                      width=200, height=50, font=('Helvetica', 18)).pack(pady=20)
        ctk.CTkButton(lang_frame, text="Français (coming soon)", command=lambda: set_language('fr'),
                      width=200, height=50, font=('Helvetica', 18)).pack(pady=20)

    # NOTE: Update 2025-01-07 by HunMin Kim - Add a function to select the parent directory
    def select_parent_directory(self, root, previous_frame):
        # Clear previous frame
        previous_frame.destroy()

        # Create a frame for directory selection
        dir_frame = ctk.CTkFrame(root)
        dir_frame.pack(expand=True, fill='both')

        # Create label
        ctk.CTkLabel(dir_frame, text="Select Parent Directory",
                     font=('Helvetica', 20, 'bold')).pack(pady=20)

        # Create frame for path display and button
        path_frame = ctk.CTkFrame(dir_frame)
        path_frame.pack(pady=20, padx=20, fill='x')

        # Path display
        path_var = ctk.StringVar(value=os.getcwd())  # Default to current directory
        path_entry = ctk.CTkEntry(path_frame, textvariable=path_var, width=400)
        path_entry.pack(side='left', padx=(0, 10))

        def browse_directory():
            directory = filedialog.askdirectory(initialdir=path_var.get())
            if directory:
                path_var.set(directory)

        # Browse button
        browse_btn = ctk.CTkButton(path_frame, text="Browse", command=browse_directory)
        browse_btn.pack(side='right')

        def confirm_directory():
            self.parent_directory = path_var.get()
            dir_frame.destroy()
            self.choose_process_mode(root, dir_frame)

        # Confirm button
        confirm_btn = ctk.CTkButton(dir_frame, text="Confirm", command=confirm_directory,
                                   width=200, height=50, font=('Helvetica', 18))
        confirm_btn.pack(pady=20)

    def choose_process_mode(self, root, previous_frame):
        # Clear previous frame
        previous_frame.destroy()

        # Create a new frame for process mode selection
        mode_frame = ctk.CTkFrame(root)
        mode_frame.pack(expand=True, fill='both')

        def set_mode(mode):
            self.process_mode = mode
            mode_frame.destroy()
            
            # If batch mode, prompt for number of trials
            if mode == 'batch':
                self.prompt_number_of_trials(root)
            else:
                # Return control to main GUI
                if hasattr(self, 'on_settings_complete'):
                    self.on_settings_complete()

        # Process mode selection buttons
        ctk.CTkLabel(mode_frame, text="Select Process Mode / Sélectionnez le mode de traitement",
                     font=('Helvetica', 20, 'bold')).pack(pady=40)
        ctk.CTkButton(mode_frame, text="Single", command=lambda: set_mode('single'),
                      width=200, height=50, font=('Helvetica', 18)).pack(pady=20)
        ctk.CTkButton(mode_frame, text="Batch", command=lambda: set_mode('batch'),
                      width=200, height=50, font=('Helvetica', 18)).pack(pady=20)

    def prompt_number_of_trials(self, root):
        num_trials = simpledialog.askinteger("Batch Processing",
                                           "Enter the number of trials:",
                                           minvalue=1)
        if not num_trials:
            messagebox.showerror("Input Error", "Number of trials must be at least 1.")
            root.destroy()
            return
            
        self.num_trials = num_trials
        
        # Return control to main GUI
        if hasattr(self, 'on_settings_complete'):
            self.on_settings_complete()

    def start_initial_setup(self, root, callback=None):
        """Start the initial setup process"""
        if callback:
            self.on_settings_complete = callback
        self.select_language(root)


# NOTE: Update 2025-01-07 by HunMin Kim - Move the config_template from GUI.py to settings.py
###############################################################################
config_template= r"""##########################################################
## PROJECT PARAMETERS                                                        ##
###############################################################################


# Configure your project parameters here. 
# 
# IMPORTANT:
# If a parameter is not found here, Pose2Sim will look for its value in the 
# Config.toml file of the level above. This way, you can set global 
# instructions for the Session and alter them for specific Participants or Trials.
#
# If you wish to overwrite a parameter for a specific trial or participant,  
# edit its Config.toml file by uncommenting its key (e.g., [project])
# and editing its value (e.g., frame_range = [10,300]). Or else, uncomment 
# [filtering.butterworth] and set cut_off_frequency = 10, etc.



[project]
multi_person = false # true for trials with multiple participants. If false, only the main person in scene is analyzed (and it run much faster). 
participant_height = 1.72 # m # float if single person, list of float if multi-person (same order as the Static trials) # Only used for marker augmentation
participant_mass = 70.0 # kg # Only used for marker augmentation and scaling

frame_rate = 'auto' # fps # int or 'auto'. If 'auto', finds from video (or defaults to 60 fps if you work with images) 
frame_range = [] # For example [10,300], or [] for all frames. 
## If cameras are not synchronized, designates the frame range of the camera with the shortest recording time
## N.B.: If you want a time range instead, use frame_range = time_range * frame_rate
## For example if you want to analyze from 0.1 to 2 seconds with a 60 fps frame rate, 
## frame_range = [0.1, 2.0]*frame_rate = [6, 120]

exclude_from_batch = [] # List of trials to be excluded from batch analysis, ['<participant_dir/trial_dir>', 'etc'].
# e.g. ['S00_P00_Participant/S00_P00_T00_StaticTrial', 'S00_P00_Participant/S00_P00_T01_BalancingTrial']

[pose]
vid_img_extension = 'mp4' # any video or image extension
pose_model = 'HALPE_26'  #With RTMLib: HALPE_26 (body and feet, default), COCO_133 (body, feet, hands), COCO_17 (body)
                         # /!\ Only RTMPose is natively embeded in Pose2Sim. For all other pose estimation methods, you will have to run them yourself, and then refer to the documentation to convert the files if needed
                         #With MMPose: HALPE_26, COCO_133, COCO_17, CUSTOM. See CUSTOM example at the end of the file
                         #With openpose: BODY_25B, BODY_25, BODY_135, COCO, MPII
                         #With mediapipe: BLAZEPOSE
                         #With alphapose: HALPE_26, HALPE_68, HALPE_136, COCO_133
                         #With deeplabcut: CUSTOM. See example at the end of the file
mode = 'balanced' # 'lightweight', 'balanced', 'performance'
det_frequency = 1 # Run person detection only every N frames, and inbetween track previously detected bounding boxes (keypoint detection is still run on all frames). 
                  # Equal to or greater than 1, can be as high as you want in simple uncrowded cases. Much faster, but might be less accurate. 
display_detection = true
overwrite_pose = false # set to false if you don't want to recalculate pose estimation when it has already been done
save_video = 'to_video' # 'to_video' or 'to_images', 'none', or ['to_video', 'to_images']
output_format = 'openpose' # 'openpose', 'mmpose', 'deeplabcut', 'none' or a list of them # /!\ only 'openpose' is supported for now


[synchronization]
display_sync_plots = true # true or false (lowercase)
keypoints_to_consider = ['RWrist'] # 'all' if all points should be considered, for example if the participant did not perform any particicular sharp movement. In this case, the capture needs to be 5-10 seconds long at least
                           # ['RWrist', 'RElbow'] list of keypoint names if you want to specify keypoints with a sharp vertical motion.
approx_time_maxspeed = 'auto' # 'auto' if you want to consider the whole capture (default, slower if long sequences)
                           # [10.0, 2.0, 8.0, 11.0] list of times (seconds) if you want to specify the approximate time of a clear vertical event for each camera
time_range_around_maxspeed = 2.0 # Search for best correlation in the range [approx_time_maxspeed - time_range_around_maxspeed, approx_time_maxspeed  + time_range_around_maxspeed]
likelihood_threshold = 0.4 # Keypoints whose likelihood is below likelihood_threshold are filtered out
filter_cutoff = 6 # time series are smoothed to get coherent time-lagged correlation
filter_order = 4


# Take heart, calibration is not that complicated once you get the hang of it!
[calibration]
calibration_type = 'convert' # 'convert' or 'calculate'

   [calibration.convert]
   convert_from = 'qualisys' # 'caliscope', 'qualisys', 'optitrack', vicon', 'opencap', 'easymocap', 'biocv', 'anipose', or 'freemocap'
      [calibration.convert.caliscope]  # No parameter needed
      [calibration.convert.qualisys]
      binning_factor = 1 # Usually 1, except when filming in 540p where it usually is 2
      [calibration.convert.optitrack]  # See readme for instructions
      [calibration.convert.vicon]      # No parameter needed
      [calibration.convert.opencap]    # No parameter needed
      [calibration.convert.easymocap]  # No parameter needed
      [calibration.convert.biocv]      # No parameter needed
      [calibration.convert.anipose]    # No parameter needed
      [calibration.convert.freemocap]  # No parameter needed
  

   [calibration.calculate] 
      # Camera properties, theoretically need to be calculated only once in a camera lifetime
      [calibration.calculate.intrinsics]
      overwrite_intrinsics = false # set to false if you don't want to recalculate intrinsic parameters
      show_detection_intrinsics = true # true or false (lowercase)
      intrinsics_extension = 'jpg' # any video or image extension
      extract_every_N_sec = 1 # if video, extract frames every N seconds (can be <1 )
      intrinsics_corners_nb = [4,7] 
      intrinsics_square_size = 60 # mm

      # Camera placements, need to be done before every session
      [calibration.calculate.extrinsics]
      calculate_extrinsics = true # true or false (lowercase) 
      extrinsics_method = 'scene' # 'board', 'scene', 'keypoints'
      # 'board' should be large enough to be detected when laid on the floor. Not recommended.
      # 'scene' involves manually clicking any point of know coordinates on scene. Usually more accurate if points are spread out.
      # 'keypoints' uses automatic pose estimation of a person freely walking and waving arms in the scene. Slighlty less accurate, requires synchronized cameras.
      moving_cameras = false # Not implemented yet

         [calibration.calculate.extrinsics.board]
         show_reprojection_error = true # true or false (lowercase)
         extrinsics_extension = 'png' # any video or image extension
         extrinsics_corners_nb = [4,7] # [H,W] rather than [w,h]
         extrinsics_square_size = 60 # mm # [h,w] if square is actually a rectangle

         [calibration.calculate.extrinsics.scene]
         show_reprojection_error = true # true or false (lowercase)
         extrinsics_extension = 'png' # any video or image extension
         # list of 3D coordinates to be manually labelled on images. Can also be a 2 dimensional plane. 
         # in m -> unlike for intrinsics, NOT in mm!
         object_coords_3d =   [[-2.0,  0.3,  0.0], 
                              [-2.0 , 0.0,  0.0], 
                              [-2.0, 0.0,  0.05], 
                              [-2.0, -0.3 ,  0.0], 
                              [0.0,  0.3,  0.0], 
                              [0.0, 0.0,  0.0], 
                              [0.0, 0.0,  0.05], 
                              [0.0, -0.3,  0.0]]
        
         [calibration.calculate.extrinsics.keypoints]
         # Coming soon!


[personAssociation]
   likelihood_threshold_association = 0.3

   [personAssociation.single_person]
   reproj_error_threshold_association = 20 # px
   tracked_keypoint = 'Neck' # If the neck is not detected by the pose_model, check skeleton.py 
               # and choose a stable point for tracking the person of interest (e.g., 'right_shoulder' or 'RShoulder')
   
   [personAssociation.multi_person]
   reconstruction_error_threshold = 0.1 # 0.1 = 10 cm
   min_affinity = 0.2 # affinity below which a correspondence is ignored


[triangulation]
reproj_error_threshold_triangulation = 15 # px
likelihood_threshold_triangulation= 0.3
min_cameras_for_triangulation = 2
interpolation = 'linear' #linear, slinear, quadratic, cubic, or none
                        # 'none' if you don't want to interpolate missing points
interp_if_gap_smaller_than = 10 # do not interpolate bigger gaps
show_interp_indices = true # true or false (lowercase). For each keypoint, return the frames that need to be interpolated
fill_large_gaps_with = 'last_value' # 'last_value', 'nan', or 'zeros' 
handle_LR_swap = false # Better if few cameras (eg less than 4) with risk of limb swapping (eg camera facing sagittal plane), otherwise slightly less accurate and slower
undistort_points = false # Better if distorted image (parallel lines curvy on the edge or at least one param > 10^-2), but unnecessary (and slightly slower) if distortions are low
make_c3d = true # save triangulated data in c3d format in addition to trc


[filtering]
type = 'butterworth' # butterworth, kalman, gaussian, LOESS, median, butterworth_on_speed
display_figures = true # true or false (lowercase) 
make_c3d = true # also save triangulated data in c3d format

   [filtering.butterworth]
   order = 4 
   cut_off_frequency = 6 # Hz
   [filtering.kalman]
   # How much more do you trust triangulation results (measurements), than previous data (process assuming constant acceleration)?
   trust_ratio = 100 # = measurement_trust/process_trust ~= process_noise/measurement_noise
   smooth = true # should be true, unless you need real-time filtering
   [filtering.butterworth_on_speed]
   order = 4 
   cut_off_frequency = 10 # Hz
   [filtering.gaussian]
   sigma_kernel = 2 #px
   [filtering.LOESS]
   nb_values_used = 30 # = fraction of data used * nb frames
   [filtering.median]
   kernel_size = 9


[markerAugmentation] 
## Requires the following markers: ["Neck", "RShoulder", "LShoulder", "RHip", "LHip", "RKnee", "LKnee",
##        "RAnkle", "LAnkle", "RHeel", "LHeel", "RSmallToe", "LSmallToe",
##        "RBigToe", "LBigToe", "RElbow", "LElbow", "RWrist", "LWrist"]
make_c3d = true # save triangulated data in c3d format in addition to trc


[kinematics]
use_augmentation = true  # true or false (lowercase) # Set to true if you want to use the model with augmented markers
right_left_symmetry = true # true or false (lowercase) # Set to false only if you have good reasons to think the participant is not symmetrical (e.g. prosthetic limb)
remove_individual_scaling_setup = true # true or false (lowercase) # If true, the individual scaling setup files are removed to avoid cluttering
remove_individual_IK_setup = true # true or false (lowercase) # If true, the individual IK setup files are removed to avoid cluttering



# CUSTOM skeleton, if you trained your own model from DeepLabCut or MMPose for example. 
# Make sure the node ids correspond to the column numbers of the 2D pose file, starting from zero.
# 
# If you want to perform inverse kinematics, you will also need to create an OpenSim model
# and add to its markerset the location where you expect the triangulated keypoints to be detected.
# 
# In this example, CUSTOM reproduces the HALPE_26 skeleton (default skeletons are stored in skeletons.py).
# You can create as many custom skeletons as you want, just add them further down and rename them.
# 
# Check your model hierarchy with:  for pre, _, node in RenderTree(model): 
#                                      print(f'{pre}{node.name} id={node.id}')
[pose.CUSTOM]
name = "Hip"
id = "19"
  [[pose.CUSTOM.children]]
  name = "RHip"
  id = 12
     [[pose.CUSTOM.children.children]]
     name = "RKnee"
     id = 14
        [[pose.CUSTOM.children.children.children]]
        name = "RAnkle"
        id = 16
           [[pose.CUSTOM.children.children.children.children]]
           name = "RBigToe"
           id = 21
              [[pose.CUSTOM.children.children.children.children.children]]
              name = "RSmallToe"
              id = 23
           [[pose.CUSTOM.children.children.children.children]]
           name = "RHeel"
           id = 25
  [[pose.CUSTOM.children]]
  name = "LHip"
  id = 11
     [[pose.CUSTOM.children.children]]
     name = "LKnee"
     id = 13
        [[pose.CUSTOM.children.children.children]]
        name = "LAnkle"
        id = 15
           [[pose.CUSTOM.children.children.children.children]]
           name = "LBigToe"
           id = 20
              [[pose.CUSTOM.children.children.children.children.children]]
              name = "LSmallToe"
              id = 22
           [[pose.CUSTOM.children.children.children.children]]
           name = "LHeel"
           id = 24
  [[pose.CUSTOM.children]]
  name = "Neck"
  id = 18
     [[pose.CUSTOM.children.children]]
     name = "Head"
     id = 17
        [[pose.CUSTOM.children.children.children]]
        name = "Nose"
        id = 0
     [[pose.CUSTOM.children.children]]
     name = "RShoulder"
     id = 6
        [[pose.CUSTOM.children.children.children]]
        name = "RElbow"
        id = 8
           [[pose.CUSTOM.children.children.children.children]]
           name = "RWrist"
           id = 10
     [[pose.CUSTOM.children.children]]
     name = "LShoulder"
     id = 5
        [[pose.CUSTOM.children.children.children]]
        name = "LElbow"
        id = 7
           [[pose.CUSTOM.children.children.children.children]]
           name = "LWrist"
           id = 9 """