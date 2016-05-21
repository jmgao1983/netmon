<?php
include 'header.php';
?>
<div class = "down">
<h4>资源下载</h4>
<a href="down/pub/">公共资源</a><br/>
用户手册:netmon.docx&nbsp;&nbsp;<a href="down/netmon.docx">下载</a><br/>
<?php
if(isset($_SESSION['user'])){
   $conf_path = 'down/conf/'. md5($_SESSION['city']);
   $cap_path = 'down/cap/'. md5($_SESSION['city']);
?>

<h4>配置备份</h4>
<a href="<?php echo $conf_path ?>"><?php echo $_SESSION['user'] ?>的设备配置</a><br/>

<h4>状态验证</h4>
<a href="<?php echo $cap_path ?>"><?php echo $_SESSION['user'] ?>的设备验证</a><br/>
<?php }else{ ?>
<div class='down'>
  <h3>请先登录</h3>
</div>
<?php
}
include 'footer.php';
?>
