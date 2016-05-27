<?php
  include __DIR__. '/../function/fun.php';
  session_start();
  if(isset($_SESSION['user'])){
     $tip = $_GET['tip'];
     $rname = $_GET['rname'];
     //先把js传过来的中文编码进行解码
     $tdes = urldecode($_GET['tdes']);
     $isp = $_GET['isp'];
     $pri = $_GET['alert'];
     $mail1 = $_GET['mail1'];
     $mail2 = $_GET['mail2'];
     $phone = $_GET['phone'];
     $sql = "update target set tip='".$tip."',rname='".$rname."',isp='"
        .$isp."',pri=$pri,mail1='". $mail1. "',mail2='". $mail2. "',phone='" 
        .$phone. "' where tdes='".$tdes."'";
     //echo $sql;
     $re = xxq($sql);
     if($re == 1){
        $msg = $_SESSION['user']. '更新监控:'. $tdes. '成功';
        $logger->info($msg);
        echo $msg;
     }else{
        $msg = $_SESSION['user']. '更新监控:'. $tdes. '失败';
        $logger->info($msg);
        echo $msg;
     }
  }
?>
