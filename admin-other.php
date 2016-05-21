<?php
include 'header-admin.php';
require_once 'function/fun.php';
if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){

?>
<div class = "main">
  <h5>参数设置</h5>
  <div class="panel">
     <div class="txt_info">内网SMTP服务器设置</div><br/>
     服务器地址<input type="text" id="smtp_server" size="10">
     用户名<input type="text" id="smtp_usr" size="10">
     密码<input type="password" id="smtp_pwd" size="10">
     <button onclick=test_send_mail()>发送测试邮件</button>
     <span id="smtp_output" class="txt_warn"></span>
     <br/><br/>
     <select id = "s_loglvl">
       <option value='-1'>日志级别设置</option>
       <option value='10'>调试</option>
       <option value='20'>通知</option>
       <option value='30'>警告</option>
       <option value='40'>错误</option>
       <option value='50'>严重</option>
     </select>&nbsp;
     <select id = "s_threads">
       <option value='-1'>多线程设置</option>
       <option value='4'>4</option>
       <option value='8'>8</option>
       <option value='16'>16</option>
       <option value='32'>32</option>
     </select>
     </br></br>
     <button onclick=save_envi()>保存设置</button>
  </div>
  <br/><br/>
  <select id = "sw_ecnmon" onchange=sw_ecnmon()>
     <option><p>功能开关</p></option>
     <option><p>开启自动外联监控</p></option>
     <option><p>开启自动配置保存</p></option>
     <option><p>开启自动备份任务</p></option>
     <option><p>关闭所有自动任务</p></option>
  </select>&nbsp;
  <button onclick=update_server(this)>升级版本</button>&nbsp;
  <br/><br/>
</div>
<?php }else{ ?>
<div class='down'>
  <h3>请以管理员登录</h3>
</div>
<?php
}
include 'footer.php';
?>
