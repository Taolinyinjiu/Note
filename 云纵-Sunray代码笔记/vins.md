/camera/color/camera_info
/camera/color/image_raw
/camera/color/image_raw/compressed
/camera/color/image_raw/compressed/parameter_descriptions
/camera/color/image_raw/compressed/parameter_updates
/camera/color/image_raw/compressedDepth
/camera/color/image_raw/compressedDepth/parameter_descriptions
/camera/color/image_raw/compressedDepth/parameter_updates
/camera/color/image_raw/theora
/camera/color/image_raw/theora/parameter_descriptions
/camera/color/image_raw/theora/parameter_updates
/camera/depth/camera_info
/camera/depth/color/points
/camera/depth/image_raw
/camera/depth/image_raw/compressed
/camera/depth/image_raw/compressed/parameter_descriptions
/camera/depth/image_raw/compressed/parameter_updates
/camera/depth/image_raw/compressedDepth
/camera/depth/image_raw/compressedDepth/parameter_descriptions
/camera/depth/image_raw/compressedDepth/parameter_updates
/camera/depth/image_raw/theora
/camera/depth/image_raw/theora/parameter_descriptions
/camera/depth/image_raw/theora/parameter_updates
/camera/infra1/camera_info
/camera/infra1/image_raw
/camera/infra1/image_raw/compressed
/camera/infra1/image_raw/compressed/parameter_descriptions
/camera/infra1/image_raw/compressed/parameter_updates
/camera/infra1/image_raw/compressedDepth
/camera/infra1/image_raw/compressedDepth/parameter_descriptions
/camera/infra1/image_raw/compressedDepth/parameter_updates
/camera/infra1/image_raw/theora
/camera/infra1/image_raw/theora/parameter_descriptions
/camera/infra1/image_raw/theora/parameter_updates
/camera/infra2/camera_info
/camera/infra2/image_raw
/camera/infra2/image_raw/compressed
/camera/infra2/image_raw/compressed/parameter_descriptions
/camera/infra2/image_raw/compressed/parameter_updates
/camera/infra2/image_raw/compressedDepth
/camera/infra2/image_raw/compressedDepth/parameter_descriptions
/camera/infra2/image_raw/compressedDepth/parameter_updates
/camera/infra2/image_raw/theora
/camera/infra2/image_raw/theora/parameter_descriptions
/camera/infra2/image_raw/theora/parameter_updates



header: 
  seq: 3787
  stamp: 
    secs: 1765957120
    nsecs: 974315280
  frame_id: "D435i::camera_ired1_frame"
height: 480
width: 640
distortion_model: "plumb_bob"
D: []
K: [319.9348449707031, 0.0, 320.0, 0.0, 319.9348449707031, 240.0, 0.0, 0.0, 1.0]
R: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
P: [319.9348449707031, 0.0, 320.0, 0.0, 0.0, 319.9348449707031, 240.0, 0.0, 0.0, 0.0, 1.0, 0.0]
binning_x: 0
binning_y: 0
roi: 
  x_offset: 0
  y_offset: 0
  height: 0
  width: 0
  do_rectify: False




  header: 
  seq: 4112
  stamp: 
    secs: 1765957131
    nsecs: 815660876
  frame_id: "D435i::camera_ired2_frame"
height: 480
width: 640
distortion_model: "plumb_bob"
D: []
K: [319.9348449707031, 0.0, 320.0, 0.0, 319.9348449707031, 240.0, 0.0, 0.0, 1.0]
R: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
P: [319.9348449707031, 0.0, 320.0, 0.0, 0.0, 319.9348449707031, 240.0, 0.0, 0.0, 0.0, 1.0, 0.0]
binning_x: 0
binning_y: 0
roi: 
  x_offset: 0
  y_offset: 0
  height: 0
  width: 0
  do_rectify: False



在Gazebo中，Livox的IMU和飞控的IMU具有这同样地高斯噪声？如果使用的话其实最好是套一层滤波进行处理
目前的问题是对于D435i来说，在Gazebo中没有imu，这是什么问题呢，因为在sdf文件里面写到了有imu
对于姿态-推力算法，应该需要先做状态估计，以及先测量重量得到精确的重力，然后再套一层全状态控制器去解算姿态分配推力


header: 
  seq: 180
  stamp: 
    secs: 17
    nsecs: 608000000
  frame_id: "D435i::camera_depth_frame"
height: 480
width: 640
distortion_model: "plumb_bob"
D: []
K: [319.9348449707031, 0.0, 320.0, 0.0, 319.9348449707031, 240.0, 0.0, 0.0, 1.0]
R: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
P: [319.9348449707031, 0.0, 320.0, 0.0, 0.0, 319.9348449707031, 240.0, 0.0, 0.0, 0.0, 1.0, 0.0]
binning_x: 0
binning_y: 0
roi: 
  x_offset: 0
  y_offset: 0
  height: 0
  width: 0
  do_rectify: False

# 真值

  header: 
  seq: 24778
  stamp: 
    secs: 365
    nsecs: 612000000
  frame_id: "world"
child_frame_id: "base_link"
pose: 
  pose: 
    position: 
      x: -0.06957560032606125
      y: 0.07079733908176422
      z: 0.040893569588661194
    orientation: 
      x: -0.003826358935433646
      y: 0.009897613780517072
      z: -0.006338759575492846
      w: -0.9999236549430758

# vins 定位
header: 
  seq: 1077
  stamp: 
    secs: 340
    nsecs: 690000000
  frame_id: "world"
child_frame_id: "world"
pose: 
  pose: 
    position: 
      x: 0.01184117235983502
      y: -0.7085978321754045
      z: -0.07697573236941069
    orientation: 
      x: -0.0008990272378763017
      y: -0.004240871467884132
      z: 0.0033212837618135215
      w: 0.9999850878055092
  covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
twist: 
  twist: 
    linear: 
      x: -0.007386234336808415
      y: -0.007161758285478341
      z: -0.0005550143295719235
    angular: 
      x: 0.0
      y: 0.0
      z: 0.0
  covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


rosrun tf static_transform_publisher 0.0 0.0 0.0 1.57 3.14 1.57 base_link "D435i::camera_depth_frame" 100