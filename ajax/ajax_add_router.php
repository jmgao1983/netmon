<?php
  require_once __DIR__. '/../function/fun.php';
  session_start();
  if(isset($_SESSION['user'])){
     //$_GET and $_REQUEST are already decoded.
     $rip = $_GET['rip'];
     $rname = $_GET['rname'];
     $pass1 = $_GET['pass1'];
     $pass2 = $_GET['pass2'];
     $pass3 = $_GET['pass3'];
     $corp = $_GET['corp'];
     $mode = intval($_GET['mode']);
     $city = isset($_GET['city']) ? $_GET['city'] : $_SESSION['city'];
     $app  = $_GET['app'];
     if(strpos($pass1,"'") || strpos($pass2,"'") || strpos($pass3,"'")){
     	$sql = "insert into router values('". $rip. "','". $rname. "','".
            $city. "',". '"'. $pass1. '","'. $pass2. '","'. $pass3. '",'. "'".
            $corp. "',". $mode. ",". $app. ")";
     }else{
     	$sql = "insert into router values('". $rip. "','". $rname. "','".
            $city. "','". $pass1. "','". $pass2. "','". $pass3. "','".
            $corp. "',". $mode. ",". $app. ")";
     }
     //echo $sql;
     //return;
     $re = xxq($sql);
     if($re == 1){
        $msg = $_SESSION['user']. '添加router:'. $rip. "成功\n";
        $logger->info($msg);
        echo $msg;
     }else{
        $msg = $_SESSION['user']. '添加router:'. $rip. "失败\n". $sql;
        $logger->info($msg);
        echo $msg;
     }
  }
?>
