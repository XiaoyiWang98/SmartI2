# Index Machine FS

#采集端：
采集data，存进目录里面，然后存一个timestamp和index在一个localCSV里面
采集完data之后，把文件夹存进Samples文件夹里面，文件夹名是timestamp，记录timestamp到data的CSV文件夹里

#Sample Collection program:
After sampling the data, save them into a folder with the name of timestamp. 
Save a csv with index in the folder. Record timestamp to data.csv

#导出端：
显示所有timestamp文件夹名字，用户选择导出的timestamp名字，然后系统把timestamp存进setout文件夹里

#Setout
Show all datafolder's in the sample folder with the folder name of timestamp. 
Users can choose which one to be output. 
Save the folders users want to output in the setout folder.

#导入端：
系统读取timestamp文件夹，对比timestamp和data.csv查重复，
如果没重复的话直接copy选定的timestamp文件夹进Samples文件夹内

#Setin
Read the name of each folder in setin folder. Check with data.csv to prevent duplication.
If there is no duplications with current data in Samples, copy folder from Setin folder to
Sample folder. 

#处理端：
读取data.csv，确定现有的data数量
用for-loop跑get所有timestamp中的所有data

#
Read data.csv, get the number of data 
