<?php
   require_once __DIR__. '/../function/fun.php';
   session_start();
   if(isset($_SESSION['user'])){
      $sql = "select rname from router where rip='". $_GET['ip']. "'";
      $re = xget($sql);
      $rname = $re[0]['rname'];
      $path = __DIR__. '/../down/cap/'. md5($_SESSION['city']). '/'. $rname;
      $stamp = date("ymdHi");

      //备份旧的当前状态
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';mv -f conf conf.'. $stamp;
      $cmd = $cmd. ';mv -f int int.'. $stamp;
      $cmd = $cmd. ';mv -f mod mod.'. $stamp;
      $cmd = $cmd. ';mv -f stp stp.'. $stamp;
      $cmd = $cmd. ';mv -f routesum routesum.'. $stamp;
      $cmd = $cmd. ';mv -f rtsum rtsum.'. $stamp;
      $cmd = $cmd. ';mv -f route route.'. $stamp;
      $cmd = $cmd. ';mv -f route.txt route.txt.'. $stamp;
      $cmd = $cmd. ' 2>&1';
      exec($cmd, $o, $return);
      
      //抓取当前状态
      $output = '';
      $cmd = 'python '. __DIR__. '/../script/capture.py ';
      $cmd = $cmd. $_GET['ip']. ' 2>&1';
      $last = exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }

      $logger->info($_SESSION['user']. "抓取当前状态:". $_GET['ip']);
      echo $output;
   }
?>
