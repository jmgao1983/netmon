<?php
  include __DIR__. '/../function/fun.php';
  session_start();
  if(isset($_SESSION['user'])){
     //先把js传过来的中文编码进行解码
     $tdes = urldecode($_GET['tdes']);
     $sql = "select * from detail where tdes='".$tdes."'";
     $det = xget($sql);
     $re = count($det);
     if($re == 1){
        $out = "线路[". $_GET['tdes']. "]的详细信息如下：\n\n". 
            "线路编号:". $det[0]['line_no']. "\n报障电话:". $det[0]['isp_contact']. "\n". 
            "对端地址:". $det[0]['t_address']. "\n对端联系:". $det[0]['t_contact']. "\n".
            "应用名称:". $det[0]['app_name']. "\n应用联系:". $det[0]['app_contact']. "\n".
            "线路资费:". $det[0]['line_fee']. "\n线路所属:". $det[0]['line_own']. "\n".
            "其他信息:". $det[0]['memo'];
        $msg = $_SESSION['user']. '查看线路详情:'. $tdes. '成功';
        $logger->info($msg);
        echo $out;
     }else{
        $msg = $_SESSION['user']. '查看线路详情:'. $tdes. '失败';
        $logger->warn($msg);
        echo "没有该线路详细信息\n请在[编辑]中修改添加";
     }
  }
?>
