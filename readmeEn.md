## Project Introduction [CN](https://github.com/AnGuoHui/RF4Helper/blob/main/readme.md)
This script supports operations for all types of fishing gear, supports bilingual (Chinese and English) clients, and provides automatic preparation/feeding operations, aiming to simplify   
repetitive operations in the capture process.If there are catches beyond the pulling range of the fishing gear, manual intervention should be carried out; otherwise, there is a risk of damaging the fishing gear

## Run the script locally
git clone https://github.com/AnGuoHui/RF4Helper.git  
cd /path/RF4Helper  
pip install -r requirements.txt  
python main.py  
## Download the compressed package
[Releases](https://github.com/AnGuoHui/RF4Helper/releases/tag/v0.1.0)
## User Manual
1. All reel fishing groups must be equipped with rainbow lines
2. When using the Match/Bolognese rod, a line clip must be set up. It is recommended to use it in windy weather or when operating from a distance
3. Buoy identification currently only supports two types of buoys: syberia styro b2 and express fishing bob original
4. When manual intervention is required during use, press the number 9 to stop the script
5. The fold button will fix the running window at the top layer
6. Before using the script, you should turn off the click lock setting. This setting will conflict with the script
## Precautions
1. It is not recommended to execute this script on the officially downloaded client. When the level exceeds 35 and there are recorded catches, there is a probability of being sanctioned
2. When operating with buoy recognition, strong wind weather can greatly affect the buoy signal, leading to incorrect pole lifting
3. The identification of the standard ICONS for various sunfish is inaccurate. When catching sunfish, it is recommended to keep all the catches
4. All operations rely on screenshots. When operating, compare the icon status to ensure that the fishing rod status bar is not affected by lighting
## License
Apache License 2.0
## Others
1. Currently, there are relatively few samples using the yolo model. If you are interested, you can train model in https://roboflow.com to achieve better recognition results
2. If there is a need for client support in other languages, you can add client screenshots in the operating_signal/static directory in the project and debug the comparison accuracy
