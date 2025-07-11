## 项目简介[EN](https://github.com/AnGuoHui/RF4Helper/blob/main/readmeEn.md)
此脚本支持所有渔具种类的操作，支持中英双语客户端，提供自动制作/饮食操作，旨在简化捕获过程的重复操作，如有超过渔具
拉力范围的渔获，应当手动介入，否则存在损坏渔具的风险
## 本地运行脚本
git clone https://github.com/AnGuoHui/RF4Helper.git  
cd /path/RF4Helper  
pip install -r requirements.txt  
python main.py  
## 下载压缩包
[Releases](https://github.com/AnGuoHui/RF4Helper/releases/tag/v0.1.0)
## 使用手册
1. 所有带轮钓组都必需配置彩虹线
2. 使用赛干/博格尼亚杆必须设置管轮卡，在大风天气，或远距离操作时，推荐使用
3. 浮标识别目前只支持syberia styro b2和express fishing bob original两种浮标
4. 在使用中需要手动介入时，按下数字9以停止脚本
5. 折叠按钮会将运行窗口置于最上层固定
6. 使用脚本前应当关闭单击锁定，此设置会与脚本产生冲突
## 注意事项
1. 不推荐在官方下载的客户端执行此脚本，当等级超过35级且存在记录渔获时，有概率被制裁
2. 在使用浮标识别进行操作时，大风天气会极大影响浮标信号，导致错误的提竿
3. 多种太阳鱼的达标图标识别不准确，在捕获太阳鱼时，建议保留所有渔获
4. 所有操作依赖于屏幕截图，比对图标状态进行操作，应当保证鱼竿状态栏不会被光照影响
## 交流
qq群 619313190 
## 开源协议
[Apache License 2.0](https://github.com/AnGuoHui/RF4Helper/blob/main/LICENSE)
## 其他
1. 当前使用yolo模型样本较少，如有兴趣可以在https://roboflow.com中自行训练以获得更好的识别效果
2. 如有其他客户端支持需要，可在项目中operating_signal/static目录中添加客户端截图，并调试比对精度
