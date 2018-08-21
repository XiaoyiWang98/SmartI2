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
  https://drive.google.com/file/d/1i3Nm69A6-eGy0TalZKg684q5KA4QiwPw/view?usp=sharing
  URL: https://pan.baidu.com/s/1Hm6NEaVet1W8Ate6LS5zFw Password: ajw6<br>
  cd to "targetDirectory/bin" in the environment package，then input command: source activate<br>

# Image Classification 
  x: image; y: one-hot binary array [middle,up,down,left,right,click]<br>
  Plan to use CNN<br>

