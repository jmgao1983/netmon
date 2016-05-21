<?php
  include __DIR__. '/../function/fun.php';
  session_start();
  if(isset($_SESSION['user'])){
     $rname = $_GET['rname'];
     $str_sql = "select city from router where rname='".$rname."'";
     $re = xget($str_sql);
     $city = $re[0]['city'];
     $tip = $_GET['tip'];
     //先把js传过来的中文编码进行解码
     $tdes = urldecode($_GET['tdes']);
     $isp = $_GET['isp'];
     $sql = "insert into target (tip,tdes,isp,city,rname) values('".
	        $tip."','".$tdes."','".$isp."','".$city."','".$rname."')";
     if($re = xxq($sql) == 1){
        $msg = $_SESSION['user']. '添加监控:'. $tdes. '成功';
        $logger->info($msg);
        echo $msg;
        return;
     }
  }
  $msg = $_SESSION['user']. '添加监控:'. $tdes. '失败';
  $logger->info($msg);
  echo $msg;
?>
