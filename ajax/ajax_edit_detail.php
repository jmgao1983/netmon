<?php
  include __DIR__. '/../function/fun.php';
  session_start();
  if(isset($_SESSION['user'])){
     //ajax传过来的中文编码已经被自动解码
     //无需$tdes = urldecode($_GET['tdes']);
     $tdes = $_GET['tdes'];

     $sql = "delete from detail where tdes='".$tdes."'";
     xxq($sql);
     $sql = "insert into detail (tdes,line_no,isp_contact,t_address,t_contact,".
        "app_name,app_contact,line_fee,line_own,memo) values('".
        $_GET['tdes']. "','". $_GET['line_no']. "','". $_GET['isp_contact']. "','".
        $_GET['t_address']. "','". $_GET['t_contact']. "','". $_GET['app_name']. "','".
        $_GET['app_contact']. "','". $_GET['line_fee']. "','". $_GET['line_own']. "','".
        $_GET['memo']. "')";

     $re = xxq($sql);
     if($re == 1){
        $msg = $_SESSION['user']. '更新线路详情:'. $tdes. '成功';
        $logger->info($msg);
     }else{
        $msg = $_SESSION['user']. '更新线路详情:'. $tdes. '失败';
        $logger->warn($msg);
     }
     echo $msg;
  }
?>
