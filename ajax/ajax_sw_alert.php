<?php
   include __DIR__. '/../function/fun.php';
   session_start();
   if(isset($_SESSION['user'])){
      //先把js传过来的中文编码进行解码
      $city = urldecode($_GET['city']);
      $pri = $_GET['pri'];
      if($city == "全部"){
         $sql = "update target set pri='".$pri."'";
      }else{
         $sql = "update target set pri='".$pri."' where city='".$city."'";
      }
      if(xxq($sql) > 0){
         if($pri == 1){
            $msg = $_SESSION['user']. '打开'. $city. '的全部告警';
            $logger->info($msg);
         }else{
            $msg = $_SESSION['user']. '关闭'. $city. '的全部告警';
            $logger->info($msg);
         }
         echo $msg;
      }else{
         $msg = $_SESSION['user']. '设置'. $city. '告警未变更';
         $logger->info($msg);
         echo $msg;
      }
   }
?>
