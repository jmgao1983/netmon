<?php
include 'header.php';
//判断是否登录用户，否则返回主页
if(isset($_SESSION['user'])){
   $sql_rname = "select rname from router where app=3 and city in (select city from target where tdes='".
                  $_GET['tdes']. "')";
   //获取'接入点'下拉框中的设备列表
   $s_rname = xget($sql_rname);

   //获取线路的告警手机和邮箱
   $sql = "select mail1,mail2,phone from target where tdes='". $_GET['tdes']. "'";
   $re = xget($sql);

   //获取线路的详细信息
   $sql = "select * from detail where tdes='". $_GET['tdes']. "'";
   $det = xget($sql);
   if(count($det)){
      $line_no = $det[0]['line_no'];
      $isp_contact = $det[0]['isp_contact'];
      $t_address = $det[0]['t_address'];
      $t_contact = $det[0]['t_contact'];
      $app_name = $det[0]['app_name'];
      $app_contact = $det[0]['app_contact'];
      $line_fee = $det[0]['line_fee'];
      $line_own = $det[0]['line_own'];
      $memo = $det[0]['memo'];
   }else{
      $line_no = '';
      $isp_contact = '';
      $t_address = '';
      $t_contact = '';
      $app_name = '';
      $app_contact = '';
      $line_fee = '';
      $line_own = '';
      $memo = '';
   }

?>

<div class = "edit">
  <div>
    <h4>编辑:
      <span id="tdes_edit"><?php echo $_GET['tdes'] ?></span>
    </h4>
  </div>
  <h5>基本信息</h5>
  <div class="panel">
    <select id="rname_edit">
       <option value='-1'>接入设备</option>
       <?php for($i=0; $i<count($s_rname); $i++){ ?>
       <option value=<?php echo $s_rname[$i]['rname'];?>>
          <?php echo $s_rname[$i]['rname'];?>
       </option>
       <?php } ?>
    </select>
    <input type="text" id="tip_edit" size="10" 
      value="<?php echo $_GET['tip'] ?>">
    <select id="isp_edit">
      <option value='-1'>运行商</option>
      <option value='DX'>电信</option>
      <option value='LT'>联通</option>
      <option value='HS'>华数</option>
      <option value='YD'>移动</option>
      <option value='QT'>其他</option>
    </select>
    <select id="alert_edit">
      <option value='-1'>告警</option>
      <option value='1'>普通告警</option>
      <option value='2'>优先告警</option>
      <option value='0'>关闭告警</option>
    </select>
    <span id="edit_info" class="txt_warn"></span>
     <p>为该线路设置独立的告警手机和邮箱(可以留空)
     填写多个号码、邮箱请以';'(英文分号)分隔
     </p>
     手机号码(14小时):  <input type="text" id="phone" size="45"
                         value=<?php echo $re[0]['phone'] ?>><br/>
     内网邮箱(24小时):  <input type="text" id="mail1" size="45"
                         value=<?php echo $re[0]['mail1'] ?>><br/>
     外网邮箱(14小时):  <input type="text" id="mail2" size="45"
                         value=<?php echo $re[0]['mail2'] ?>>
    <p>
      <button onclick=edit_confirm(<?php 
        echo "'".$_GET['tdes']."'";?>)>应用</button>
      <button onclick=edit_cancel()>取消</button>
    </p>
  </div>
  <h5>详细信息[选填]</h5>
  <div class="panel">
    线路编号:<input type="text" id="line_no" value=<?php echo $line_no ?>>&nbsp;
    报障电话:<input type="text" id="isp_contact" value=<?php echo $isp_contact ?>><br/>
    对端地址:<input type="text" id="t_address" value=<?php echo $t_address ?>>&nbsp;
    对端联系:<input type="text" id="t_contact" value=<?php echo $t_contact ?>><br/>
    应用名称:<input type="text" id="app_name" value=<?php echo $app_name ?>>&nbsp;
    应用联系:<input type="text" id="app_contact" value=<?php echo $app_contact ?>><br/>
    线路资费:<input type="text" id="line_fee" value=<?php echo $line_fee ?>>&nbsp;
    线路所属:<input type="text" id="line_own" value=<?php echo $line_own ?>><br/>
    其他信息:<input type="text" id="memo" size="50" value=<?php echo $memo ?>><br/>
    <p>
      <button onclick=ajax_edit_detail(<?php 
        echo "'".$_GET['tdes']."'";?>)>应用</button>
      <button onclick=edit_cancel()>取消</button>
    </p>
  </div>
  <p></p>
</div>

<?php }else{ ?>
<div class='edit'>
  <h3>请先登录,5秒后回到主页</h3>
</div>
<script language='javascript'>
  var t=setTimeout("location.href='index.php'",5000);
</script>
<?php
}
include 'footer.php';
?>
