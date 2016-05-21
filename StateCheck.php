<?php
include 'header.php';
//判断是否登录用户
if(isset($_SESSION['user']) && isset($_GET['ip'])){
?>

<div class='main'>
  <h4>网络设备<a href='intro-netcap.php'>状态验证</a>操作说明</h4>
  <p>第1步: 
    <input type="button" id="btn_cap1" onclick=cap1(this,'<?php echo $_GET['ip']?>') value="设置参照状态">
    &nbsp;(如已设置请跳过此步)
  </p>
  <p>第2步:
    <input type="button" id="btn_cap2" onclick=cap2(this,'<?php echo $_GET['ip']?>') value="抓取当前状态">
  </p>
  <p>第3步: 
    <input type="button" id="btn_mat" onclick=match(this,'<?php echo $_GET['ip']?>') value="开始状态验证">
  </p>
   <textarea id="log_win" rows="30" cols="130" readonly>
   </textarea>
</div>

<script src="resource/netcap.js" type="text/javascript"></script>

<?php }else{ ?>
<div class='main'>
  <h3>请先登录</h3>
</div>
<?php
}
include 'footer.php';
?>

