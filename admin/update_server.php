<?php
   require_once '../function/fun.php';
   session_start();
   if(isset($_SESSION['user']) && $_SESSION['user'] == 'admin'){
      //
      $output = '';

      $cmd = "expect ". __DIR__. "/../script/update.exp 2>&1";
      
      $last = exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      if($ret == 0){
         $msg = 'admin升级版本成功:'. $output. $cmd;
         $logger->info($msg);
         echo "升级成功";
      }else{
         $msg = 'admin升级版本失败:'. $output. $cmd;
         $logger->error($msg);
         echo "升级失败，请查看日志";
      }

   }else{
      echo "非授权用户\n";
   }
?>
