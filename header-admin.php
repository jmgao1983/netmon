<?php
header("Content-type:text/html;charset=utf-8");
session_start();
?>
<html>
   <head>
      <title>网络辅助管理平台</title>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <link href="resource/index.css" rel="stylesheet" type="text/css" />
      <script src="resource/js.js" type="text/javascript"></script>
      <script src="resource/md5.js" type="text/javascript"></script>
      <script src="resource/admin.js" type="text/javascript"></script>
   </head>
   <body>
   <div class = "header">
      <div id = "logo">
	     <br/><a href="#"><img src="resource/logo.gif"></a><br/>
      </div>
      <div id = "user">
	<?php if(isset($_SESSION['user'])){?>
	    <br/><br/><br/><br/>
	    <a href="#">
	      欢迎，<?php echo $_SESSION['user']?></a>&nbsp;&nbsp;
	    <a href="" onclick="logout();return false;">退出</a>
	  <?php }else{ ?>
	    <br/><br/>
	    管理员<input type='text' id='username' size=10/>&nbsp;
	    密码<input type='password' id='passwd' size=10/>&nbsp;
	    <button onclick="login()">登录</button>
	<?php } ?>
      </div>
      <div class = "floatclear"></div>
   </div>
   <div class = "navi">
      <ul class="ul_lv1" id="navtree">
	 <li class="li_lv1" id="nav1"><a class="a_lv1" href="admin.php" >基础数据</a></li>
	 <li class="li_lv1" id="nav2"><a class="a_lv1" href="admin-other.php" >参数设置</a></li>
	 <li class="li_lv1" id="nav2"><a class="a_lv1" href="admin-log.php" >运行日志</a></li>
      </ul>
      <hr/>
   </div>
   <div class = "floatclear">
   </div>
