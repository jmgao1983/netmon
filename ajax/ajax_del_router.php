<?php
  include __DIR__. '/../function/fun.php';
  session_start();
  if(isset($_SESSION['user'])){
     $ip = $_GET['ip'];
     $app = $_GET['app'];
     $sql = "delete from router where rip='".$ip."' and app='". $app. "'";
     $re = xxq($sql);
     //只能单个删除，xxq返回值:-1表示sql执行错误，0,1,2,3...表示sql执行影响行数
     if($re == 1){
        $msg = 'admin删除设备:'. $ip. '成功';
        $logger->info($msg);
        echo $msg;
     }else{
        $msg = 'admin删除设备:'. $ip. '失败(请尝试在管理员页面删除)';
        $logger->info($msg);
        echo $msg;
     }
  }
?>
