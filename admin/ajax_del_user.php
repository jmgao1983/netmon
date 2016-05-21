<?php
  include '../function/fun.php';
  session_start();
  if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){
     $name = $_GET['name'];
     $sql = "delete from user where name='".$name."'";
     if($re = xxq($sql) == 1){
        $msg = 'admin删除用户:'. $name. '成功';
        $logger->info($msg);
        echo $msg;
        return;
     }
  }
  $msg = 'admin删除用户:'. $name. '失败';
  $logger->info($msg);
  echo $msg;
?>
