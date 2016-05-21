<?php
  include __DIR__. '/../function/fun.php';
  session_start();
  if(isset($_SESSION['user'])){
     //先把js传过来的中文编码进行解码
     $tdes = urldecode($_GET['tdes']);
     $sql = "delete from target where tdes='".$tdes."'";
     $re = xxq($sql);
     //只能单个删除，xxq返回值:-1表示sql执行错误，0,1,2,3...表示sql执行影响行数
     if($re == 1){
        $sql = "delete from detail where tdes='".$tdes."'";
        xxq($sql);
        $msg = $_SESSION['user']. '删除监控:'. $tdes. '成功';
        $logger->info($msg);
        echo $msg;
     }else{
        $msg = $_SESSION['user']. '删除监控:'. $tdes. '失败';
        $logger->info($msg);
        echo $msg;
     }
  }
?>
