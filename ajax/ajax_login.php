<?php
  require_once __DIR__. '/../function/fun.php';
  session_start();
  $lifeTime = 14400;    //设置session为240分钟过期 
  setcookie(session_name(), session_id(), time() + $lifeTime, "/"); 

  $ip = get_real_ip();
  $usr = $_GET['usr'];
  $pwd = $_GET['pwd'];
  $sql = "select city from user where name='".$usr."' and pwd='".$pwd."'";
  $re = xget($sql);
  if(count($re) == 1){
    //设置session
    $_SESSION['user'] = $usr;
    $_SESSION['city'] = $re[0]['city'];
    $msg = $usr. '@'. $ip. '登陆成功';
    $logger->info($msg);
    echo '1';
  }else{
    $msg = $usr. '@'. $ip. '登陆失败';
    $logger->info($msg);
    echo '0';
  }
?>
