<?php
  include '../function/fun.php';
  session_start();
  if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){
     //先把js传过来的中文编码进行解码
     $city = urldecode($_GET['city']);
     $name = $_GET['name'];
     $pwd  = $_GET['pwd'];
     $sql = "insert into user (city,name,pwd) values('".$city."','".$name."','".$pwd."')";
     
     if($re = xxq($sql) == 1){
        $msg = 'admin添加用户:'. $name. '成功';
        $logger->info($msg);
        echo $msg;
     }else{
        $msg = 'admin添加用户:'. $name. '失败';
        $logger->info($msg);
        echo $msg;
     }
  }
?>
