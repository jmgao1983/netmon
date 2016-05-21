<?php
   include __DIR__. '/../function/fun.php';
   session_start();
   if(isset($_SESSION['user'])){
      $name = $_SESSION['user'];
      $mail1 = $_GET['mail1'];
      $mail2 = $_GET['mail2'];
      $phone = $_GET['phone'];
      //
      $sql = "update user set mail1='". $mail1. "',mail2='". $mail2.
         "',phone='". $phone. "' where name='". $name."'";
      if(($re = xxq($sql)) == 1){
         $msg = $name. "修改信息成功";
         $logger->info($msg);
         echo $msg;
      }else{
         $msg = $name. "修改信息失败";
         $logger->info($msg);
         echo $msg;
      }
   }
?>
