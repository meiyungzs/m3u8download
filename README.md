# m3u8视频下载器
### 依赖
+ python3 
+ ffmpeg 
+ requests库

### 简介  
github 上查了一下有一个 m3u8 下载器只不过是依赖 python2 的，让我很头疼，因为我不想再配 python2 的环境。所以花了半个晚上写了一个，本下载器利用多线程下载，没有对同时下载的数量进行控制，比如有1000个分段，就同时下载这1000个，所以网速可以跑满！下载速度很快！

### 使用方法 
在源码中写入`保存路径`及`下载地址`即可，上面有注释

