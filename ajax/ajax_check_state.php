<?php
   require_once __DIR__. '/../function/fun.php';
   session_start();
   if(isset($_SESSION['user'])){
      $sql = "select rname from router where rip='". $_GET['ip']. "'";
      $re = xget($sql);
      $rname = $re[0]['rname'];
      $path = __DIR__. '/../down/cap/'. md5($_SESSION['city']). '/'. $rname;
      $stamp = date("ymdHi");
      //
      $output = '';
      $out = '';
      $output = $output. "比对配置文件\n";
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';diff -a -s -y --suppress-common-lines conf.old conf 2>&1';
      exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      $out = '';
      $output = $output. "比对模块信息\n";
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';diff -a -s -y --suppress-common-lines mod.old mod 2>&1';
      exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      $out = '';
      $output = $output. "比对端口信息\n";
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';diff -a -s -y --suppress-common-lines int.old int 2>&1';
      exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      $out = '';
      $output = $output. "比对stp信息\n";
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';diff -a -s -y --suppress-common-lines stp.old stp 2>&1';
      exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      $out = '';
      $output = $output. "比对路由汇总信息\n";
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';diff -a -s -y --suppress-common-lines rtsum.old rtsum 2>&1';
      exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      $out = '';
      $output = $output. "比对路由明细信息\n";
      $cmd = 'cd '. $path;
      $cmd = $cmd. ';diff -a -s -y --suppress-common-lines route.old route 2>&1';
      exec($cmd, $out, $ret);
      for($i=0; $i<count($out); $i++){
         $output = $output. $out[$i]. "\n";
      }
      
      //记录状态比对结果
      $file = $path. '/result'. $stamp;
      $f = fopen($file, 'w');
      fwrite($f, $output);
      fclose($f);

      $logger->info($_SESSION['user']. "设置参考状态:". $_GET['ip']);
      echo $output;
   }
?>
