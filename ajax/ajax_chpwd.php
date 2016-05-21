<?php
   include __DIR__. '/../function/fun.php';
   session_start();
   if(isset($_SESSION['user'])){
      $name = $_SESSION['user'];
      $pwd = $_GET['pwd'];
      $pwd2 = $_GET['new'];
      //echo $pwd.$pwd2;
      $sql = "update user set pwd='".$pwd2."' where name='".$name."' and pwd='".$pwd."'";
      if(($re = xxq($sql)) == 1){
         $msg = $name. '修改密码成功';
         $logger->info($msg);
         echo $msg;
      }else{
         $msg = $name. '修改密码失败';
         $logger->info($msg);
         echo $msg;
      }
   }
?>
