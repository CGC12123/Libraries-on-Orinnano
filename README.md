# Libraries-on-Orinnano
> 此包含搭载在无人机上 jetson orinnano 的所有程序\
> 包括双目的自启动及板载任务等

## 文件构成
- Start_system.py：\
    启动总入口（用于自启动）包括双目自启动及cv部分自启动等
- Cv_mode.py：\
    视觉任务入口
- communite_module/：\
    包含通信协议
- detection_module/：\
    包含检测任务所需要的文件
    - Detections.py 为检测任务总入口
- routines/:\
    包含一些可能用到的实例工具
- tools/：\
    包含工具类函数
