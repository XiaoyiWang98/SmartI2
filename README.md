## SmartI Capstone Project

Plan:<br>
  1. 480p frame acquisition via camera (Completed)<br>
  2. Perform face localization for the head (Completed)<br>
  3. From the results of face loacalization, capture the face frames of size 100 * 100 (Completed)<br>
  4. Train eyeball recognition using the face frames. Plan to use the CNN algorithm.<br>
     x - face frame; y - [middle, up, down, left, right, click] (The cursor follows the user's eyes. "Click" means blink)<br>
  5. Identify the position of eyeballs: using deep learning for result classification, determine the direction of cursor movement on the screen<br>

# Facial Sample Collection (StartUI.py):
Run the program:<br>
  1. Sample collection (face)<br>
  2. Python3 StartUI.py<br>
  3. Choose the camera<br>
  4. Start to collect the samples: 1) move the eyeballs according to the arrow direction; 2) when the eyeballs are in place, press 'd' to capture the next picture, press 'q' to exit<br>

Information of Sample:<br>
  x - image<br>
  y = filename mod 6<br>
  for example, if the filename is 7.jpg, y is 1<br>
  y = 0 :middle<br>
  y = 1 :up<br>
  y = 2 :down<br>
  y = 3 :left<br>
  y = 4 :right<br>
  y = 5 :click (blink)<br>

Virtual Environment:<br>
  URL: https://pan.baidu.com/s/1Hm6NEaVet1W8Ate6LS5zFw Password: ajw6<br>
  cd to "targetDirectory/bin" in the environment package，then "source activate"<br>

# Image Classification
  x: image; y: one-hot binary array [middle,up,down,left,right,click]<br>
  Plan to use CNN<br>

==============================================================================

计划：
1. 通过摄像头采集480p frame （Completed)<br>
2. 对头部进行face localization (Completed)<br>
3. 通过localization的结果采集截取100* 100的脸部frame (Completed)<br>
4. 用脸部frame 训练眼球识别，计划使用CNN，x为脸部frame，y为[middle, up, down, left, right, click], 向哪边看鼠标就往哪里跑，正常看屏幕鼠标就不动，click是眨眼<br>
5. 识别眼球的位置用DL结果进行classification，确定屏幕上光标移动方向<br>

# 面部样本采集程序 （通过StartUI.py进入）
运行：<br>
样本采集（面部）<br>
Python3 StartUI.py<br>
选择摄像头<br>
开始采集，根据箭头方向活动眼球，眼球到位后按'd'进入下一张图，长按'q'退出<br>

Sample信息：<br>
x 为图像 <br>
y = filename mod 6 <br>
for example, if the filename is 7.jpg, y is 1<br>
y = 0 :middle<br>
y = 1 :up<br>
y = 2 :down<br>
y = 3 :left<br>
y = 4 :right<br>
y = 5 :click (blink)<br>

Virtual Environment:<br>
链接: https://pan.baidu.com/s/1Hm6NEaVet1W8Ate6LS5zFw 密码: ajw6 <br>
cd 到环境包里的targetDirectory/bin，然后source activate <br>

# Image Classification
x 为图像，y为one-hot binary array [middle,up,down,left,right,click] <br>
计划使用CNN <br>

