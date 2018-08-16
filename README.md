# SmartI Capstone Project
计划：

客户端
1. 通过摄像头采集480p frame （Completed)
2. 对头部进行face localization (Completed)
3. 通过localization的结果采集截取100* 100的脸部frame (Completed)
4. 用脸部frame 训练眼球识别，计划使用CNN，x为脸部frame，y为[middle, up, down, left, right, click], 向哪边看鼠标就往哪里跑，正常看屏幕鼠标就不动，click是眨眼
5. 识别眼球的位置用DL结果进行classification，确定屏幕上光标移动方向


运行：
样本采集（面部）
Python3 StartUI.py
选择摄像头
开始采集，根据箭头方向活动眼球，眼球到位后按'd'进入下一张图，长按'q'退出


