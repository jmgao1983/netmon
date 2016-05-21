<?php
  include '../function/fun.php';
  session_start();
  if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){
     //先把js传过来的中文编码进行解码
     $city = urldecode($_GET['city']);
     $sql = "insert into city (city) values('".$city."')";
     if($re = xxq($sql) == 1){
        $msg = 'admin添加城市:'. $city. "成功";
        $logger->info($msg);
        echo $msg;
        return;
     }
  }
  $msg = 'admin添加城市:'. $city. "失败";
  $logger->info($msg);
  echo $msg;
?>
