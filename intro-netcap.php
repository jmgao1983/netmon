<?php
include 'header.php';
?>
<div class = "main">
  <p style="TEXT-ALIGN: center"><strong>网络设备状态验证使用说明</strong></p>
  <p>&nbsp;&nbsp;&nbsp; 为方便网络管理员在对设备进行例行重启、升级等工作，减少重复性劳动，该程序自动验证设备
  重启、升级前后相关状态信息是否一致，具体验证规则如下：</p>
  <p>&nbsp;&nbsp;&nbsp;<strong> 一、设备配置<br /></strong>&nbsp;&nbsp;&nbsp;
    1．检查设备重启、升级前后设备配置是否一致，如果不一致详细列出改变的地方。<br />&nbsp;&nbsp;&nbsp;
    2．<strong>注意</strong>以设备的运行配置(running-configration)为准，重启、升级前请保存好相关配置。<br />&nbsp;&nbsp;&nbsp;
    3. 思科设备使用 <strong>sh run</strong>命令。<br />&nbsp;&nbsp;&nbsp;
    4. 华三设备使用 <strong>disp curr</strong>命令。</p>
  <p>&nbsp;&nbsp;&nbsp;<strong> 二、板卡模块<br /></strong>&nbsp;&nbsp;&nbsp;
    1. 检查设备重启、升级前后设备加载的板卡模块信息是否一致，如改变则列出变化的内容。<br />&nbsp;&nbsp;&nbsp;
    2. 思科设备使用 <strong>sh module/sh inventory</strong>命令。<br />&nbsp;&nbsp;&nbsp;
    3. 华三设备使用 <strong>disp device</strong>命令。</p>
  <p>&nbsp;&nbsp;&nbsp;<strong> 二、端口信息<br /></strong>&nbsp;&nbsp;&nbsp;
    1. 检查设备重启、升级前后设备端口状态信息是否一致，如改变则列出变化的内容。<br />&nbsp;&nbsp;&nbsp;
    2. 端口信息包括全半双工、速率等物理层信息和IP地址等网络层信息。<br />&nbsp;&nbsp;&nbsp;
    3. 思科设备使用 <strong>sh int status/sh ip int b</strong>命令。<br />&nbsp;&nbsp;&nbsp;
    4. 华三设备使用 <strong>disp int brief</strong>命令。</p>
  <p>&nbsp;&nbsp;&nbsp;<strong> 三、二层信息<br /></strong>&nbsp;&nbsp;&nbsp;
    1. 检查设备重启、升级前后设备stp状态信息是否一致，如改变则列出变化的内容。<br />&nbsp;&nbsp;&nbsp;
    2. 暂时只检查生成树根信息。<br />&nbsp;&nbsp;&nbsp;
    3. 思科设备使用 <strong>sh spanning-tree root id</strong>命令。<br />&nbsp;&nbsp;&nbsp;
    4. 华三设备使用 <strong>disp stp root/disp stp brief</strong>命令。</p>
  <p>&nbsp;&nbsp;&nbsp;<strong> 四、路由信息<br /></strong>&nbsp;&nbsp;&nbsp;
    1. 检查设备重启、升级前后设备路由表信息是否一致，如改变则列出变化的内容。<br />&nbsp;&nbsp;&nbsp;
    2. 思科设备使用 <strong>sh ip route</strong>命令。<br />&nbsp;&nbsp;&nbsp;
    3. 华三设备使用 <strong>disp ip rout</strong>命令。</p>
</div>
<?php
include 'footer.php';
?>
