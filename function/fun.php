<?php
header("Content-type:text/html;charset=utf-8");
require_once 'logger.php';
//设置数据库参数
define('_dbhost',"localhost");
define('_dbuser',"netmon");
define('_dbpwd',"netmon");
define('_dbname',"netmon");

//从数据库中获取数据
function xget($sql){
   $arr = array();
// 创建连接
   $conn = new mysqli(_dbhost, _dbuser, _dbpwd, _dbname);
// 检测连接
   if ($conn->connect_error) {
      //die("Connection failed: " . $conn->connect_error);
      return $arr;
   }
   $conn->query('SET NAMES UTF8');
   $re = $conn->query($sql);
   while($row = $re->fetch_assoc()){
      $arr[] = $row;
   }
   $conn->close();
   return $arr;
}

//向表中插入、删除、修改数据
function xq($sql){
   $db = mysqli_connect(_dbhost, _dbuser, _dbpwd, _dbname);
   $charset = 'set names utf8';
   mysqli_query($db,$charset);
   $re = mysqli_query($db,$sql);
   mysqli_close($db);
   return $re;
}

//向表中插入、删除、修改数据、返回受影响行数
function xxq($sql){
   $db = mysqli_connect(_dbhost, _dbuser, _dbpwd, _dbname);
   $charset = 'set names utf8';
   mysqli_query($db,$charset);
   mysqli_query($db,$sql);
   $ret = mysqli_affected_rows($db);
   mysqli_close($db);
   return $ret;
}

//获取客户端IP
function get_real_ip(){
   $ip=false; 
   if(!empty($_SERVER['HTTP_CLIENT_IP'])){ 
      $ip=$_SERVER['HTTP_CLIENT_IP']; 
   }
   if(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])){
      $ips=explode (', ', $_SERVER['HTTP_X_FORWARDED_FOR']); 
      if($ip){ array_unshift($ips, $ip); $ip=FALSE; }
      for ($i=0; $i < count($ips); $i++){
         if(!eregi ('^(10│172.16│192.168).', $ips[$i])){
            $ip=$ips[$i];
            break;
         }
      }
   }
   return ($ip ? $ip : $_SERVER['REMOTE_ADDR']); 
}

//获取用户所在城市
function get_city(){
   $city = '全部';  //默认全部
   if(isset($_SESSION['city'])){
      $city = $_SESSION['city'];
      return $city;
   }
   if(isset($_GET['city'])){
      $city = $_GET['city'];
      setcookie('city',$city,time()+900);
      return $city;
   }
   if(isset($_COOKIE['city'])){
      $city = $_COOKIE['city'];
      return $city;
   }
   return $city;
}

//筛选条件判断与COOKIE设置
function get_filter($mysql){
   //COOKIE默认过期时间15分钟
   $expire = time() + 900;

if(!isset($_GET['clear'])){
  if(isset($_GET['rname'])||isset($_COOKIE['rname'])){
    if(isset($_GET['rname'])){
      $rname = $_GET['rname'];
      setcookie('rname',$rname,$expire);
    }else{
      $rname = $_COOKIE['rname'];
    }
    $mysql = $mysql." and rname='".$rname."'";
  }
  if(isset($_GET['isp'])||isset($_COOKIE['isp'])){
    if(isset($_GET['isp'])){
      $isp = $_GET['isp'];
      setcookie('isp',$isp,$expire);
    }else{
      $isp = $_COOKIE['isp'];
    }
    $mysql = $mysql." and isp='".$isp."'";
  }
  if(isset($_GET['status'])||isset($_COOKIE['status'])){
    if(isset($_GET['status'])){
      $status = $_GET['status'];
      setcookie('status',$status,$expire);
    }else{
      $status = $_COOKIE['status'];
    }
    if($status == 'Down'){
      $mysql = $mysql." and rtt=0";
    }else{
      $mysql = $mysql." and rtt>0";
    }
  }
  if(isset($_GET['tdes'])||isset($_COOKIE['tdes'])){
    if(isset($_GET['tdes'])){
      $tdes = $_GET['tdes'];
      setcookie('tdes',$tdes,$expire);
    }else{
      $tdes = $_COOKIE['tdes'];
    }
    $mysql = $mysql." and tdes like '%".$tdes."%'";
  }
  if(isset($_GET['tip'])||isset($_COOKIE['tip'])){
    if(isset($_GET['tip'])){
      $tip = $_GET['tip'];
      setcookie('tip',$tip,$expire);
    }else{
      $tip = $_COOKIE['tip'];
    }
    $mysql = $mysql." and tip like '%".$tip."%'";
  }
}else{
  //用户clear筛选条件后的COOKIE销毁
  $destroy = time() - 3600;
  setcookie('rname','',$destroy);
  setcookie('isp','',$destroy);
  setcookie('status','',$destroy);
  setcookie('tdes','',$destroy);
  setcookie('tip','',$destroy);
}
   return $mysql;
}
