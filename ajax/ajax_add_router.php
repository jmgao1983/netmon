<?php
  require_once __DIR__. '/../function/fun.php';
  require_once __DIR__. '/../function/fun2.php';
  session_start();
  if(isset($_SESSION['user'])){
     //$_GET and $_REQUEST are already decoded.
     $rip = $_GET['rip'];
     $rname = $_GET['rname'];
     $pass1 = my_encode($_GET['pass1'], $rname);
     $pass2 = my_encode($_GET['pass2'], $rname);
     $pass3 = my_encode($_GET['pass3'], $rname);
     $corp = $_GET['corp'];
     $mode = intval($_GET['mode']);
     $city = isset($_GET['city']) ? $_GET['city'] : $_SESSION['city'];
     $app  = $_GET['app'];

     $sql = "insert into router values('". $rip. "','". $rname. "','".
            $city. "','". $pass1. "','". $pass2. "','". $pass3. "','".
            $corp. "',". $mode. ",". $app. ")";

     //echo $sql;
     //return;
     $re = xxq($sql);
     if($re == 1){
        $msg = $_SESSION['user']. '添加router:'. $rip. "成功";
        $logger->info($msg);
        echo $msg;
     }else{
        $msg = $_SESSION['user']. '添加router:'. $rip. "失败";
        $logger->info($msg);
        echo $msg;
     }
  }
?>
