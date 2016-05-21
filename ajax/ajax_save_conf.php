<?php
   require_once __DIR__. '/../function/fun.php';
   session_start();
   if(isset($_SESSION['user'])){
      //
      $output = '';
      $cmd = 'python '. __DIR__. '/../script/ConfSaveOne.py ';
      $cmd = $cmd. $_GET['ip']. ' 2>&1';
      $last = exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      //
      if(strpos($last,'finish')){
         $msg = $_SESSION['user']. "保存配置:". $_GET['ip']. "成功";
         $logger->info($msg);
         echo "配置保存成功\n". $last;
      }else{
         $msg = $_SESSION['user']. "保存配置:". $_GET['ip']. "失败";
         $logger->error($msg);
         echo "配置保存失败\n". $last;
      }
   }
?>
