# Index Machine FS

#采集端：
采集data，存进目录里面，然后存一个timestamp和index在一个localCSV里面
采集完data之后，把文件夹存进Samples文件夹里面，文件夹名是timestamp，记录timestamp到data的CSV文件夹里

#导出端：
显示所有timestamp文件夹名字，用户选择导出的timestamp名字，然后系统把timestamp存进setout文件夹里

#导入端：
系统读取timestamp文件夹，对比timestamp和data.csv查重复，如果没重复的话直接copy选定的timestamp文件夹进Samples文件夹内

#处理端：
读取data.csv，确定现有的data数量
用for-loop跑get所有timestamp中的所有data
