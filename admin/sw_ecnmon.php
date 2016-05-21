<?php
   require_once '../function/fun.php';
   session_start();
   if(isset($_SESSION['user']) && $_SESSION['user'] == 'admin'){
      //
      if(!isset($_GET['sw'])){
         echo '参数错误';
         return;
      }
      switch($_GET['sw']){
         case 1:
            $cmd = 'crontab '. __DIR__. '/../script/ecnmon_crond';
            break;
         case 2:
            $cmd = 'crontab '. __DIR__. '/../script/confsave_crond';
            break;
         case 3:
            $cmd = 'crontab '. __DIR__. '/../script/all_crond';
            break;
         case 4:
            $cmd = 'crontab -r';
            break;
         default:
            $msg = 'admin功能选择错误';
            $logger->error($msg);
            echo $msg;
            return;
      }

      $output = '';
      $cmd = $cmd . ' 2>&1';
      $last = exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      if($ret == 0){
         $msg = 'admin功能设置成功:'. $output. $cmd;
         $logger->info($msg);
         echo "功能设置成功";
      }else{
         $msg = 'admin功能设置失败:'. $output. $cmd;
         $logger->error($msg);
         echo "功能设置失败";
      }

   }else{
      echo "非授权用户\n";
   }
?>
