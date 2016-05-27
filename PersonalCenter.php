<?php
include 'header.php';
//判断是否登录用户，否则返回主页
if(isset($_SESSION['user'])){
  $usr = $_SESSION['user'];
  $sql = "select * from user where name='".$usr."'";
  //echo date("Y-m-d H:i");
  $re = xget($sql);
?>

<div class = "person">
  <div>
    <h4>配置中心：</h4>
    <ul class='ul_person'>
      <li><a href="#">用户名称:</a>&nbsp;<?php echo $usr ?></li>
      <li><a href="#">用户权限:</a>&nbsp;<?php echo $re[0]['city'] ?></li>
    </ul>
  </div>
  <p><a href="#">修改密码</a></p>
  <div id="chpwd">
     <p></p>
     旧密码: <input type="password" id="pwd_old" size="10">
     新密码: <input type="password" id="pwd_new1" size="10">
     再确认: <input type="password" id="pwd_new2" size="10">
     <button onclick=chpwd()>确定</button>
     <p></p>
  </div>
  <p><a href="#">告警开关</a>
  <select id="alert_sw" onchange=sw_alert(<?php echo "'".$re[0]['city']."'" ?>)>
     <option value='-1'>设置</option>
     <option value='1'>打开</option>
     <option value='0'>关闭</option>
  </select></p>
  <div id="chmail">
     <p></p>
     手机号码(14小时):  <input type="text" id="phone" size="45"
                         value=<?php echo $re[0]['phone'] ?>><br/>
     内网邮箱(24小时):  <input type="text" id="mail1" size="45"
                         value=<?php echo $re[0]['mail1'] ?>><br/>
     外网邮箱(14小时):  <input type="text" id="mail2" size="45"
                         value=<?php echo $re[0]['mail2'] ?>>
     <button onclick=chmail()>修改</button><br/>
     <p></p>
  </div>
</div>

<?php }else{ ?>
<div class='person'>
  <h3>请先登录</h3>
</div>
<?php
}
include 'footer.php';
?>
