<?php
header("Content-type:text/html;charset=utf-8");
require_once 'function/fun.php';
session_start();

$sql = "select city from city order by id";
$cities = xget($sql);
?>
<html>
   <head>
      <title>外联监控</title>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <meta name="keywords" content="网络监控,外联监控,智能监控,网管平台">
      <!--每隔300秒自动刷新页面-->
      <meta http-equiv="refresh" content="300">
      <link href="resource/index.css" rel="stylesheet" type="text/css" />
      <script src="resource/js.js" type="text/javascript"></script>
      <script src="resource/md5.js" type="text/javascript"></script>
   </head>
   <body>
   <div class = "header">
      <div id = "logo">
	     <a href="#"><img src="resource/logo.gif"></a>
      </div>
      <div id = "city">
	     <br/><b></b><br/>
	     <select id="s_city" onchange=select_city()>
          <option>城市</option>
          <?php for($i=0; $i<count($cities); $i++){ ?>
          <option><?php echo $cities[$i]['city']?></option>
          <?php } ?>
        </select>
      </div>
      <div id = "user">
	     <?php if(isset($_SESSION['user'])){?>
	        <br/><br/><br/>
	        <a href="PersonalCenter.php">
	         欢迎，<?php echo $_SESSION['user']?></a>&nbsp;&nbsp;
	        <a href="" onclick="logout();return false;">退出</a>
	     <?php }else{ ?>
	        <br/>
	       帐号<input type='text' id='username' size=10/>&nbsp;
	       <a href="#">注册</a><br />
	       密码<input type='password' id='passwd' size=10/>&nbsp;
	       <button onclick="login()">登录</button>
	     <?php } ?>
      </div>
      <div class = "floatclear"></div>
   </div>
   <div class = "navi">
      <ul class="ul_lv1" id="navtree">
	 <li class="li_lv1" id="nav1"><a class="a_lv1" href="index.php" >外联平台</a></li>
	 <li class="li_lv1" id="nav2"><a class="a_lv1" href="PersonalCenter.php" >用户设置</a></li>
	 <li class="li_lv1" id="nav3"><a class="a_lv1" href="tool.php" >实用工具</a></li>
	 <li class="li_lv1" id="nav5"><a class="a_lv1" href="down.php" >下载</a></li>
      </ul>
      <hr/>
   </div>
   <div class = "floatclear">
   </div>
