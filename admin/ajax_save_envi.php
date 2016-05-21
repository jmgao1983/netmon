<?php
  require_once '../function/fun.php';
  session_start();
  if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){
     $file = __DIR__ . '/../script/netmon_env.py';
     try{
        $envi = file_get_contents($file);
     }catch ( Exception $e ) {
        $logger->error($e->getMessage());
        $return;
     }
     $file2 = __DIR__ . '/../function/logger.php';
     try{
        $envi2 = file_get_contents($file2);
     }catch ( Exception $e ) {
        $logger->error($e->getMessage());
        $return;
     }
     
     if($_GET['log_lvl'] != ''){
        $pattern = "/'log_lvl': (\d+),/";
        $replace = "'log_lvl': " . $_GET['log_lvl'] . ",";
        $envi = preg_replace($pattern, $replace, $envi);

        $pattern2 = "/setLogLevel\(\d+/";
        $replace2 = "setLogLevel(" . $_GET['log_lvl'];
        $envi2 = preg_replace($pattern2, $replace2, $envi2);
     }
     if($_GET['threads'] != ''){
        $pattern = "/'threads': (\d+),/";
        $replace = "'threads': " . $_GET['threads'] . ",";
        $envi = preg_replace($pattern, $replace, $envi);
     }
     if($_GET['smtp_server'] != ''){
        $server = $_GET['smtp_server'];
        $pattern = "/'smtp_server': '(.*)',/";
        $replace = "'smtp_server': '" . $server . "',";
        $envi = preg_replace($pattern, $replace, $envi);

        $usr = $_GET['smtp_usr'];
        $pattern = "/'smtp_usr': '(.*)',/";
        $replace = "'smtp_usr': '" . $usr . "',";
        $envi = preg_replace($pattern, $replace, $envi);

        $pwd = $_GET['smtp_pwd'];
        $pattern = "/'smtp_pwd': '(.*)',/";
        $replace = "'smtp_pwd': '" . $pwd . "',";
        $envi = preg_replace($pattern, $replace, $envi);
     }
     if(file_put_contents($file, $envi) && file_put_contents($file2, $envi2)){
        $msg = 'admin配置保存成功';
        $logger->info($msg);
        echo $msg;
     }else{
        $msg = 'admin配置保存失败';
        $logger->info($msg);
        echo $msg;
     }
  }
?>
