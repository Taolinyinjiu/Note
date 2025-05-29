% 列出可用的摄像头
camList = webcamlist;
disp(['可用摄像头: ', strjoin(camList, ', ')]);

% 假设你的摄像头名称是 'Integrated Webcam' 或列表中的其他名称
try
    cam = webcam('Integrated Webcam'); % 将 'Integrated Webcam' 替换为你的摄像头名称
catch ME
    disp(['无法打开摄像头: ', ME.message]);
    return;
end

% 可以设置捕获图像的分辨率 (可选)
% cam.Resolution = '640x480';