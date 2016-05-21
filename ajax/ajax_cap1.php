<?php
   require_once __DIR__. '/../function/fun.php';
   session_start();
   if(isset($_SESSION['user'])){
      $sql = "select rname from router where rip='". $_GET['ip']. "'";
      $re = xget($sql);
      $rname = $re[0]['rname'];
      $path = __DIR__. '/../down/cap/'. md5($_SESSION['city']). '/'. $rname;
      $stamp = date("ymdHi");
      //备份旧的参照状态
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';mv -f conf.old conf.old.'. $stamp;
      $cmd = $cmd. ';mv -f int.old int.old.'. $stamp;
      $cmd = $cmd. ';mv -f mod.old mod.old.'. $stamp;
      $cmd = $cmd. ';mv -f stp.old stp.old.'. $stamp;
      $cmd = $cmd. ';mv -f routesum.old routesum.old.'. $stamp;
      $cmd = $cmd. ';mv -f rtsum.old rtsum.old.'. $stamp;
      $cmd = $cmd. ';mv -f route.old route.old.'. $stamp;
      $cmd = $cmd. ';mv -f route.txt.old route.txt.old.'. $stamp;
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
      //把当前状态设定为参照状态
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';mv -f conf conf.old';
      $cmd = $cmd. ';mv -f int int.old';
      $cmd = $cmd. ';mv -f mod mod.old';
      $cmd = $cmd. ';mv -f stp stp.old';
      $cmd = $cmd. ';mv -f routesum routesum.old';
      $cmd = $cmd. ';mv -f rtsum rtsum.old';
      $cmd = $cmd. ';mv -f route route.old';
      $cmd = $cmd. ';mv -f route.txt route.txt.old';
      $cmd = $cmd. ' 2>&1';
      exec($cmd, $out, $ret);

      $logger->info($_SESSION['user']. "设置参考状态:". $_GET['ip']);
      echo $output;
   }
?>
