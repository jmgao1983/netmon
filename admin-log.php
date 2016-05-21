<?php
include 'header-admin.php';
if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){

?>
<div class = "main">
  <p><a href="./log/link.log">线路通断日志</a></p>
  <p><a href="./log/web.log">网站访问日志</a></p>
  <p><a href="./log/netmon.log">后台运行日志</a></p>
  <p><a href="./log">全部历史日志</a></p>
</div>

<?php }else{ ?>
<div class='main'>
  <h3>请以管理员登录</h3>
</div>
<?php
}
include 'footer.php';
?>
